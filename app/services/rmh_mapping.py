#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/rmh_mapping.py
#
#   Do mapping between redactietool form and mh target data for saving changes.
#   Similarly load json data from MediahavenApi and populate form back.
#
# from requests import Session

import json
import os
from viaa.configuration import ConfigParser
from viaa.observability import logging
from app.services.subtitle_files import get_property, get_array_property, get_md_array
from app.services.mediahaven_api import MediahavenApi
from markupsafe import escape

logger = logging.get_logger(__name__, config=ConfigParser())


class RmhMapping:
    def __init__(self):
        print("RmhMapping initialised...")

    def set_property(self, mam_data, propkey, propvalue):
        for prop in mam_data['mdProperties']:
            if prop.get('attribute') == propkey:
                print("saving ", propkey,
                      "in mam_data with value=", escape(propvalue))
                prop['value'] = propvalue
                return mam_data

        # if we get here. we need to add a new property as it was cleared and
        # is not present anymore
        mam_data['mdProperties'].append({
            'value': propvalue,
            'attribute': propkey,
            'dottedKey': None
        })

        return mam_data

    def form_params(self, token, pid, department, errors, mam_data):
        dc_description_lang = get_property(mam_data, 'dc_description_lang')
        ondertitels = get_property(mam_data, 'dc_description_ondertitels')
        cast = get_property(mam_data, 'dc_description_cast')
        transcriptie = get_property(mam_data, 'dc_description_transcriptie')

        keyframe_edit_url = '{}{}'.format(
            os.environ.get('KEYFRAME_EDITING_LINK',
                           'https://set_in_secrets?id='),
            mam_data['fragmentId']
        )

        return {
            'token': token,
            'department': department,
            'mam_data': json.dumps(mam_data),
            'original_cp': get_property(mam_data, 'Original_CP'),
            'makers': get_md_array(mam_data, 'dc_creators'),
            'contributors': get_md_array(mam_data, 'dc_contributors'),
            'publishers': get_md_array(mam_data, 'dc_publishers'),
            'item_type': mam_data.get('type'),
            'item_themas': json.dumps(get_md_array(mam_data, 'lom_thema')),
            'item_vakken': json.dumps(get_md_array(mam_data, 'lom_vak')),
            'item_languages': json.dumps(get_md_array(mam_data, 'lom_languages')),
            'item_eindgebruikers': json.dumps(get_md_array(mam_data, 'lom_intendedenduserrole')),
            'item_onderwijsniveaus': json.dumps(
                get_md_array(
                    mam_data, 
                    'lom_onderwijsniveau',
                    legacy_fallback=True
                )
            ),
            'item_onderwijsniveaus_legacy': json.dumps(get_md_array(mam_data, 'lom_context')),
            'item_onderwijsgraden': json.dumps(
                get_md_array(
                    mam_data, 
                    'lom_onderwijsgraad',
                    legacy_fallback=True
                )
            ),
            'item_onderwijsgraden_legacy': json.dumps(get_md_array(mam_data, 'lom_typicalagerange')),
            'item_keywords_cp': json.dumps(get_md_array(mam_data, 'dc_subjects')),
            'item_keywords': json.dumps(get_md_array(mam_data, 'lom_keywords')),
            'dc_identifier_localid': get_property(mam_data, 'dc_identifier_localid'),
            'keyframe': mam_data.get('previewImagePath'),
            'pid': pid,
            'title': mam_data.get('title'),
            'ontsluitingstitel': get_property(mam_data, 'dc_title'),
            'titel_serie': get_array_property(mam_data, 'dc_titles', 'serie'),
            'titel_episode': get_array_property(mam_data, 'dc_titles', 'episode'),
            'titel_aflevering': get_array_property(mam_data, 'dc_titles', 'aflevering'),
            'titel_alternatief': get_array_property(mam_data, 'dc_titles', 'alternatief'),
            'titel_programma': get_array_property(mam_data, 'dc_titles', 'programma'),
            'titel_serienummer': get_array_property(mam_data, 'dc_titles', 'serienummer'),
            'titel_seizoen': get_array_property(mam_data, 'dc_titles', 'seizoen'),
            'titel_seizoen_nr': get_array_property(mam_data, 'dc_titles', 'seizoen_nr'),
            'titel_archief': get_array_property(mam_data, 'dc_titles', 'archief'),
            'titel_deelarchief': get_array_property(mam_data, 'dc_titles', 'deelarchief'),
            'titel_reeks': get_array_property(mam_data, 'dc_titles', 'reeks'),
            'titel_deelreeks': get_array_property(mam_data, 'dc_titles', 'deelreeks'),
            'titel_registratie': get_array_property(mam_data, 'dc_titles', 'registratie'),
            'description': mam_data.get('description'),
            'avo_beschrijving': get_property(mam_data, 'dcterms_abstract'),
            'ondertitels': ondertitels,
            'programma_beschrijving': get_property(mam_data, 'dc_description_programma'),
            'cast': cast,
            'transcriptie': transcriptie,
            'dc_description_lang': dc_description_lang,  # orig uitgebr. beschr
            'created': get_property(mam_data, 'CreationDate'),
            'dcterms_issued': get_property(mam_data, 'dcterms_issued'),
            # not used in form yet?
            'dcterms_created': get_property(mam_data, 'dcterms_created'),
            'archived': get_property(mam_data, 'created_on'),
            'keyframe_edit_url': keyframe_edit_url,
            # for v2 mam_data['Internal']['PathToVideo']
            'video_url': mam_data.get('videoPath'),
            'flowplayer_token': os.environ.get(
                'FLOWPLAYER_TOKEN', 'set_in_secrets'
            ),
            'validation_errors': errors
        }

    def form_to_mh(self, request, mam_data):
        """
        convert form metadata hash into json data
        """
        # print("DEBUG form metadata:\n", request.form)
        # logic and checks here that can generate errors, warnings etc.

        pid = escape(request.form.get('pid'))
        token = escape(request.form.get('token'))
        department = escape(escape(request.form.get('department')))

        # save some fields back into mam_data
        print("\n ontsluitingstitel=", escape(
            request.form.get('ontsluitingstitel')))
        mam_data = self.set_property(
            mam_data, 'dc_title',
            request.form.get('ontsluitingstitel')
        )

        print("uitzenddatum=", escape(request.form.get('uitzenddatum')))
        mam_data = self.set_property(
            mam_data, 'dcterms_issued',
            request.form.get('uitzenddatum')
        )

        # deze nog eventjes un-escaped
        print("avo_beschrijving=", request.form.get('avo_beschrijving'))
        mam_data = self.set_property(
            mam_data, 'dcterms_abstract',
            request.form.get('avo_beschrijving')
        )

        # todo fetch + write these also in the xml sidecar:
        print("DEBUG form data=", request.form)

        # maybe also serie, episode and aflevering editable (double check this tomorrow).
        # TODO:  mediahaven sidecar is necessary (put call does not work mh bug vs docs!
        mh_api = MediahavenApi()
        mh_api.update_metadata(department, mam_data)

        errors = None  # for now always none, hoever mh can give errors
        # also validation errors can be added here

        # we can even do another GET call here too if we want to validate the
        # changes have propagated this is even described in the mh documenation
        # as the call is async so we can check a modified timestamp and
        # wait until it changes...

        tp = self.form_params(token, pid, department, errors, mam_data)

        # if no errors from mediahaven put call signal a sucess notification:
        tp['data_saved_to_mam'] = True

        # return our params that are now saved in MH (or return responded errors)
        return tp, json.dumps(tp), errors

    # for the post call we don't need it as the id's will be directly pushed to mediahaven api
    # but this is something for later as Caroline needs to extend MAM structure
    # to have support for these:
    # more details in jira tickets
    #  https://meemoo.atlassian.net/browse/DEV-1821
    #  https://meemoo.atlassian.net/browse/OPS-1231
    def mh_to_form(self, token, pid, department, errors, mam_data):
        """
        convert json metadata from MediahavenApi back into a
        python hash for populating the view
        """

        # debug data for in logs:
        print("DEBUG: mediahaven json_data:\n")
        print(json.dumps(mam_data, indent=2))

        return self.form_params(token, pid, department, errors, mam_data)
