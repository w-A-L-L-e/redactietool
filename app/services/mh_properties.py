#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/mh_properties.py
#
#   Setting, getting properties and array properties in v1 json of Mediahaven.
#

import json


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
