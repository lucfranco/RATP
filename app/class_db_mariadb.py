# Class Base Mariadb
import mysql.connector
from mysql.connector import errorcode


class gestionMARIADB:
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
            self.mariadb.set_charset_collation('utf8', 'utf8')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("mariadb OK !!")

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
        request = ("SELECT tr.route_id, tr.trip_id, s_tr.stop_id, s_tr.stop_sequence, sts.stop_name, sts.stop_desc, sts.stop_lat, sts.stop_lon, rtes.route_type, pct.file_name FROM trips AS tr LEFT JOIN stop_times AS s_tr ON tr.trip_id = s_tr.trip_id LEFT JOIN stops AS sts ON sts.stop_id = s_tr.stop_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id LEFT JOIN pictos AS pct ON rtes.route_short_name = pct.indices_commerciaux WHERE tr.route_id = " + str(var_ligne) + " GROUP BY stop_name ORDER BY tr.trip_id, s_tr.stop_sequence")
        print("0| " + request)
        list_station_lgn.execute(request)
        records = list_station_lgn.fetchall()
        self.nb_list_station_lgn = list_station_lgn.rowcount
        return records

    def infoStation(self, lat, lng):
        print('infoStation')
        infostation = self.mariadb.cursor()
        request = ("SELECT sts2.stop_id, sts2.stop_name, sts2.stop_desc, s_tr.stop_sequence, rtes.route_id, rtes.route_short_name, rtes.route_type FROM stops AS sts2 LEFT JOIN stop_times AS s_tr ON s_tr.stop_id = sts2.stop_id LEFT JOIN trips AS tr ON tr.trip_id = s_tr.trip_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id WHERE sts2.stop_name = (SELECT DISTINCT sts1.stop_name FROM stops AS sts1 WHERE sts1.stop_lat = " + str(lat) + " AND sts1.stop_lon = " + str(lng) + ") GROUP BY rtes.route_short_name")
        print("0| " + request)
        infostation.execute(request)
        records = infostation.fetchall()
        self.nb_infostation = infostation.rowcount
        return records





