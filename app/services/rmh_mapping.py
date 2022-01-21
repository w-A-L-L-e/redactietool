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

    def set_json_array_property(self, mam_data, propkey, jkey, jvalue, prop_name="multiselect"):
        values = json.loads(jvalue)
        array_values = []
        for v in values:
            array_values.append({
                'value': v[jkey],
                'attribute': prop_name,
                'dottedKey': None
            })

        # print("set_json_array values=", array_values, "prop_name", prop_name)

        for prop in mam_data['mdProperties']:
            if prop.get('attribute') == propkey:
                prop['value'] = array_values
                return mam_data

        mh_prop = {
            'value': array_values,
            'attribute': propkey,
            'dottedKey': None
        }

        # extra subKey to set here
        if prop_name == 'multiselect':
            mh_prop['subKey'] = 'multiselect'

        mam_data['mdProperties'].append(mh_prop)
        return mam_data

    def set_array_property(self, mam_data, attribute, array_attribute, propvalue):
        props = mam_data.get('mdProperties', [])
        array_attrib_exists = False
        array_prop = None
        for prop in props:
            if prop.get('attribute') == attribute:
                array_prop = prop
                array_values = prop.get('value', '')
                for att in array_values:
                    if att.get('attribute') == array_attribute:
                        array_attrib_exists = True
                        att['value'] = propvalue
                        return mam_data

        if not array_prop:
            array_val = [{
                'value': propvalue,
                'attribute': array_attribute,
                'dottedKey': None
            }]
            array_prop = {
                'attribute': attribute,
                'dottedKey': None,
                'value': array_val
            }
            mam_data['mdProperties'].append(array_prop)
            return mam_data

        if array_prop and not array_attrib_exists:
            array_prop['value'].append({
                'value': propvalue,
                'attribute': array_attribute,
                'dottedKey': None
            })
            return mam_data

        # in case it's new array prop (bail out for now):
        print(
            "ERROR in set_array_property: {}/{} with value {} not saved!".format(
                attribute,
                array_attribute,
                propvalue
            )
        )

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

        # fields we can alter+save:
        mam_data = self.set_property(
            mam_data, 'dc_title',
            request.form.get('ontsluitingstitel')
        )

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

        # array value serie in subsection dc_titles
        # (this is also how we need to save our productie section values soon!!!)
        mam_data = self.set_array_property(
            mam_data, 'dc_titles',
            'serie', request.form.get('serie')
        )

        # multiselect talen -> lom_languages
        mam_data = self.set_json_array_property(
            mam_data, 'lom_languages', 'code',
            request.form.get('talen'),
        )

        # multiselect item_eindgebruikers -> lom_intendedenduserrole
        mam_data = self.set_json_array_property(
            mam_data, 'lom_intendedenduserrole', 'code',
            request.form.get('lom1_beoogde_eindgebruiker'),
        )

        # multiselect item_onderwijsniveaus of item_onderwijsnivaus_legacy -> lom_onderwijsniveau
        mam_data = self.set_json_array_property(
            mam_data, 'lom_onderwijsniveau', 'id',
            request.form.get('lom1_onderwijsniveaus'),
        )

        # multiselect item_onderwijsgraden of item_onderwijsgraden_legacy -> lom_onderwijsgraad
        mam_data = self.set_json_array_property(
            mam_data, 'lom_onderwijsgraad', 'id',
            request.form.get('lom1_onderwijsgraden'),
        )

        # multiselect themas -> lom_thema
        mam_data = self.set_json_array_property(
            mam_data, 'lom_thema', 'id',
            request.form.get('themas'),
            'Thema'
        )

        # multiselect vakken -> lom_vak
        mam_data = self.set_json_array_property(
            mam_data, 'lom_vak', 'id',
            request.form.get('vakken'),
            'Vak'
        )

        # TODO: lom_legacy 'boolean field' -> save as 'false' if vakken or themas contain entries

        # Sleutelwoord(en) trefwoorden -> lom_keywords
        mam_data = self.set_json_array_property(
            mam_data, 'lom_keywords', 'name',
            request.form.get('trefwoorden'),
            'Sleutelwoord'
        )

        # item_type heeft nog een issue (check vrijdag met rudolf of bart -> is omdat
        # het een level boven de mdprops zit)
        changed_item_type = json.loads(request.form.get('item_type'))
        if type(changed_item_type) == list:
            item_type = changed_item_type[0]['code']
        else:
            item_type = changed_item_type['code']
        mam_data['type'] = item_type


        # TODO: productie velden: dc_creators, dc_contributors and dc_publishers
        # 'makers': get_md_array(mam_data, 'dc_creators'),
        # 'contributors': get_md_array(mam_data, 'dc_contributors'),
        # 'publishers': get_md_array(mam_data, 'dc_publishers'),
        
        # makers = get_md_array(mam_data, 'dc_creators')
        # first fix issue in frontend, the attribute needs to be numbered here like we do for value
        # so we can match up the dropdown with correct input and re-populate the arrays here based on
        
        # fields in request.form:
        #  for f in request.form:
        #     print("field=", f)



        # Wat met publiatiestatus checkbo here? :
        # form field name = publicatiestatus -> lom_publicatie ????


        # also validation errors can be added here
        errors = None  # for now always none, hoever mh can give errors
        tp = self.form_params(token, pid, department, errors, mam_data)

        mh_api = MediahavenApi()
        result = mh_api.update_metadata(department, mam_data, tp)
        print("save result=", result)

        # we can even do another GET call here too if we want to validate the
        # changes have propagated this is even described in the mh documenation
        # as the call is async so we can check a modified timestamp and
        # wait until it changes...

        # if no errors from mediahaven and no validation errors signal a sucess notification:
        tp['data_saved_to_mam'] = True
        # else set this to False + set errors (can be used to show dialog in case of errors)

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
