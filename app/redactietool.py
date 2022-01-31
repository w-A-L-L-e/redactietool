#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers and integrated
#           code from python-saml3 flask demo for SAML authorization
#
#           Thanks to 'suggest library' from Miel Vander Sande that will
#           be used to populate the dropdowns in the metadata
#           form's LOM sections. Suggest is part of the KnowledeGraph project.
#
#  app/redactietool.py
#
#   Application to upload srt file and push into mediahaven.
#   It stores and converts an uploaded srt file to webvtt format,
#   shows preview with flowplayer and subtitles.
#   Metadata is fetched with mediahaven_api using a pid.
#   Authorization is done by feching jwt token from oas.viaa.be and passing
#   jwt between forms and pages as 'token'. This token is verified in the
#   authorization.py module, using decorator @requires_authorization
#
#   Future work is also editing metadata for same PID entry with addition
#   of calls to knowledgegraph api from Miel Vander Sande

import os
import json

from flask import (Flask, request, render_template, session,  # make_response,
                   redirect, url_for, send_from_directory)

# only needed for saml debug session
# from flask import abort, jsonify

from flask_api import status
from viaa.configuration import ConfigParser
from viaa.observability import logging

from app.config import flask_environment
from app.services.authorization import (get_token, requires_authorization,
                                        verify_token, check_saml_session, OAS_APPNAME)
from app.services.mediahaven_api import MediahavenApi
from app.services.suggest_api import SuggestApi
from app.services.ftp_uploader import FtpUploader
from app.services.subtitle_files import (
    save_subtitles, delete_files, save_sidecar_xml,
    move_subtitle, get_property, not_deleted, srt_to_vtt
)
from app.services.validation import (pid_error, upload_error, validate_input,
                                     validate_upload, validate_conversion)

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from flask_login import LoginManager, login_required  # current_user
from app.services.rmh_mapping import RmhMapping
from app.services.user import User


app = Flask(__name__)
config = ConfigParser()
logger = logging.get_logger(__name__, config=config)

app.config.from_object(flask_environment())

# disables caching of srt and other files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# TODO: replace these with some ENV vars soon:

# session cookie/saml key TODO: put this in env var!
app.config['SECRET_KEY'] = 'meemoo_saml_secret_to_be_set_using_configmap_or_secrets'
app.config['SAML_PATH'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'saml'
)

# optional:
# right now session expires only when browser is closed
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=9)
# with this we need to set :
# sesson.permanent = True


# mixin/model for current_user method of flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.request_loader
def load_user_from_request(request):
    user = User()
    if check_saml_session():
        user.save_saml_username(session.get('samlUserdata'))
    else:
        # and throw away invalid or timed out session
        session.clear()
        token = request.form.get('token', None)
        if not token:
            token = request.args.get('token', None)

        if token:
            user.save_jwt_username(token)

    return user


# ====================== LEGACY LOGIN RELATED ROUTES ==========================
@app.route('/legacy_login', methods=['GET'])
def legacy_login():
    return render_template('legacy_login.html')


@app.route('/legacy_login', methods=['POST'])
def login():
    if app.config['DEBUG'] is True and not app.config['TESTING']:
        print('DISABLE login checks for development/debug mode')
        return redirect(
            url_for('.search_media', token='debug_authorization_disabled')
        )

    username = request.form.get('username')
    password = request.form.get('password')
    logger.info("POST login =", dictionary={
        'username': username,
        'password': '[FILTERED]'
    })
    token = get_token(username, password)
    if token:
        if verify_token(token['access_token']):
            return redirect(url_for('.search_media', token=token['access_token']))
        else:
            return render_template(
                'legacy_login.html',
                validation_errors=f"Login correct, maar geen toegang tot {OAS_APPNAME}"
            )

    else:
        return render_template('legacy_login.html', validation_errors='Fout email of wachtwoord')


# ========================== SAML Authentication ==============================
def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth


