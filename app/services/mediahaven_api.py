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
# import json
from requests import Session
from viaa.configuration import ConfigParser
from viaa.observability import logging
from app.services.subtitle_files import get_property, sidecar_root, get_array_property

from lxml import etree


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

    def find_item_by_pid(self, department, pid):
        # per request Athina, we drop the department filtering here
        # self.list_objects(search=f"%2B(DepartmentName:{department})%2B(ExternalId:{pid})")
        matched_videos = self.list_objects(
            department, search=f"%2B(ExternalId:{pid})")

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

    # With API v2 will this will be easier to make this call using json directly
    # but that requires refactoring authentication to mediahaven (also for the existing subloader
    # calls).
    # For now we stick with what works and use an xml sidecar which should be fine at least until 2023.

    def metadata_sidecar(self, metadata, tp):
        TESTBEELD_PERM_ID = os.environ.get(
            'TESTBEELD_PERM_ID', 'config_testbeeld_uuid')
        ONDERWIJS_PERM_ID = os.environ.get(
            'ONDERWIJS_PERM_ID', 'config_onderwijs_uuid')
        ADMIN_PERM_ID = os.environ.get('ADMIN_PERM_ID', 'config_admin_uuid')

        cp_id = get_property(metadata, 'CP_id')
        cp = get_property(metadata, 'CP')
        # xml_pid = f"{tp['pid']}_{tp['subtitle_type']}"

        root, MH_NS, MHS_NS, XSI_NS = sidecar_root()

        rights = etree.SubElement(
            root, '{%s}RightsManagement' % MHS_NS)
        perms = etree.SubElement(rights, '{%s}Permissions' % MH_NS)
        etree.SubElement(perms, '{%s}Read' % MH_NS).text = TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Read' % MH_NS).text = ONDERWIJS_PERM_ID
        etree.SubElement(perms, '{%s}Read' % MH_NS).text = ADMIN_PERM_ID
        etree.SubElement(perms, '{%s}Write' % MH_NS).text = TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Write' % MH_NS).text = ADMIN_PERM_ID
        etree.SubElement(perms, '{%s}Export' % MH_NS).text = TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Export' % MH_NS).text = ADMIN_PERM_ID

        mdprops = etree.SubElement(root, "{%s}Dynamic" % MHS_NS)

        # WARNING: is_verwant_aan is broken, see ticket dev-1900 in jira
        # relations = etree.SubElement(mdprops, "dc_relations")
        # etree.SubElement(relations, "is_verwant_aan").text = tp['pid']

        etree.SubElement(mdprops, "CP_id").text = cp_id
        # mediahaven computes external_id for us.
        # etree.SubElement(mdprops, "external_id").text = xml_pid
        etree.SubElement(mdprops, "PID").text = tp['pid']
        etree.SubElement(mdprops, "CP").text = cp
        etree.SubElement(mdprops, "sp_name").text = 'borndigital'

        # set ontsluitingstitel, uizenddatum, avo_beschrijving
        etree.SubElement(mdprops, "dc_title").text = get_property(
            metadata, 'dc_title')
        etree.SubElement(mdprops, "dcterms_issued").text = get_property(
            metadata, 'dcterms_issued')
        etree.SubElement(mdprops, "dcterms_abstract").text = get_property(
            metadata, 'dcterms_abstract')

        dc_titles = etree.SubElement(mdprops, "dc_titles")
        dc_titles.set('strategy', 'OVERWRITE')
        etree.SubElement(dc_titles, "serie").text = get_array_property(
            metadata, 'dc_titles', 'serie')

        # WARNING: this also does not save correctly now!
        # etree.SubElement(root, 'type').text = metadata.get('type') # default to video

        # eindgebruiker is multiselect
        lom_languages = etree.SubElement(mdprops, "lom_intendedenduserrole")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_intendedenduserrole'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # talen are multiselect
        lom_languages = etree.SubElement(mdprops, "lom_languages")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_languages'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # lom_onderwijsniveau are multiselect
        lom_languages = etree.SubElement(mdprops, "lom_onderwijsniveau")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_onderwijsniveau'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # lom_graad are multiselect
        lom_languages = etree.SubElement(mdprops, "lom_onderwijsgraad")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_onderwijsgraad'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # themas are multiselect
        lom_languages = etree.SubElement(mdprops, "lom_thema")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_thema'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # vakken are multiselect
        lom_languages = etree.SubElement(mdprops, "lom_vak")
        lom_languages.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_vak'):
            etree.SubElement(lom_languages, kw['attribute']).text = kw['value']

        # trefwoorden / keywords are 'Sleutelwoord'
        lom_keywords = etree.SubElement(mdprops, "lom_keywords")
        lom_keywords.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_keywords'):
            etree.SubElement(lom_keywords, kw['attribute']).text = kw['value']

        xml_data = etree.tostring(
            root, pretty_print=True, encoding="UTF-8", xml_declaration=True
        ).decode()

        return xml_data

    def update_metadata(self, department, metadata, tp):
        xml_sidecar = self.metadata_sidecar(metadata, tp)
        send_url = f"{self.API_SERVER}/resources/media/{metadata['fragmentId']}"
        print("\nSubmitting sidecar url=", send_url, "\nsidecar:\n", xml_sidecar)

        file_fields = {
            # 'file': (tp['srt_file'], open(srt_path, 'rb')),
            'metadata': ('metadata.xml', xml_sidecar),
            # 'externalId': ('', f"{tp['mam_data']['externalId']}_{tp['subtitle_type']}"),
            'externalId': ('', f"{metadata['externalId']}"),
            'departmentId': ('', self.DEPARTMENT_ID),
            'autoPublish': ('', 'true')
        }

        # logger.info("posting subtitles to mam", data=file_fields)
        response = self.session.post(
            url=send_url,
            auth=(self.api_user(tp['department']), self.API_PASSWORD),
            files=file_fields,
        )

        return response.status_code

    # below two methods are extra helpers only used by maintenance scripts
    def get_object(self, object_id, department='testbeeld'):
        return self.get_proxy(department, f"/resources/media/{object_id}")

    def list_videos(self, department='testbeeld'):
        matched_videos = self.list_objects(
            department, search=f"%2B(DepartmentName:{department})")
        return matched_videos
