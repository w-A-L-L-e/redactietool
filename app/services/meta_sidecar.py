#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/meta_sidecar.py
#
#   This class can generate a xml sidecar for doing updates on metadata for items in
#   mediahaven. With API v2 this class could become deprecated if we have the possibility
#   to do all the wanted updates with json directly.
#

import os
from app.services.subtitle_files import get_property, sidecar_root, get_array_property
from lxml import etree


class MetaSidecar:
    def __init__(self):
        self.TESTBEELD_PERM_ID = os.environ.get(
            'TESTBEELD_PERM_ID', 'config_testbeeld_uuid')
        self.ONDERWIJS_PERM_ID = os.environ.get(
            'ONDERWIJS_PERM_ID', 'config_onderwijs_uuid')
        self.ADMIN_PERM_ID = os.environ.get(
            'ADMIN_PERM_ID', 'config_admin_uuid')

    def save_array_field(self, metadata, fieldname, mdprops, field_attrib="multiselect"):
        array_values = get_property(metadata, fieldname)
        array_elem = etree.SubElement(mdprops, fieldname)
        array_elem.set('strategy', 'OVERWRITE')
        if array_values and len(array_values) > 0:
            for kw in array_values:
                etree.SubElement(
                    array_elem, kw['attribute']).text = kw['value']
        else:
            etree.SubElement(array_elem, field_attrib).text = ''

    def generate(self, metadata, tp):
        root, MH_NS, MHS_NS, XSI_NS = sidecar_root()
        rights = etree.SubElement(root, '{%s}RightsManagement' % MHS_NS)

        perms = etree.SubElement(rights, '{%s}Permissions' % MH_NS)
        perms.set('strategy', 'OVERWRITE')

        # now set our permissions and exclude the ONDERWIJS_PERM_ID
        # when publish_item is not set
        etree.SubElement(perms, '{%s}Read' %
                         MH_NS).text = self.TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Read' % MH_NS).text = self.ADMIN_PERM_ID

        if tp.get('frontend_metadata').get('publish_item'):
            etree.SubElement(perms, '{%s}Read' %
                             MH_NS).text = self.ONDERWIJS_PERM_ID
            print(
                "publicatiestatus == TRUE, added read permission =",
                self.ONDERWIJS_PERM_ID
            )

        else:
            print("publicatiestatus== FALSE")

        etree.SubElement(perms, '{%s}Write' %
                         MH_NS).text = self.TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Write' % MH_NS).text = self.ADMIN_PERM_ID
        etree.SubElement(perms, '{%s}Export' %
                         MH_NS).text = self.TESTBEELD_PERM_ID
        etree.SubElement(perms, '{%s}Export' % MH_NS).text = self.ADMIN_PERM_ID

        mdprops = etree.SubElement(root, "{%s}Dynamic" % MHS_NS)

        # Alemene fields:
        # ===============
        # ontsluitingstitel
        etree.SubElement(mdprops, "dc_title").text = get_property(
            metadata, 'dc_title')

        # uizenddatum
        etree.SubElement(mdprops, "dcterms_issued").text = get_property(
            metadata, 'dcterms_issued')

        # serie
        dc_titles = etree.SubElement(mdprops, "dc_titles")
        dc_titles.set('strategy', 'OVERWRITE')
        etree.SubElement(dc_titles, "serie").text = get_array_property(
            metadata, 'dc_titles', 'serie')

        # Inhoud fields:
        # ==============
        # avo_beschrijving
        etree.SubElement(mdprops, "dcterms_abstract").text = get_property(
            metadata, 'dcterms_abstract')

        # Productie fields:
        # =================
        # dc_creators
        dc_creators = etree.SubElement(mdprops, "dc_creators")
        dc_creators.set('strategy', 'OVERWRITE')
        for entry in get_property(metadata, 'dc_creators'):
            etree.SubElement(
                dc_creators, entry['attribute']).text = entry['value']

        # dc_contributors
        dc_creators = etree.SubElement(mdprops, "dc_contributors")
        dc_creators.set('strategy', 'OVERWRITE')
        for entry in get_property(metadata, 'dc_contributors'):
            etree.SubElement(
                dc_creators, entry['attribute']).text = entry['value']

        # dc_publishers
        dc_creators = etree.SubElement(mdprops, "dc_publishers")
        dc_creators.set('strategy', 'OVERWRITE')
        for entry in get_property(metadata, 'dc_publishers'):
            etree.SubElement(
                dc_creators, entry['attribute']).text = entry['value']

        # Leerobject fields:
        # ==================
        # lom_type -> lom_learningresourcetype (Audio/Video)
        lom_type = etree.SubElement(mdprops, "lom_learningresourcetype")
        lom_type.set('strategy', 'OVERWRITE')
        for kw in get_property(metadata, 'lom_learningresourcetype'):
            etree.SubElement(lom_type, kw['attribute']).text = kw['value']

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

        # lom_onderwijsniveau is like keywords (onderwijsniveau)
        self.save_array_field(
            metadata, "lom_onderwijsniveau", mdprops, "Onderwijsniveau")

        # lom_onderwijsgraad is like keywords
        self.save_array_field(
            metadata, "lom_onderwijsgraad", mdprops, "Onderwijsgraad")

        # themas are like keywords (in future might be multiselect)
        self.save_array_field(metadata, "lom_thema", mdprops, "Thema")

        # vakken are multiselect but like keywords
        self.save_array_field(metadata, "lom_vak", mdprops, "Vak")

        # lom_legacy "false" indien vakken + themas ingevuld (logic in rmh_mapping.py)
        etree.SubElement(mdprops, "lom_legacy").text = get_property(
            metadata, 'lom_legacy')

        # trefwoorden / keywords are 'Sleutelwoord'
        self.save_array_field(metadata, "lom_keywords",
                              mdprops, "Sleutelwoord")

        xml_data = etree.tostring(
            root, pretty_print=True, encoding="UTF-8", xml_declaration=True
        ).decode()

        return xml_data