def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    legact_login_enabled = app.config['DEBUG'] is True and not app.config['TESTING']

    if 'sso' in request.args:
        # If AuthNRequest ID need to be stored in
        # order to later validate it, do instead
        sso_built_url = auth.login()
        session['AuthNRequestID'] = auth.get_last_request_id()
        return redirect(sso_built_url)
    elif 'slo' in request.args:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        if 'samlNameIdFormat' in session:
            name_id_format = session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in session:
            name_id_nq = session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in session:
            name_id_spnq = session['samlNameIdSPNameQualifier']

        return redirect(
            auth.logout(
                name_id=name_id,
                session_index=session_index,
                nq=name_id_nq,
                name_id_format=name_id_format,
                spnq=name_id_spnq
            )
        )
    elif 'acs' in request.args:
        request_id = None
        if 'AuthNRequestID' in session:
            request_id = session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            if 'AuthNRequestID' in session:
                del session['AuthNRequestID']
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlNameIdFormat'] = auth.get_nameid_format()
            session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the request.form['RelayState'] is a trusted URL.
                return redirect(
                    auth.redirect_to(
                        request.form['RelayState']
                    )
                )
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
    elif 'sls' in request.args:
        request_id = None
        if 'LogoutRequestID' in session:
            request_id = session.get(
                'LogoutRequestID', 'empty_logout_request_id')

        def dscb(): return session.clear()

        # HOTFIX so that the POST_DATA is put in GET_DATA and we properly
        # respond to the sls request from our idp
        req['get_data'] = req['post_data']

        # re-init auth with hotfixed request object
        auth = init_saml_auth(req)

        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the url is a trusted URL.
                return redirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if check_saml_session():
        return redirect('/search_media')
    else:
        return render_template(
            'index.html',
            errors=errors,
            error_reason=error_reason,
            not_auth_warn=not_auth_warn,
            success_slo=success_slo,
            attributes=attributes,
            legact_login_enabled=legact_login_enabled,
        )


# ======================== SUBLOADER RELATED ROUTES ===========================
@app.route('/search_media', methods=['GET'])
@requires_authorization
@login_required
def search_media():
    if 'samlUserdata' in session:
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()
        token = 'saml'
    else:
        token = request.args.get('token')

    validation_errors = request.args.get('validation_errors')
    logger.info('search_media')

    return render_template('search_media.html', **locals())


@app.route('/search_media', methods=['POST'])
@requires_authorization
@login_required
def post_media():
    token = request.form.get('token')
    pid = request.form.get('pid')
    department = request.form.get('department')

    if not pid:
        return pid_error(token, pid, 'Geef een PID')
    else:
        if request.form.get('redirect_subtitles') == 'yes':
            logger.info('post_media, editing subtitles', data={'pid': pid})
            return redirect(url_for('.get_upload', **locals()))
        else:
            logger.info('post_media, editing metadata', data={'pid': pid})
            return redirect(url_for('.edit_metadata', **locals()))


@app.route('/upload', methods=['GET'])
@requires_authorization
@login_required
def get_upload():
    logger.info('get_upload')

    token = request.args.get('token')
    pid = request.args.get('pid').strip()
    department = request.args.get('department')
    errors = request.args.get('validation_errors')

    validation_error = validate_input(pid, department)
    if validation_error:
        return pid_error(token, pid, validation_error)

    mh_api = MediahavenApi()
    mam_data = mh_api.find_item_by_pid(department, pid)
    if not mam_data:
        return pid_error(token, pid, f"PID niet gevonden in {department}")

    return render_template(
        'subtitles/upload.html',
        token=token,
        pid=pid,
        department=department,
        mam_data=json.dumps(mam_data),
        title=mam_data.get('title'),
        keyframe=mam_data.get('previewImagePath'),
        description=mam_data.get('description'),
        created=get_property(mam_data, 'CreationDate'),
        archived=get_property(mam_data, 'created_on'),
        original_cp=get_property(mam_data, 'Original_CP'),
        # for v2 mam_data['Internal']['PathToVideo']
        video_url=mam_data.get('videoPath'),
        flowplayer_token=os.environ.get('FLOWPLAYER_TOKEN', 'set_in_secrets'),
        validation_errors=errors)


