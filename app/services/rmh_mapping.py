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
from app.services.subtitle_files import get_property

logger = logging.get_logger(__name__, config=ConfigParser())


class RmhMapping:
    def __init__(self):
        print("RmhMapping initialized")

    def form_to_mh(self, request):
        """
        convert form metadata hash into json data
        """
        print("TODO: convert following metadata:\n", request.form)

        tp = {
            'token': request.form.get('token'),
            'pid': request.form.get('pid'),
            'department': request.form.get('department'),
            'mam_data': request.form.get('mam_data'),
            'video_url': request.form.get('video_url'),
            'subtitle_type': request.form.get('subtitle_type')
        }

        errors = None  # for now, there will however be a lot more
        # logic and checks here that can generate errors, warnings etc.

        # TODO: figure out how to turn our submitted params into the correct
        # json data or xml sidecar in order to update the wanted fields
        # for now return the template params as json
        return tp, json.dumps(tp), errors

    def mh_to_form(self, token, pid, department, errors, mam_data):
        """
        convert json metadata from MediahavenApi back into a
        python hash for populating the view
        """

        # debug data for in logs:
        print("TODO: find mapped fields in json_data:\n", mam_data)
        dc_description_lang = get_property(
            mam_data,
            'dc_description_lang'
        )

        # TODO: check tomorrow if we should make this the
        # default behaviour for get_property
        if dc_description_lang is None:
            dc_description_lang = ''

        # also don't forget to make calls here using the suggest library from Miel.
        # we will be getting back id's from mediahaven and in order to populate
        # the dropdowns in form we will need some extra calls in order to fetch
        # the actual label and description:
        # https://github.com/viaacode/skos-scripts-redactietool

        # for the post call we don't need it as the id's will be directly pushed to mediahaven api
        # but this is something for later as Caroline needs to extend MAM structure
        # to have support for these.
        # more details in jira ticket https://meemoo.atlassian.net/browse/DEV-1821

        # TODO: also be more logic involved to prepare the values of
        # lists for instance in the productie section etc.

        return {
            'token': token,
            'pid': pid,
            'department': department,
            'mam_data': json.dumps(mam_data),
            'title': mam_data.get('title'),
            'description': mam_data.get('description'),
            'dc_description_lang': dc_description_lang,  # orig uitgebreide beschrijving
            'created': get_property(mam_data, 'CreationDate'),
            'archived': get_property(mam_data, 'created_on'),
            'original_cp': get_property(mam_data, 'Original_CP'),
            # for v2 mam_data['Internal']['PathToVideo']
            'video_url': mam_data.get('videoPath'),
            'flowplayer_token': os.environ.get(
                'FLOWPLAYER_TOKEN', 'set_in_secrets'
            ),
            'validation_errors': errors
        }
