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

import json
import os
from lxml import etree


def get_property(mam_data, attribute):
    props = mam_data.get('mdProperties', [])
    result = ''
    for prop in props:
        if prop.get('attribute') == attribute:
            return prop.get('value', '')

    return result


def set_property(mam_data, propkey, propvalue):
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


def get_md_array(mam_data, attribute, legacy_fallback=False):
    props = mam_data.get('mdProperties', [])
    for prop in props:
        if prop.get('attribute') == attribute:
            return prop.get('value', [])

    if legacy_fallback:
        return {'show_legacy': True}
    else:
        return []


def get_array_property(mam_data, attribute, array_attribute):
    props = mam_data.get('mdProperties', [])
    result = ''
    for prop in props:
        if prop.get('attribute') == attribute:
            array_values = prop.get('value', '')
            for att in array_values:
                if att.get('attribute') == array_attribute:
                    return att.get('value', '')

    return result


def set_array_property(mam_data, attribute, array_attribute, propvalue):
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


def set_json_array_property(mam_data, propkey, jkey, jvalue, prop_name="multiselect"):
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


def sidecar_root():
    MH_NS = 'https://zeticon.mediahaven.com/metadata/20.3/mh/'
    MHS_NS = 'https://zeticon.mediahaven.com/metadata/20.3/mhs/'
    XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'  # version="20.3"

    schema_loc = etree.QName(
        "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
    zeticon_mhs = 'https://zeticon.mediahaven.com/metadata/20.3/mhs/'
    zeticon_mhs_xsd = 'https://zeticon.mediahaven.com/metadata/20.3/mhs.xsd'
    zeticon_mh = 'https://zeticon.mediahaven.com/metadata/20.3/mh/'
    zeticon_mh_xsd = 'https://zeticon.mediahaven.com/metadata/20.3/mh.xsd'
    XSI_LOC = f"{zeticon_mhs} {zeticon_mhs_xsd} {zeticon_mh} {zeticon_mh_xsd}"

    NSMAP = {
        'mh': MH_NS,
        'mhs': MHS_NS,
        'xsi': XSI_NS
    }

    root = etree.Element(
        "{%s}Sidecar" % MHS_NS,
        {
            'version': '20.3',
            schema_loc: XSI_LOC
        },
        nsmap=NSMAP
    )

    return root, MH_NS, MHS_NS, XSI_NS


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

        # lom_legacy "false" indien vakken + themas ingevuld
        etree.SubElement(mdprops, "lom_legacy").text = get_property(
            metadata, 'lom_legacy')

        # trefwoorden / keywords are 'Sleutelwoord'
        self.save_array_field(metadata, "lom_keywords",
                              mdprops, "Sleutelwoord")

        xml_data = etree.tostring(
            root, pretty_print=True, encoding="UTF-8", xml_declaration=True
        ).decode()

        return xml_data
