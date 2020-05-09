# Class Base Cassandra
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
            print(f'Cassandra | route : trip_id = {route[0]} route_id = {route[1]} short_name = {route[2]} type_name = {route[5]} direction = {route[6]}')
            trip_id, route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, arrival_time, departure_time, stop_lat, stop_lon = route
            #print(trip_id, '\n', route_id, '\n', route_short_name, '\n', route_long_name, '\n', route_type, '\n', type_name, '\n', direction_id, '\n', file_name, '\n', stop_id, '\n', stop_sequence, '\n', stop_name, '\n', stop_desc, '\n', arrival_time, '\n', departure_time, '\n', stop_lat, '\n', stop_lon, '\n')
            # convertion en list
            stop_id = stop_id.split(';')
            stop_sequence = stop_sequence.split(';')
            stop_name = stop_name.split(';')
            stop_desc = stop_desc.split(';')
            arrival_time = arrival_time.split(';')
            departure_time = departure_time.split(';')
            stop_lat = stop_lat.split(';')
            stop_lon = stop_lon.split(';')

            cql = "INSERT INTO routes (trip_id, route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, arrival_time, departure_time, stop_lat, stop_lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #self.session.execute(cql, (str(route[0]), int(route[1]), str(route[2]), str(route[3]), int(route[4]), str(route[5]), int(route[6]), str(route[7]), str(route[8])))
            self.session.execute(cql, (trip_id, route_id, route_short_name, route_long_name, route_type, type_name, direction_id, file_name, stop_id, stop_sequence, stop_name, stop_desc, arrival_time, departure_time, stop_lat, stop_lon))

# For Flask
    def listLignes(self):
        print('listLignes CASSANDRA')
        listLignes = []
        cql = "SELECT route_id, route_short_name, route_long_name, route_type FROM list_routes"
        print("0| " + cql)
        #self.session.row_factory = named_tuple_factory
        records = self.session.execute(cql)
        print(records[0])
        for ligne in records:
            listLignes.append(ligne[0], ligne[1], ligne[2], ligne[3])
        print(listLignes)
        return records









'''
CREATE TABLE IF NOT EXISTS routes (
trip_id VARCHAR, route_short_name VARCHAR, route_long_name VARCHAR, route_type int, type_name VARCHAR, route_id INT, direction_id int, file_name VARCHAR, stop_id list<text>, stop_sequence list<text>, stop_name list<text>, stop_desc list<text>, arrival_time list<text>, departure_time list<text>, stop_lat list<text>, stop_lon list<text>,
PRIMARY KEY ( trip_id )
);
CREATE INDEX fk_route_short_name ON routes ( route_short_name );
CREATE INDEX fk_route_id ON routes ( route_id );

CREATE TABLE IF NOT EXISTS routes (
route_id INT, route_short_name VARCHAR, route_long_name VARCHAR, route_type int, type_name VARCHAR, trip_id int, direction_id int, stops VARCHAR,
PRIMARY KEY ( route_id )
);
CREATE INDEX fk_routes_Short_Name ON routes ( route_short_name );
'''
