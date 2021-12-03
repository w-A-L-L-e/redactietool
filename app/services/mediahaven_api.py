#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/mediahaven_api.py
#
#   Make api calls to hetarchief/mediahaven
#   find_video used to lookup video by pid and tenant
#   send_subtitles saves the srt file together with an xml sidecar
#   delete_old_subtitle used to replace existing srt with new upload
#

import os
from requests import Session
from viaa.configuration import ConfigParser
from viaa.observability import logging
from app.services.subtitle_files import get_property  # , get_array_property

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

    def __init__(self, session=None):
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def api_user(self, department):
        return f"{self.API_USER_PREFIX}{department}"

    # generic get request to mediahaven api
    def get_proxy(self, department, api_route):
        get_url = f"{self.API_SERVER}{api_route}"
        headers = {
            'Content-Type': 'application/json',
            # TODO: currently this breaks calls, re-enable later
            # for better compatibility with v2:
            # 'Accept': 'application/vnd.mediahaven.v2+json'
        }

        response = self.session.get(
            url=get_url,
            headers=headers,
            auth=(self.api_user(department), self.API_PASSWORD)
        )

        return response.json()

    def list_objects(self, department, search='', offset=0, limit=25):
        return self.get_proxy(
            department,
            f"/resources/media?q={search}&startIndex={offset}&nrOfResults={limit}"
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

    def find_video(self, department, pid):
        # per request Athina, we drop the department filtering here
        # self.list_objects(search=f"%2B(DepartmentName:{department})%2B(ExternalId:{pid})")
        matched_videos = self.list_objects(
            department, search=f"%2B(ExternalId:{pid})")

        if matched_videos.get('totalNrOfResults') == 1:
            return matched_videos.get('mediaDataList', [{}])[0]
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

    # This is far from finished. but as poc we truly propagate the dcterms_abstract to MH now ;)
    # problems:
    #   1 this is async so the get takes a while before showing true updated data
    #   2 we will in the end be moving to xml for batch field update with 1 call for multiple fields
    #
    # Also with API v2 will be easier to make this call using json directly
    # but requires different authentication (this is something for a future release to consider).
    # we know however v1 is still staying around until 2023.
    def update_metadata(self, department, metadata):
        # responses to handle:
        # 200 Ok: Record object
        # 400 Bad request: error result
        # 409 Conflict:
        # metadata = json.loads(tp['mam_data'])
        #  We can opt to also add some eventType or reason as params ex:
        #  -F "value=new title" -F "reason=my reason -F "eventType=my event type"

        print("DEBUG: sending metadata for department=", department, " to mediahaven:", metadata)
        fragment_id = metadata['fragmentId']
        avo_beschrijving = get_property(metadata, 'dcterms_abstract')
        print("sending this to mediahaven now: ", avo_beschrijving)

        # we only update dcterms_abstract for now:
        send_url = f"{self.API_SERVER}/resources/media/{fragment_id}/dcterms_abstract"

        # for now we skip these, but will do this later when we switch to bach update.
        # dc_title, dcterms_issued
        metadata_fields = {
            'departmentId': ('', self.DEPARTMENT_ID),
            # 'fragmentId': ('', f"{metadata['fragmentId']}"),
            # 'metadata': metadata,
            'dcterms_abstract': ('', avo_beschrijving),
            'autoPublish': ('', 'true')
        }

        logger.info("posting metadata to mam:", data=metadata_fields)
        response = self.session.post(
            url=send_url,
            auth=(self.api_user(department), self.API_PASSWORD),
            files=metadata_fields,
        )
        # return response.json()
        return response.status_code

    # below two methods are extra helpers only used by maintenance scripts
    def get_object(self, object_id, department='testbeeld'):
        return self.get_proxy(department, f"/resources/media/{object_id}")

    def list_videos(self, department='testbeeld'):
        matched_videos = self.list_objects(
            department, search=f"%2B(DepartmentName:{department})")
        return matched_videos
