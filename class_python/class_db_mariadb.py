# Class Base Mariadb
import mysql.connector
from mysql.connector import errorcode


class gestionMARIADB:
    config = ''
    mariadb = ''
    nb_route_global = 0
    nb_route = 0
    nb_trip = 0
    nb_horaire = 0
    nb_stop = 0
    nb_list_stop = 0
    nb_list_Lignes = 0
    nb_list_station_lgn = 0
    nb_infostation = 0

    def __init__(self, config):
        self.config = config
        print(self.config)
        try:
            self.mariadb = mysql.connector.connect(**self.config)
            #self.mariadb.set_charset_collation('utf8', 'utf8')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("mariadb OK !!")

# For Cassandra
    def RouteGlobal(self, limit_debut = 0, limit_fin = 10):
        route_global = self.mariadb.cursor()
        request = ("SELECT tr.trip_id, rtes.route_id, rtes.route_short_name, rtes.route_long_name, rtes.route_type, type_name, tr.direction_id, IF (pic.file_name IS NULL, IF(type_name = 'METRO', 'M-flou0-160x160-bleu.svg', IF(type_name = 'BUS', 'B-flou0-160x160-bleu.svg', IF(type_name = 'RER','R-flou0-160x160-bleu.svg', IF(type_name = 'TRAM','T-flou0-160x160-bleu.svg', '')))), pic.file_name) AS file_name FROM routes AS rtes LEFT JOIN routes_types_names ON routes_types_names.type = rtes.route_type LEFT JOIN trips AS tr ON tr.route_id = rtes.route_id LEFT JOIN pictos AS pic ON pic.route_short_name = rtes.route_short_name ORDER BY route_short_name, rtes.route_id, tr.trip_id  LIMIT " + str(limit_debut) + "," + str(limit_fin))
        #print("0| " + request)
        route_global.execute(request)
        records = route_global.fetchall()

        records_lst = []
        for route in records:
            print(f'Mysql     | route : trip_id = {route[0]} route_id = {route[1]} short_name = {route[2]} type_name = {route[5]} direction = {route[6]}')
            list_trip_stop = self.trip_stop(route[0], route[1])
            route = route + list_trip_stop[0]
            records_lst.append(route)

        self.nb_route_global = route_global.rowcount
        return records_lst

    def trip_stop(self, trip_id, route_id):
        trip_stop = self.mariadb.cursor()
        request =("SELECT (SELECT GROUP_CONCAT(sts2.stop_id SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_id,(SELECT GROUP_CONCAT(sts2.stop_sequence SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_sequence,(SELECT GROUP_CONCAT(st2.stop_name SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id LEFT JOIN stops AS st2 ON st2.stop_id = sts2.stop_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_name,(SELECT GROUP_CONCAT(st2.stop_desc SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id LEFT JOIN stops AS st2 ON st2.stop_id = sts2.stop_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_desc,(SELECT GROUP_CONCAT(sts2.arrival_time SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS arrival_time,(SELECT GROUP_CONCAT(sts2.departure_time SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS departure_time,(SELECT GROUP_CONCAT(st2.stop_lat SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id LEFT JOIN stops AS st2 ON st2.stop_id = sts2.stop_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_lat,(SELECT GROUP_CONCAT(st2.stop_lon SEPARATOR ';') FROM stop_times AS sts2 LEFT JOIN trips AS tr2 ON tr2.trip_id = sts2.trip_id LEFT JOIN stops AS st2 ON st2.stop_id = sts2.stop_id WHERE sts2.trip_id = " +  str(trip_id) + " AND tr2.route_id = " +  str(route_id) + " ORDER BY sts2.stop_sequence) AS stop_lon")
        #print("1|- " + request)
        trip_stop.execute(request)
        records = trip_stop.fetchall()
        return records