@app.route('/upload', methods=['POST'])
@requires_authorization
@login_required
def post_upload():
    tp = {
        'token': request.form.get('token'),
        'pid': request.form.get('pid'),
        'department': request.form.get('department'),
        'mam_data': request.form.get('mam_data'),
        'video_url': request.form.get('video_url'),
        'subtitle_type': request.form.get('subtitle_type')
    }

    validation_error, uploaded_file = validate_upload(tp, request.files)
    if validation_error:
        return upload_error(tp, validation_error)

    tp['subtitle_file'], tp['vtt_file'] = save_subtitles(
        upload_folder(), tp['pid'], uploaded_file)

    conversion_error = validate_conversion(tp)
    if conversion_error:
        return upload_error(tp, conversion_error)

    logger.info('subtitles/preview', data={
        'pid': tp['pid'],
        'file': tp['subtitle_file']
    })

    video_data = json.loads(tp['mam_data'])
    tp['title'] = video_data.get('title')
    tp['description'] = video_data.get('description')
    tp['keyframe'] = video_data.get('previewImagePath')
    tp['created'] = get_property(video_data, 'CreationDate')
    tp['archived'] = get_property(video_data, 'created_on')
    tp['original_cp'] = get_property(video_data, 'Original_CP')
    tp['flowplayer_token'] = os.environ.get(
        'FLOWPLAYER_TOKEN', 'set_in_secrets')

    return render_template('subtitles/preview.html', **tp)


def upload_folder():
    return os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])


@app.route('/subtitles/<filename>')
@requires_authorization
@login_required
def uploaded_subtitles(filename):
    return send_from_directory(upload_folder(), filename)


@app.route('/cancel_upload')
@requires_authorization
@login_required
def cancel_upload():
    token = request.args.get('token')
    pid = request.args.get('pid')
    department = request.args.get('department')
    vtt_file = request.args.get('vtt_file')
    srt_file = request.args.get('srt_file')

    delete_files(upload_folder(), {
        'srt_file': srt_file,
        'vtt_file': vtt_file
    })

    return redirect(url_for('.get_upload', token=token, pid=pid, department=department))


@app.route('/send_to_mam', methods=['POST'])
@requires_authorization
@login_required
def send_to_mam():

    tp = {
        'token': request.form.get('token'),
        'pid': request.form.get('pid'),
        'department': request.form.get('department'),
        'video_url': request.form.get('video_url'),
        'subtitle_type': request.form.get('subtitle_type'),
        'srt_file': request.form.get('subtitle_file'),
        'vtt_file': request.form.get('vtt_file'),
        'xml_file': request.form.get('xml_file'),
        'xml_sidecar': request.form.get('xml_sidecar'),
        'mh_response': request.form.get('mh_response'),
        'mam_data': request.form.get('mam_data'),
        'replace_existing': request.form.get('replace_existing'),
        'transfer_method': request.form.get('transfer_method')
    }

    # TODO: refactor out code duplication
    video_data = json.loads(tp['mam_data'])
    tp['title'] = video_data.get('title')
    tp['keyframe'] = video_data.get('previewImagePath')
    # tp['description'] = video_data.get('description')
    # tp['created'] = get_property(video_data, 'CreationDate')
    # tp['archived'] = get_property(video_data, 'created_on')
    # tp['original_cp'] = get_property(video_data, 'Original_CP')
    tp['flowplayer_token'] = os.environ.get(
        'FLOWPLAYER_TOKEN', 'set_in_secrets')
    
    print("tp=", tp)

    if tp['replace_existing'] == 'cancel':
        # abort and remove temporary files
        delete_files(upload_folder(), tp)

    # extra check to avoid re-sending if user refreshes page
    if not_deleted(upload_folder(), tp['srt_file']):
        metadata = json.loads(tp['mam_data'])
        if not tp['replace_existing']:
            # first request, generate xml_file
            tp['srt_file'] = move_subtitle(upload_folder(), tp)

            tp['xml_file'], tp['xml_sidecar'] = save_sidecar_xml(
                upload_folder(), metadata, tp)

        if tp['transfer_method'] == 'api':
            mh_api = MediahavenApi()
            if tp['replace_existing'] == 'confirm':
                mh_api.delete_old_subtitle(tp['department'], tp['srt_file'])

            mh_response = mh_api.send_subtitles(upload_folder(), metadata, tp)
            logger.info('send_to_mam', data=mh_response)
            tp['mh_response'] = json.dumps(mh_response)

            if not tp['replace_existing'] and (
                (mh_response.get('status') == 409)
                or
                (mh_response.get('status') == 400)
            ):  # duplicate error can give 409 or 400, show dialog
                return render_template('subtitles/confirm_replace.html', **tp)
        else:
            # upload subtitle and xml sidecar with ftp instead
            ftp_uploader = FtpUploader()
            ftp_response = ftp_uploader.upload_subtitles(
                upload_folder(), metadata, tp)
            tp['mh_response'] = json.dumps(ftp_response)

        # cleanup temp files and show final page with mh request results
        delete_files(upload_folder(), tp)
        return render_template('subtitles/sent.html', **tp)
    else:
        # user refreshed page (tempfiles already deleted),
        # or user chose 'cancel' above. in both cases show
        # subtitles already sent
        tp['upload_cancelled'] = True
        return render_template('subtitles/sent.html', **tp)


