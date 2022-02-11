#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers and integrated
#           code from python-saml3 flask demo for SAML authorization
#
#           Thanks to 'suggest library' from Miel Vander Sande that will
#           be used to populate the dropdowns in the metadata
#           form's LOM sections. Suggest is part of the KnowledeGraph project.
#
#  app/redactietool.py
#
#   Micro service to supply the wanted mocked responses that come back from mediahaven and
#   from the suggest library. This is useful because the suggest lib currently supplies some outdated
#   data on qas with lorem ipsums. Also it's useful because it allows working faster offline without a vpn connection
#
#   example export:
#     export MEDIAHAVEN_API = https://example-qas.meemoo.be/mediahaven-rest-api
#
#   for the mocked server just change the export like so:
#     export MEDIAHAVEN_API = http://localhost:5000
#
# TODO: also most likely make the suggest library use an env var to differentiate between QAS/PRD
# then put this export here also as this microservice mocks both services.
#
#   Running the mock/dev server just do following:
#       cd mocked_metadata
#       ./start_mock_api.sh
#

from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin

import csv
import json
import urllib

app = Flask(
    __name__,
    static_url_path='',
    static_folder='items',
    template_folder='templates'
)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/resources/media')
@cross_origin()
def send_json_file():
    print("in send json")
    search_qry = request.args.get('q')
    start_index = request.args.get('startIndex')
    nr_of_results = request.args.get('nrOfResults')
    print("q=", search_qry)
    print("start_index=", start_index)
    print("nr results=", nr_of_results)
    json_file = search_qry.split('ExternalId:')[1].split(')')[
        0].strip() + '.json'
    print("json_file to respond=", json_file)

    # return send_from_directory('items', json_file, as_attachment=True)
    return send_from_directory('items', json_file)


def csv_to_suggest_response(csv_path, id_prefix, title_col=0, desc_col=1):
    csvfile = open(csv_path, 'r')
    reader = csv.reader(csvfile)
    items_array = []
    rowcount = 0
    for row in reader:
        rowcount += 1
        if rowcount > 1:
            title = row[0]
            desc = row[1]
            title_to_id = title.lower().replace(" ", "-")
            item_id = '{}{}'.format(
                id_prefix,
                urllib.parse.quote(title_to_id)
            )
            item = {
                'id': item_id,
                'label': title,
                'definition': desc
            }
            items_array.append(item)

    return items_array


@app.route('/onderwijsniveaus')
@cross_origin()
def onderwijsniveaus_json():
    return send_from_directory('suggest', 'onderwijsniveaus.json')


@app.route('/onderwijsgraden')
@cross_origin()
def onderwijsgraden_json():
    return send_from_directory('suggest', 'onderwijsgraden.json')


@app.route('/themas')
@cross_origin()
def themas_json():
    # themas als suggest lib ze goed teruggeeft gewoon 1 response opslaan en zo terug geven:
    # return send_from_directory('themas', 'themas_suggest_format.json')

    # use csv file from ticket DEV-1878
    themas = csv_to_suggest_response(
        'themas/themas_grid_view.csv',
        'https://data.meemoo.be/terms/ond/thema#'
    )
    return json.dumps(themas)


@app.route('/vakken')
@cross_origin()
def vakken_json():
    # vakken zodra de suggest library call volledig werkt, gewoon zo mocken:
    # return send_from_directory('vakken', 'vakkenlijst_suggest_format.json')

    # use csv file from ticket DEV-1878
    vakken = csv_to_suggest_response(
        'vakken/vakkenlijst_grid_view.csv',
        'https://data.meemoo.be/terms/ond/vak#'
    )
    return json.dumps(vakken)


@app.route('/vakken_suggest', methods=['POST'])
@cross_origin()
def get_vakken_suggesties():
    json_data = json.loads(request.data)
    print("graden=", json_data['graden'])
    print("themas=", json_data['themas'])
    return send_from_directory('vakken', 'suggested_vakken.json')


@app.route('/publicatie_status', methods=['GET'])
@cross_origin()
def mock_pub_status():
    # request.form.pid and request.form.department are passed
    return {
        'publish_item': True
    }


@app.route('/')
def api_docs():
    return render_template('api.html')


if __name__ == '__main__':
    app.run()
