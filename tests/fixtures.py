# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  tests/fixtures.py
#


def sidecar_v2_output():
    with open('tests/fixture_data/sidecar_v2.xml', 'r') as xmlfile:
        return xmlfile.read()


def sub_params():
    return {
        'pid': 'qsf7664p39',
        'subtitle_type': 'closed',
        'srt_file': 'qsf7664p39_closed.srt',
        'vtt_file': 'qsf7664p39.vtt',
        'xml_file': None,
        'xml_sidecar': None,
        'mh_response': None,
        'mam_data': '{}',
        'replace_existing': None,
        'transfer_method': 'ftp'
    }


def sub_meta():
    return {
        'mediaObjectId': '70af6a77d62e42dfa2c87b037458400f5c1943debc864537b24c31a56c38bbec',
        'externalId': 'qsf7664p39',
        'title': 'QAS 20.1 ingest test - Fietsstraten in centrum Gent',
        'description': 'QAS 20.1 ingest test',
        'date': '2019:05:28 09:34:30',
        'originalFileName': 'qsf7664p39.mp4',
        'type': 'Video',
        'authors': [],
        'lastModifiedDate': '2020-10-15T09:29:28Z',
        'archiveDate': '2020-06-19T10:56:45Z',
        'originalStatus': 'completed',
        'archiveStatus': 'on_disk',
        'workflow': 'borndigital',
        'mdProperties': [
            {'value': [{'value': 'qsvx05z57z',
                          'attribute': 'is_verwant_aan',
                          'dottedKey': None}
                       ],
             'attribute': 'dc_relations',
             'dottedKey': None},
            {'value': 'QAS 20.1 ingest test - Fietsstraten in centrum Gent',
             'attribute': 'dc_title',
             'dottedKey': None},
            {'value': 'OR-h41jm06',
             'attribute': 'Original_CP_ID',
             'dottedKey': None},
            {'value': 'qsf7664p39',
             'attribute': 'PID',
             'dottedKey': None},
            {'value': 'testbeeld',
             'attribute': 'CP',
             'dottedKey': None},
            {'value': '2019:05:28 09:34:30',
             'attribute': 'CreationDate',
             'dottedKey': None},
            {'value': 'AVS',
             'attribute': 'Original_CP',
             'dottedKey': None},
            {'value': 'OR-h41jm1d',
             'attribute': 'CP_id',
             'dottedKey': None},
            {'value': 'borndigital',
             'attribute': 'sp_name',
             'dottedKey': None}
        ]
    }
