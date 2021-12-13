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
        print("RmhMapping initialized")

    def set_property(self, mam_data, propkey, propvalue):
        for prop in mam_data['mdProperties']:
            if prop.get('attribute') == propkey:
                print("saving ", propkey, "in mam_data with value=", escape(propvalue))
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
            os.environ.get('KEYFRAME_EDITING_LINK', 'https://set_in_secrets?id='),
            mam_data['fragmentId']
        )

        return {
            'token': token,
            'department': department,
            'mam_data': json.dumps(mam_data),
            'original_cp': get_property(mam_data, 'Original_CP'),
            'makers': get_md_array(mam_data, 'dc_creators'),
            'bijdragers': get_md_array(mam_data, 'dc_creators'),
            'publishers': get_md_array(mam_data, 'dc_contributors'),
            'dc_identifier_localid': get_property(mam_data, 'dc_identifier_localid'),
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
            # deze is zelfde waarde, stond fout in wireframes Koen
            # 'beschrijving_meemoo_redactie': get_property(mam_data, 'dcterms_abstract'),
            'avo_beschrijving': get_property(mam_data, 'dcterms_abstract'),
            'ondertitels': ondertitels,
            'programma_beschrijving': get_property(mam_data, 'dc_description_programma'),
            'cast': cast,
            'transcriptie': transcriptie,
            'dc_description_lang': dc_description_lang,  # orig uitgebr. beschr
            'created': get_property(mam_data, 'CreationDate'),
            'dcterms_issued': get_property(mam_data, 'dcterms_issued'),
            'dcterms_created': get_property(mam_data, 'dcterms_created'),  # not used in form yet?
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
        print("\n ontsluitingstitel=", escape(request.form.get('ontsluitingstitel')))
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

        # maybe also serie, episode and aflevering editable (double check this tomorrow).
        # TODO:  make mediahaven PUT CALL HERE with adjusted mam_data
        # disable until we generate batch update xml sidecar (theres a bug in the
        # single update field call which is not according to the docs). However we will
        # fix this tomorrow.
        mh_api = MediahavenApi()
        # mh_api = mh_api  # temp lint fix until tomorrow
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
    # more details in jira ticket https://meemoo.atlassian.net/browse/DEV-1821
    def mh_to_form(self, token, pid, department, errors, mam_data):
        """
        convert json metadata from MediahavenApi back into a
        python hash for populating the view
        """
        # TODO: also don't forget to make calls here using the suggest library from Miel.
        # we will be getting back id's from mediahaven and in order to populate
        # the dropdowns in form we will need some extra calls in order to fetch
        # the actual label and description:
        # https://github.com/viaacode/skos-scripts-redactietool

        # debug data for in logs:
        print("DEBUG: mediahaven json_data:\n", mam_data)

        return self.form_params(token, pid, department, errors, mam_data)
