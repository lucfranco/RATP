# Class Base Cassandra
import time
from cassandra.cluster import Cluster
import json

class gestionCASSANDRA:
    config = ''
    cassandra = ''
    session = ''

    def __init__(self, config):
        self.config = config
        print(self.config)
        try:
            self.cassandra = Cluster([config["ip"]],port=9042)
            self.session = self.cassandra.connect(config["keyspace"],wait_for_all_pools=True)
            self.session.execute('USE ' + config["keyspace"])

        except:
            print('erreur de connexion cassandra')
        else:
            print("cassandra OK !!")

    def insertRoutes(self, routes):
        request = ''
        #print(routes)
        for route in routes:
            print(f'Cassandra | route : route_id = {route[0]} short_name = {route[1]} type_name = {route[4]} direction = {route[5]}')
            route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, stop_lat, stop_lon = route
            #print(route_id, '\n', route_short_name, '\n', route_long_name, '\n', route_type, '\n', type_name, '\n', direction_id, '\n', file_name, '\n', stop_id, '\n', stop_sequence, '\n', stop_name, '\n', stop_desc, '\n', stop_lat, '\n', stop_lon, '\n')
            # convertion en list
            stop_id = stop_id.split(';')
            stop_sequence = stop_sequence.split(';')
            stop_name = stop_name.split(';')
            stop_desc = stop_desc.split(';')
            stop_lat = stop_lat.split(';')
            stop_lon = stop_lon.split(';')

            cql = "INSERT INTO routes_trips (route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, stop_lat, stop_lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.session.execute(cql, (route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, stop_lat, stop_lon))

# For Flask
    def listLignes(self):
        print('listLignes Cassandra')
        startTime = time.time()
        records = []
        cql = "SELECT route_id, route_short_name, route_long_name, route_type, type_name FROM routes;"
        print("0| " + cql)

        listLignes = self.session.execute(cql)
        for ligne in listLignes:
            records.append(tuple(ligne))
        elapseTime = time.time()-startTime
        print(f'- listLignes : {elapseTime}')
        return records

    def listStationLigne(self, var_ligne):
        print('listStationLigne Cassandra')
        startTime = time.time()
        records = []
        cql = "SELECT * FROM routes_trips WHERE route_id = " + str(var_ligne) + ";"
        print("0| " + cql)

        listStationLigne = self.session.execute(cql)
        for lignestation in listStationLigne:
            records.append(tuple(lignestation))
        elapseTime = time.time()-startTime
        print(f'- listStationLigne : {elapseTime}')
        return records










'''
CREATE TABLE IF NOT EXISTS routes_trips (
route_id INT, route_short_name VARCHAR, route_long_name VARCHAR, route_type int, type_name VARCHAR, direction_id int, file_name VARCHAR, stop_id list<text>, stop_sequence list<text>, stop_name list<text>, stop_desc list<text>, stop_lat list<text>, stop_lon list<text>,
PRIMARY KEY ( route_id, route_short_name, type_name )
);
CREATE INDEX fk_route_short_name ON routes ( type_name );
CREATE INDEX fk_route_short_name ON routes ( route_short_name );
CREATE INDEX fk_route_id ON routes ( route_id );

CREATE TABLE IF NOT EXISTS routes (
route_id INT, route_short_name VARCHAR, route_long_name VARCHAR, route_type int, type_name VARCHAR, trip_id int, direction_id int, stops VARCHAR,
PRIMARY KEY ( route_id )
);
CREATE INDEX fk_routes_Short_Name ON routes ( route_short_name );
'''
