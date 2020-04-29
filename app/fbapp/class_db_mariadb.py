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
