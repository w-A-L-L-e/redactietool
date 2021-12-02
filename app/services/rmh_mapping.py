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
from app.services.subtitle_files import get_property, get_array_property

logger = logging.get_logger(__name__, config=ConfigParser())


class RmhMapping:
    def __init__(self):
        print("RmhMapping initialized")

    def form_to_mh(self, request, mam_data):
        """
        convert form metadata hash into json data
        """
        print("TODO: convert following metadata:\n", request.form)
        errors = None  # for now, there will however be a lot more
        # logic and checks here that can generate errors, warnings etc.

        pid = request.form.get('pid')
        token = request.form.get('token')
        department = request.form.get('department')

        dc_description_lang = get_property(mam_data, 'dc_description_lang')
        ondertitels = get_property(mam_data, 'dc_description_ondertitels')
        cast = get_property(mam_data, 'dc_description_cast')
        transcriptie = get_property(mam_data, 'dc_description_transcriptie')

        # first example of actually editing field and putting back into
        # json blob
        ontsluitingstitel_edited = request.form.get('ontsluitingstitel')

        print("\n now save edited title in mam_data", ontsluitingstitel_edited)
        # mam_data
        for prop in mam_data['mdProperties']:
            if prop.get('attribute') == 'dc_title':
                prop['value'] = ontsluitingstitel_edited

        # make mediahaven PUT CALL HERE with transformed ontsluitingstitel and
        # other changed fields do same as above. after put call. make new get request
        # and update mam_data json then return our tp and/or possibly some req errors

        tp = {
            'token': token,
            'department': department,
            'mam_data': json.dumps(mam_data),
            'original_cp': get_property(mam_data, 'Original_CP'),
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
            # for v2 mam_data['Internal']['PathToVideo']
            'video_url': mam_data.get('videoPath'),
            'flowplayer_token': os.environ.get(
                'FLOWPLAYER_TOKEN', 'set_in_secrets'
            ),
            'validation_errors': errors,
            'data_saved_to_mam': True
        }

        # TODO: figure out how to turn our submitted params into the correct
        # json data or xml sidecar in order to update the wanted fields
        # for now return the template params as json
        return tp, json.dumps(tp), errors

    # TODO: also don't forget to make calls here using the suggest library from Miel.
    # we will be getting back id's from mediahaven and in order to populate
    # the dropdowns in form we will need some extra calls in order to fetch
    # the actual label and description:
    # https://github.com/viaacode/skos-scripts-redactietool

    # for the post call we don't need it as the id's will be directly pushed to mediahaven api
    # but this is something for later as Caroline needs to extend MAM structure
    # to have support for these.
    # more details in jira ticket https://meemoo.atlassian.net/browse/DEV-1821
    def mh_to_form(self, token, pid, department, errors, mam_data):
        """
        convert json metadata from MediahavenApi back into a
        python hash for populating the view
        """

        # debug data for in logs:
        print("DEBUG: mediahaven json_data:\n", mam_data)

        dc_description_lang = get_property(mam_data, 'dc_description_lang')
        ondertitels = get_property(mam_data, 'dc_description_ondertitels')
        cast = get_property(mam_data, 'dc_description_cast')
        transcriptie = get_property(mam_data, 'dc_description_transcriptie')

        return {
            'token': token,
            'department': department,
            'mam_data': json.dumps(mam_data),
            'original_cp': get_property(mam_data, 'Original_CP'),
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
            # for v2 mam_data['Internal']['PathToVideo']
            'video_url': mam_data.get('videoPath'),
            'flowplayer_token': os.environ.get(
                'FLOWPLAYER_TOKEN', 'set_in_secrets'
            ),
            'validation_errors': errors
        }
