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

    def __init__(self, config):
        self.config = config
        print(self.config)
        try:
            self.mariadb = mysql.connector.connect(**self.config)
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

    def extractRoute(self, route_global):
        route = self.mariadb.cursor()
        request = ("SELECT LEFT(MD5(RAND()), 16) AS id, route_id, route_long_name, route_type FROM routes WHERE route_short_name = '" + route_global + "' LIMIT 0,1")
        print("2|- " + request)
        route.execute(request)
        records = route.fetchall()
        self.nb_route = route.rowcount
        return records

    def extractTrip(self, route):
        trip = self.mariadb.cursor()
        request = ("SELECT LEFT(MD5(RAND()), 16) AS id, trip_id, trip_short_name, direction_id FROM trips WHERE route_id ='" + str(route) + "' LIMIT 0,4")
        print("3|-- " + request)
        trip.execute(request)
        records = trip.fetchall()
        self.nb_trip = trip.rowcount
        return records

    def extractHoraire(self,trip):
        horaire = self.mariadb.cursor()
        request = ("SELECT LEFT(MD5(RAND()), 16) AS id, stop_id, arrival_time, departure_time, stop_sequence FROM stop_times WHERE trip_id ='" + str(trip) + "'")
        print("4|--- " + request)
        horaire.execute(request)
        records = horaire.fetchall()
        self.nb_horaire = horaire.rowcount
        return records

    def extractStop(self, stop_id):
        print('extractStop', stop_id)
        stop = self.mariadb.cursor()
        request = ("SELECT LEFT(MD5(RAND()), 16) AS id, stop_id, stop_name, stop_desc, stop_lat, stop_lon FROM stops WHERE stop_id ='" + str(stop_id) + "'")
        print("5|---- " + request)
        stop.execute(request)
        records = stop.fetchall()
        self.nb_stop = stop.rowcount
        return records

    def listStop(self):
        print('listtStop')
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

    def test(self, pipo):
        self.pipo = pipo
        print('test' + self.pipo)

    def extractClose(self):
        self.mariadb.close()
        print("mariadb close !!")

