#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/mediahaven_api.py
#
#   Make api calls to hetarchief/mediahaven
#   find video and audio fragments used to lookup video by pid and tenant
#   send_subtitles saves the srt file together with an xml sidecar
#   delete_old_subtitle used to replace existing srt with new upload
#

import os
from requests import Session
from viaa.configuration import ConfigParser
from viaa.observability import logging

logger = logging.get_logger(__name__, config=ConfigParser())


class MediahavenApi:
    # Voor v2 is endpoint hier /mediahaven-rest-api/v2/resources/
    # en met oauth ipv basic auth
    API_SERVER = os.environ.get(
        'MEDIAHAVEN_API',
        'https://archief-qas.viaa.be/mediahaven-rest-api'
    )
    API_USER_PREFIX = os.environ.get('MEDIAHAVEN_USER_PREFIX', 'viaa@')
    API_PASSWORD = os.environ.get('MEDIAHAVEN_PASS', 'password')
    DEPARTMENT_ID = os.environ.get(
        'DEPARTMENT_ID',
        'dd111b7a-efd0-44e3-8816-0905572421da'
    )

    # ONDERWIJS_PERM_ID is enkel voor de publicatiestatus flag
    ONDERWIJS_PERM_ID = os.environ.get(
        'ONDERWIJS_PERM_ID', 'config_onderwijs_uuid')

    def __init__(self, session=None):
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def api_user(self, department):
        return f"{self.API_USER_PREFIX}{department}"

    # generic get request to mediahaven api
    def get_proxy(self, department, api_route, enable_v2_header=False):
        get_url = f"{self.API_SERVER}{api_route}"
        headers = {
            'Content-Type': 'application/json',
        }

        if enable_v2_header:
            headers['Accept'] = 'application/vnd.mediahaven.v2+json'

        response = self.session.get(
            url=get_url,
            headers=headers,
            auth=(self.api_user(department), self.API_PASSWORD)
        )

        return response.json()

    def list_objects(self, department, search='', enable_v2_header=False, offset=0, limit=25):
        return self.get_proxy(
            department,
            f"/resources/media?q={search}&startIndex={offset}&nrOfResults={limit}",
            enable_v2_header=enable_v2_header
        )

    def find_by(self, department, object_key, value):
        search_matches = self.list_objects(
            department, search=f"+({object_key}:{value})")
        return search_matches

    def delete_fragment(self, department, frag_id):
        del_url = f"{self.API_SERVER}/resources/media/{frag_id}"
        del_resp = self.session.delete(
            url=del_url,
            auth=(self.api_user(department), self.API_PASSWORD)
        )

        logger.info(
            "deleted old subtitle fragment",
            data={
                'fragment': frag_id,
                'del_response': del_resp.status_code
            }
        )

    def find_item_by_pid(self, department, pid):
        # per request Athina, we drop the department filtering here
        # self.list_objects(search=f"%2B(DepartmentName:{department})%2B(ExternalId:{pid})")
        matched_videos = self.list_objects(
            department,
            search=f"%2B(ExternalId:{pid})",
        )

        nr_results = matched_videos.get('totalNrOfResults')
        if not nr_results:
            return None

        if nr_results == 1:
            return matched_videos.get('mediaDataList', [{}])[0]
        elif nr_results > 1:
            # future todo, iterate them and pick a certain one to return?
            return matched_videos.get('mediaDataList', [{}])[1]
        else:
            return None

    def delete_old_subtitle(self, department, subtitle_file):
        items = self.find_by(department, 'originalFileName', subtitle_file)
        if items.get('totalNrOfResults') >= 1:
            sub = items.get('mediaDataList')[0]
            frag_id = sub['fragmentId']
            self.delete_fragment(department, frag_id)

    def send_subtitles(self, upload_folder, metadata, tp):
        # sends srt_file and xml_file to mediahaven
        send_url = f"{self.API_SERVER}/resources/media/"
        srt_path = os.path.join(upload_folder, tp['srt_file'])
        xml_path = os.path.join(upload_folder, tp['xml_file'])

        file_fields = {
            'file': (tp['srt_file'], open(srt_path, 'rb')),
            'metadata': (tp['xml_file'], open(xml_path, 'rb')),
            'externalId': ('', f"{metadata['externalId']}_{tp['subtitle_type']}"),
            'departmentId': ('', self.DEPARTMENT_ID),
            'autoPublish': ('', 'true')
        }

        logger.info("posting subtitles to mam", data=file_fields)
        response = self.session.post(
            url=send_url,
            auth=(self.api_user(tp['department']), self.API_PASSWORD),
            files=file_fields,
        )

        return response.json()

    # only possible with v2 header this can replace find_item_by_pid
    # but will require the refactoring given in ticket DEV-1918
    def get_publicatiestatus(self, department, pid):
        matched_videos = self.list_objects(
            department,
            search=f"%2B(ExternalId:{pid})",
            enable_v2_header=True
        )

        nr_results = matched_videos.get('TotalNrOfResults')
        if not nr_results:
            return False

        if nr_results == 1:
            item_v2 = matched_videos.get('MediaDataList', [{}])[0]
        elif nr_results > 1:
            # future todo, iterate them and pick a certain one to return?
            item_v2 = matched_videos.get('MediaDataList', [{}])[1]
        else:
            return False

        # data = item_v2.get('Dynamic')
        # TODO: Later we can use this data to refactor the v1 calls in MetaMapping
        # and SubMapping
        # print(json.dumps(item_v2, indent=2))
        # import json

        permissions = item_v2.get('RightsManagement').get(
            'Permissions').get('Read')

        print("permissions=", permissions)

        return self.ONDERWIJS_PERM_ID in permissions

    def get_subtitles(self, department, pid):
        matched_subs = self.list_objects(
            department,
            search=f"+(dc_relationsis_verwant_aan:{pid})",
            enable_v2_header=True
        )
        nr_results = matched_subs.get('TotalNrOfResults')
        if not nr_results:
            return []

        return matched_subs.get('MediaDataList', [])

    def get_default_subtitle(self, department, pid):
        matched_subs = self.list_objects(
            department,
            search=f"+(dc_relationsis_verwant_aan:{pid})",
            enable_v2_header=True
        )

        nr_results = matched_subs.get('TotalNrOfResults')
        if not nr_results:
            return False

        if nr_results == 1:
            return matched_subs.get('MediaDataList', [{}])[0]
        elif nr_results > 1:
            # future todo, iterate them and pick a certain one to return?
            return matched_subs.get('MediaDataList', [{}])[1]
        else:
            return False

    def update_metadata(self, department, fragment_id, external_id, xml_sidecar):
        send_url = f"{self.API_SERVER}/resources/media/{fragment_id}"
        logger.info("syncing metadata to mediahaven...", data=xml_sidecar)

        file_fields = {
            'metadata': ('metadata.xml', xml_sidecar),
            'externalId': ('', f"{external_id}"),
            'departmentId': ('', self.DEPARTMENT_ID),
            'autoPublish': ('', 'true')
        }

        response = self.session.post(
            url=send_url,
            auth=(self.api_user(department), self.API_PASSWORD),
            files=file_fields,
        )

        return response

    # below two methods are extra helpers only used by maintenance scripts
    def get_object(self, object_id, department='testbeeld'):
        return self.get_proxy(department, f"/resources/media/{object_id}")

    def list_videos(self, department='testbeeld'):
        matched_videos = self.list_objects(
            department, search=f"%2B(DepartmentName:{department})")
        return matched_videos
