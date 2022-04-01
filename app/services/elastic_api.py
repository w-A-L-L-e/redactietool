#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/services/elastic_api.py
#
#   Make calls in Elastic Search AVO for keyword searches
#

import os
import json
from requests import Session
from viaa.configuration import ConfigParser
from viaa.observability import logging

logger = logging.get_logger(__name__, config=ConfigParser())


class ElasticApi:
    # Voor v2 is endpoint hier /mediahaven-rest-api/v2/resources/
    # en met oauth ipv basic auth
    API_SERVER = os.environ.get(
        'ELASTIC_API',
        'https://elasticsearch-ingest-qas-avo.private.cloud.meemoo.be'
    )

    def __init__(self, session=None):
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def search_keyword(self, qry):
        search_url = f"{self.API_SERVER}/avo*/_search"
        headers = {
            'Content-Type': 'application/json',
        }

        search_data = {
            "_source": False,
            "suggest": {
                "keyword-suggest": {
                    "prefix": qry,
                    "completion": {
                        "field": "lom_keywords.suggest"
                    }
                }
            }
        }

        response = self.session.post(
            url=search_url,
            headers=headers,
            json=search_data
        )

        if response.status_code >= 400:
            logger.error(
                f"search_keyword(qry={qry}). Elastic search error={response.content}")
            return json.dumps([
                {
                    'text': f"Elastic Search ERROR: {response.status_code}",
                    '_id': 'error'
                }
            ])
        else:
            return json.dumps(
                response['suggest']['keyword-suggest']['options']
            )