# ====================== Redactietool metadata ROUTES =========================
@app.route('/edit_metadata', methods=['GET'])
@requires_authorization
@login_required
def edit_metadata():
    token = request.args.get('token')
    pid = request.args.get('pid').strip()
    department = request.args.get('department')
    errors = request.args.get('validation_errors')

    logger.info(f'GET item_metadata pid={pid}')

    validation_error = validate_input(pid, department)
    if validation_error:
        return pid_error(token, pid, validation_error)

    mh_api = MediahavenApi()
    mam_data = mh_api.find_item_by_pid(department, pid)
    if not mam_data:
        return pid_error(token, pid, f"PID niet gevonden in {department}")

    data_mapping = RmhMapping()
    template_vars = data_mapping.mh_to_form(
        token, pid, department, mam_data, errors)

    # extra request necessary in order to fetch rightsmanagement/permissions
    template_vars['publish_item'] = mh_api.get_publicatiestatus(
        department, pid)

    return render_template(
        'metadata/edit.html',
        **template_vars
    )


@app.route('/edit_metadata', methods=['POST'])
@requires_authorization
@login_required
def save_item_metadata():
    token = request.form.get('token')
    pid = request.form.get('pid')
    department = request.form.get('department')

    print("item pid=", pid)

    mh_api = MediahavenApi()
    mam_data = mh_api.find_item_by_pid(department, pid)
    if not mam_data:
        return pid_error(token, pid, f"PID niet gevonden in {department}")

    data_mapping = RmhMapping()
    template_vars = data_mapping.form_to_mh(request, mam_data)

    return render_template(
        'metadata/edit.html',
        **template_vars
    )


@app.route('/onderwijsniveaus', methods=['GET'])
@requires_authorization
@login_required
def get_onderwijsniveaus():
    suggest_api = SuggestApi()
    return suggest_api.get_onderwijsniveaus()


@app.route('/onderwijsgraden', methods=['GET'])
@requires_authorization
@login_required
def get_onderwijsgraden():
    suggest_api = SuggestApi()
    return suggest_api.get_onderwijsgraden()


@app.route('/themas', methods=['GET'])
@requires_authorization
@login_required
def get_themas():
    suggest_api = SuggestApi()
    return suggest_api.get_themas()


@app.route('/vakken', methods=['GET'])
@requires_authorization
@login_required
def get_vakken():
    suggest_api = SuggestApi()
    return suggest_api.get_vakken()


@app.route('/vakken_suggest', methods=['POST'])
@requires_authorization
@login_required
def get_vakken_suggesties():
    json_data = request.json
    print("json_data=", json_data)
    suggest_api = SuggestApi()
    result = suggest_api.get_vakken_suggesties(
        json_data['graden'], json_data['themas'])
    return result


@app.route('/item_subtitles', methods=['GET'])
@requires_authorization
@login_required
def get_subtitles():
    # see this on how to construct a proper link
    # https://meemoo.atlassian.net/browse/DEV-1872?focusedCommentId=25119
    srt_url = 'https://archief-media.meemoo.be/viaa/MOB/TESTBEELD/...35b8.srt'
    return srt_to_vtt(srt_url)


# =================== HEALTH CHECK ROUTES AND ERROR HANDLING ==================
@app.route("/health/live")
def liveness_check():
    return "OK", status.HTTP_200_OK


@app.errorhandler(401)
def unauthorized(e):
    # return "<h1>401</h1><p>Unauthorized</p>", 401
    return redirect(
        url_for('.index', token=None)
    )


@app.errorhandler(404)
def page_not_found(e):
    # TODO: also a redirect but set some flash message here
    return "<h1>404</h1><p>Page not found</p>", 404


# =============== Main application startup without debug mode ================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
