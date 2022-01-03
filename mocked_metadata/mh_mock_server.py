from flask import Flask, render_template, request, send_from_directory
from flask import url_for

import sys
import csv
import json

app = Flask(__name__,
            static_url_path='', 
            static_folder='items',
            template_folder='templates')


# some example export:
# export MEDIAHAVEN_API = https://example-qas.meemoo.be/mediahaven-rest-api

# for the mocked server just change the export like so:
# export MEDIAHAVEN_API = http://localhost:5000
# and then run
# python mh_mock_server

# right now we expect this search=f"%2B(ExternalId:{pid})")
# look in app/services/mediahaven_api.py at the find_item_by_pid method

@app.route('/resources/media')
def send_json_file():
    print("in send json")
    search_qry = request.args.get('q')
    start_index = request.args.get('startIndex')
    nr_of_results = request.args.get('nrOfResults')
    print("q=", search_qry)
    print("start_index=", start_index)
    print("nr results=", nr_of_results)
    json_file = search_qry.split('ExternalId:')[1].split(')')[0].strip() + '.json'
    print("json_file to respond=", json_file)

    # return send_from_directory('items', json_file, as_attachment=True) 
    return send_from_directory('items', json_file) 

@app.route('/themas')
def themas_json():
    
    csvfile = open('themas/themas_grid_view.csv', 'r')
    reader = csv.reader(csvfile)
    themas = []
    rowcount = 0
    for row in reader:
        rowcount+=1
        if rowcount>1:
            title = row[0]
            desc = row[1]
            thema = {
                'thema': title,
                'beschrijving': desc
            }
            themas.append(thema)

    return json.dumps(themas)

@app.route('/vakken')
def vakken_json():
    data = open('themas/vakkenlijst_grid_view.csv', 'r').read()
    print("vakken=", data)



@app.route('/')
def home():
    return render_template('api.html')

if __name__ == '__main__':
    app.run()