# For FLASK
    def extractRouteGlobal(self):
        route_global = self.mariadb.cursor()
        request = ("SELECT DISTINCT LEFT(MD5(RAND()), 16) AS id, route_short_name FROM routes GROUP BY route_short_name ORDER BY route_short_name LIMIT 0,1")
        #request = ("SELECT DISTINCT @s:=@s+1 AS id, route_short_name FROM routes, (select @s:=0) as s GROUP BY route_short_name ORDER BY id LIMIT 0,3")
        print("1| " + request)
        route_global.execute(request)
        records = route_global.fetchall()
        self.nb_route_global = route_global.rowcount
        return records

    def listStop(self):
        print('listStop')
        #list_stop_dist = {}
        list_stop = self.mariadb.cursor()
        request = """SELECT LEFT(MD5(RAND()), 16) AS id, sts.stop_id, sts.stop_name, sts.stop_desc, sts.stop_lat, sts.stop_lon
                        FROM routes AS rtes
                        LEFT JOIN trips AS tr ON tr.route_id = rtes.route_id
                        LEFT JOIN stop_times AS s_tm ON s_tm.trip_id = tr.trip_id
                        LEFT JOIN stops as sts ON sts.stop_id = s_tm.stop_id
                        WHERE
                        rtes.route_short_name = '1' AND
                        rtes.route_id ='2204141' AND
                        (tr.trip_id = '24731412331078871' OR tr.trip_id = '24831412331078871' OR tr.trip_id = '24931412331078871' OR tr.trip_id = '25031412331078871')
                        GROUP BY sts.stop_id
                        ORDER BY rtes.route_short_name"""
        #request = "SELECT LEFT(MD5(RAND()), 16) AS id, stop_id, stop_name, stop_desc, stop_lat, stop_lon FROM stops"
        #request = "SELECT  LEFT(MD5(RAND()), 16) AS id, stops.stop_id, stops.stop_name, stops.stop_desc, stops.stop_lat, stops.stop_lon  FROM stop_times LEFT JOIN stops ON stops.stop_id = stop_times.stop_id WHERE trip_id ='24831412331078872'"
        print("0| " + request)
        list_stop.execute(request)
        records = list_stop.fetchall()
        self.nb_list_stop = list_stop.rowcount
        return records

    def listLignes(self):
        print('listLignes')
        list_Lignes = self.mariadb.cursor()
        request = '''SELECT route_id, route_short_name, route_long_name, route_type FROM routes'''
        print("0| " + request)
        list_Lignes.execute(request)
        records = list_Lignes.fetchall()
        self.nb_list_Lignes = list_Lignes.rowcount
        return records

    def listStationLigne(self, var_ligne):
        print('listStationLigne')
        list_station_lgn = self.mariadb.cursor()
        request = ("SELECT tr.route_id, tr.trip_id, s_tr.stop_id, s_tr.stop_sequence, sts.stop_name, sts.stop_desc, sts.stop_lat, sts.stop_lon, rtes.route_type, pct.file_name, rtes.route_short_name FROM trips AS tr LEFT JOIN stop_times AS s_tr ON tr.trip_id = s_tr.trip_id LEFT JOIN stops AS sts ON sts.stop_id = s_tr.stop_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id LEFT JOIN pictos AS pct ON rtes.route_short_name = pct.route_short_name WHERE tr.route_id = " + str(var_ligne) + " GROUP BY stop_name ORDER BY tr.trip_id, s_tr.stop_sequence")
        print("0| " + request)
        list_station_lgn.execute(request)
        records = list_station_lgn.fetchall()
        self.nb_list_station_lgn = list_station_lgn.rowcount
        return records

    def infoStation(self, lat, lng):
        print('infoStation')
        infostation = self.mariadb.cursor()
        request = ("SELECT sts2.stop_id, sts2.stop_name, sts2.stop_desc, s_tr.stop_sequence, rtes.route_id, rtes.route_short_name, rtes.route_type FROM stops AS sts2 LEFT JOIN stop_times AS s_tr ON s_tr.stop_id = sts2.stop_id LEFT JOIN trips AS tr ON tr.trip_id = s_tr.trip_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id WHERE sts2.stop_name = (SELECT DISTINCT sts1.stop_name FROM stops AS sts1 WHERE sts1.stop_lat = " + str(lat) + " AND sts1.stop_lon = " + str(lng) + ") AND s_tr.stop_sequence IS NOT NULL GROUP BY rtes.route_short_name")
        print("0| " + request)
        infostation.execute(request)
        records = infostation.fetchall()
        self.nb_infostation = infostation.rowcount
        return records





