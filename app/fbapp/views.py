import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, json, jsonify
from class_db_mariadb import gestionMARIADB
#import mysql.connector

# Path file .env-----------------
env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

# Config MariaDB--------------------------------
mariadb_config = {
    'user': os.getenv("mariadb_user"),
    'passwd': os.getenv("mariadb_pass"),
    'host': os.getenv("mariadb_host"),
    'database': os.getenv("mariadb_base")
}


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/config')
def config():
    list_env = ''
    for i, j in os.environ.items():
        list_env += 'Var: ' + str(i) + ' Value: ' + str(j) + '<br/>'
    return list_env

@app.route('/mysqlshow')
def mysqlshow():
    ratp = gestionMARIADB(mariadb_config)
    test = ratp.test("pipo") #ratp.extractRouteGlobal()
    return test

@app.route('/stations.json', methods=['GET'])
def station():
    return render_template('json/stations.json')

@app.route('/lines.json', methods=['GET'])
def line():
    return render_template('json/lines.json')
'''
def station():
    list_stop_dict = dict()
    #list_stop_dict["type"] = "FeatureCollection"
    list_stop_dict['features'] = list()
    ratp = gestionMARIADB(mariadb_config)
    listStop = ratp.listStop()
    for el in listStop:
        stop = {
            "type":"Feature",
            "properties":{
            'ID': el[1],
            'STATION': el[2],
            'DESCRIPTION': el[3]
            },
            "geometry":{
                "type":"Point",
                "coordinates":[el[5], el[4]]
            }
        }

        list_stop_dict['features'].append(stop)

    #data = {'nom': 'Wayne', 'prenom': 'Bruce'}
    #response = app.response_class(
    #     response=json.dumps(listStop),
    #     mimetype='application/json'
    # )
    # return response
    list_stop_dict["type"] = "FeatureCollection"
    return list_stop_dict #json.dumps(list_stop_dict) #jsonify({list_stop_dist}) # Returns HTTP Response with {"hello": "world"}
'''
@app.route('/ratp')
def ratp():
    return render_template('ratp.html')

@app.route('/ratp2')
def ratp2():
    return render_template('ratp2.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/test2')
def test2():
    return render_template('test2.html')

@app.route('/fullscreen')
def fullscreen():
    return render_template('fullscreen.html')


if __name__ == "__main__":
    #print(mariadb_config)

    app.run()

