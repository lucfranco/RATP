import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, json, jsonify
#import mysql.connector

# Path file .env-----------------
path_origin = str(sys.argv[0])[1:].split('/')
print("path_origin = ", path_origin, type(path_origin))
path_base = '/' + '/'.join(path_origin[0:(path_origin.index('RATP')+1)])
print("path_base = ", path_base, type(path_base))


path_env = path_base + '/.env'
print("path_env = ", path_env, type(path_env))
load_dotenv(dotenv_path=path_env)

path_import = path_base + '/class_python'
print("path_import = ", path_import, type(path_import))
sys.path.insert(0, path_import)

from class_db_mariadb import gestionMARIADB
from class_db_cassandra import gestionCASSANDRA
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
    titre = 'Configuration'
    list_env = ''
    for i, j in os.environ.items():
        list_env += 'Var: ' + str(i) + ' Value: ' + str(j) + '<br/>'
    return render_template('template_01.html', titre=titre, list_env=os.environ.items())

@app.route('/mysqlshow')
def mysqlshow():
    ratp = gestionMARIADB(mariadb_config)
    test = ratp.test("pipo") #ratp.extractRouteGlobal()
    return test

@app.route('/stations.json', methods=['GET'])
def station_json():
    return render_template('json/stations.json')

@app.route('/stations_ligne_mysql/<int:ligne>/', methods=['GET'])
def stations_ligne(ligne):
    list_stations_dict = dict()
    list_stations_dict['stations'] = list()
    ratp = gestionMARIADB(mariadb_config)
    list_stations_ligne = ratp.listStationLigne(ligne)
    print(list_stations_ligne)
    list_stations_dict['LIGNE_SHORT_NAME'] = list_stations_ligne[0][10]
    list_stations_dict['LIGNE_ID'] = list_stations_ligne[0][0]
    sequence = 1
    for station in list_stations_ligne:
        if sequence <= station[3]:
            list_stations_dict['stations'].append({
                'ID': station[2],
                'SEQUENCE': station[3],
                'NAME': station[4],
                'DESCRIPTION': station[5],
                'COLOR': station[8],
                'PICTO': station[9],
                "geometry": {
                    "coordinates":[station[7], station[6]]
                }
            })
            sequence = station[3]
        else:
            pass

    return list_stations_dict

@app.route('/station_mysql/<int:ligne>/<lat>/<lng>/', methods=['GET'])
def station(ligne, lat, lng):
    station_dict = dict()
    station_dict['station'] = list()
    list_ligne = list()
    route = list()

    ratp = gestionMARIADB(mariadb_config)
    station = ratp.infoStation(lat, lng)

    # recuperation de l'index de la station selectionnee
    for index, item in enumerate(station):
        print(index,item)
        if (item[4] == ligne):
            idx_ok = index

    # generation du json de la station + les lignes ou cette station existe
    for st_element in station:
        list_ligne.append(st_element[5])
        route.append(st_element[4])

    station_dict['station'].append({
            'ID': station[idx_ok][0],
            'NAME': station[idx_ok][1],
            'DESCRIPTION': station[idx_ok][2],
            'SEQUENCE': station[idx_ok][3],
            'ROUTE_ID': route,
            'ROUTE_TYPE': station[idx_ok][6],
            'ROUTE_SHORT_NAME': list_ligne
    })

    return station_dict


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

@app.route('/test2')
def test2():
    return render_template('test2.html')

@app.route('/fullscreen')
def fullscreen():
    return render_template('fullscreen.html')

@app.route('/carte')
def carte():
    titre = 'Carte RATP'
    ratp = gestionMARIADB(mariadb_config)
    return render_template('template_01.html', titre=titre, list_lignes=ratp.listLignes())


if __name__ == "__main__":
    #print(mariadb_config)

    app.run()

