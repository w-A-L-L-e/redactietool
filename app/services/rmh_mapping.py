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
# import os
# from requests import Session

import json
from viaa.configuration import ConfigParser
from viaa.observability import logging

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

    def mh_to_form(self, json_metadata):
        """
        convert json metadata from MediahavenApi back into a
        python hash for populating the view
        """
        print("TODO: convert json metadata for populating form:\n", json_metadata)

        # TODO: figure out how to return and use something like this:
        # token=token,
        # pid=pid,
        # department=department,
        # mam_data=json.dumps(mam_data),
        # title=mam_data.get('title'),
        # description=mam_data.get('description'),
        # created=get_property(mam_data, 'CreationDate'),
        # archived=get_property(mam_data, 'created_on'),
        # original_cp=get_property(mam_data, 'Original_CP'),
        # # for v2 mam_data['Internal']['PathToVideo']
        # video_url=mam_data.get('videoPath'),
        # flowplayer_token=os.environ.get('FLOWPLAYER_TOKEN', 'set_in_secrets')

        # # and add validation errors!

        return {}  # for now just an empty dictionary/hashmap
