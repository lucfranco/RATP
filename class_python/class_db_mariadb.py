# Class Base Mariadb
import time
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
    nb_perf = 0

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
        print(f'limit_debut = {limit_debut} limit_fin = {limit_fin}')
        route_global = self.mariadb.cursor()
        request = ("SELECT rtes.route_id, rtes.route_short_name, rtes.route_long_name, rtes.route_type, type_name, (SELECT tr.direction_id FROM trips AS tr WHERE tr.route_id = rtes.route_id LIMIT 0,1) AS nb_trips, IF (pct.file_name IS NULL, IF(type_name = 'METRO', 'M-flou0-160x160-bleu.svg', IF(type_name = 'BUS', 'B-flou0-160x160-bleu.svg', IF(type_name = 'RER','R-flou0-160x160-bleu.svg', IF(type_name = 'TRAM','T-flou0-160x160-bleu.svg', '')))), pct.file_name) AS file_name, (SELECT GROUP_CONCAT(DISTINCT sts2.stop_id SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_id, (SELECT GROUP_CONCAT(DISTINCT str2.stop_sequence SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_sequence, (SELECT GROUP_CONCAT(DISTINCT sts2.stop_name SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_name, (SELECT GROUP_CONCAT(DISTINCT sts2.stop_desc SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_desc, (SELECT GROUP_CONCAT(DISTINCT sts2.stop_lat SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_lat, (SELECT GROUP_CONCAT(DISTINCT sts2.stop_lon SEPARATOR ';') AS stop_id FROM trips AS tr2 LEFT JOIN stop_times AS str2 ON tr2.trip_id = str2.trip_id LEFT JOIN stops AS sts2 ON sts2.stop_id = str2.stop_id LEFT JOIN routes AS rtes2 ON rtes2.route_id = tr2.route_id WHERE tr2.route_id = rtes.route_id ORDER BY str2.stop_sequence) AS stop_lon FROM routes AS rtes LEFT JOIN routes_types_names ON routes_types_names.type = rtes.route_type LEFT JOIN pictos AS pct ON pct.route_short_name = rtes.route_short_name  LIMIT " + str(limit_debut) + "," + str(limit_fin))
        #print("0| " + request)
        route_global.execute(request)
        records = route_global.fetchall()
        self.nb_route_global = route_global.rowcount
        for route in records:
            print(f'Mysql     | route : route_id = {route[0]} short_name = {route[1]} type_name = {route[4]} direction = {route[5]}')
        return records

# PERF
    def perf(self, base, requete, perf):
        perf = self.mariadb.cursor()
        request = ("INSERT INTO perf_RATP (base, requete, perf) VALUES ('" + base + "', '" + requete + "', '" + str(perf) + "')")
        print("1| " + request)
        perf.execute(request)
        records = perf.fetchall()
        self.nb_perf = perf.rowcount
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
        print('- listLignes | Mysql')
        startTime = time.time()
        list_Lignes = self.mariadb.cursor()
        request = ("SELECT route_id, route_short_name, route_long_name, route_type FROM routes")
        print("0| " + request)
        list_Lignes.execute(request)
        records = list_Lignes.fetchall()
        self.nb_list_Lignes = list_Lignes.rowcount
        elapseTime = time.time()-startTime
        self.perf('Mysql', 'listLignes', elapseTime)
        print(f'- listLignes : {elapseTime}')
        return records

    def listStationLigne(self, var_ligne):
        print('listStationLigne | Mysql')
        startTime = time.time()
        list_station_lgn = self.mariadb.cursor()
        request = ("SELECT tr.route_id, tr.trip_id, s_tr.stop_id, s_tr.stop_sequence, sts.stop_name, sts.stop_desc, sts.stop_lat, sts.stop_lon, rtes.route_type, rtes.route_short_name, IF (pct.file_name IS NULL, IF(rtes.route_type = 1, 'M-flou0-160x160-bleu.svg', IF(rtes.route_type = 3, 'B-flou0-160x160-bleu.svg', IF(rtes.route_type = 2,'R-flou0-160x160-bleu.svg', IF(rtes.route_type = 0,'T-flou0-160x160-bleu.svg', '')))), pct.file_name) AS file_name FROM trips AS tr LEFT JOIN stop_times AS s_tr ON tr.trip_id = s_tr.trip_id LEFT JOIN stops AS sts ON sts.stop_id = s_tr.stop_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id LEFT JOIN pictos AS pct ON rtes.route_short_name = pct.route_short_name WHERE tr.route_id = " + str(var_ligne) + " GROUP BY stop_name ORDER BY tr.trip_id, s_tr.stop_sequence")
        print("0| " + request)
        list_station_lgn.execute(request)
        records = list_station_lgn.fetchall()
        self.nb_list_station_lgn = list_station_lgn.rowcount
        elapseTime = time.time()-startTime
        print(f'- listStationLigne : {elapseTime}')
        return records

    def infoStation(self, station_id):
        print('infoStation')
        infostation = self.mariadb.cursor()
        request = ("SELECT sts2.stop_id, sts2.stop_name, sts2.stop_desc, str2.stop_sequence, rtes.route_id, rtes.route_short_name, rtes.route_type FROM stops AS sts2 LEFT JOIN stop_times AS str2 ON str2.stop_id = sts2.stop_id LEFT JOIN trips AS tr ON tr.trip_id = str2.trip_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id WHERE sts2.stop_name LIKE (SELECT DISTINCT sts1.stop_name FROM stops AS sts1 WHERE sts1.stop_id = " + str(station_id) + ") GROUP BY tr.route_id;")
        print("0| " + request)
        infostation.execute(request)
        records = infostation.fetchall()
        self.nb_infostation = infostation.rowcount
        return records


# KAFKA stop_temps reel------------------------------------------------------
    def stop_temps_reel(self, message_kafka):
        infostation = self.mariadb.cursor()
        print('stop_temps_reel')
        #print(message_kafka)
        var_stationsDates_1 = ''
        var_stationsDates_2 = ''
        var_stationsDates_3 = ''
        var_stationsDates_4 = ''
        stationsMessages_1 = ''
        stationsMessages_2 = ''
        stationsMessages_3 = ''
        stationsMessages_4 = ''
        long_stationsDates = len(message_kafka['stationsDates'])
        if long_stationsDates >= 3:
            var_stationsDates_1 = message_kafka['stationsDates'][0][8:10]+":"+message_kafka['stationsDates'][0][10:]
            var_stationsDates_2 = message_kafka['stationsDates'][1][8:10]+":"+message_kafka['stationsDates'][1][10:]
            var_stationsDates_3 = message_kafka['stationsDates'][2][8:10]+":"+message_kafka['stationsDates'][2][10:]
            var_stationsDates_4 = ''
        elif long_stationsDates == 2:
            var_stationsDates_1 = message_kafka['stationsDates'][0][8:10]+":"+message_kafka['stationsDates'][0][10:]
            var_stationsDates_2 = message_kafka['stationsDates'][1][8:10]+":"+message_kafka['stationsDates'][1][10:]
            var_stationsDates_3 = ''
            var_stationsDates_4 = ''
        elif long_stationsDates == 1:
            var_stationsDates_1 = message_kafka['stationsDates'][0][8:10]+":"+message_kafka['stationsDates'][0][10:]
            var_stationsDates_2 = ''
            var_stationsDates_3 = ''
            var_stationsDates_4 = ''
        elif long_stationsDates == 0:
            var_stationsDates_1 = ''
            var_stationsDates_2 = ''
            var_stationsDates_3 = ''
            var_stationsDates_4 = ''

        long_stationsMessages = len(message_kafka['stationsMessages'])
        if long_stationsMessages >= 3:
            stationsMessages_1 = message_kafka['stationsMessages'][0]
            stationsMessages_2 = message_kafka['stationsMessages'][1]
            stationsMessages_3 = message_kafka['stationsMessages'][2]
            stationsMessages_4 = ''
        if long_stationsMessages == 2:
            stationsMessages_1 = message_kafka['stationsMessages'][0]
            stationsMessages_2 = message_kafka['stationsMessages'][1]
            stationsMessages_3 = ''
            stationsMessages_4 = ''
        if long_stationsMessages == 1:
            stationsMessages_1 = message_kafka['stationsMessages'][0]
            stationsMessages_2 = ''
            stationsMessages_3 = ''
            stationsMessages_4 = ''
        if long_stationsMessages == 0:
            stationsMessages_1 = ''
            stationsMessages_2 = ''
            stationsMessages_3 = ''
            stationsMessages_4 = ''

        print(long_stationsDates, var_stationsDates_1,var_stationsDates_2,var_stationsDates_3,var_stationsDates_4)
        print(stationsMessages_1, stationsMessages_2, stationsMessages_3, stationsMessages_4)

        message_kafka['stationA_name'] = self.addslashes(message_kafka['stationA_name'])
        message_kafka['stationR_name'] = self.addslashes(message_kafka['stationR_name'])


        request = ("INSERT INTO stop_temps_reel (route_id, route_name, sens, Date_temps_reel, stationsDates1, stationsDates2, stationsDates3, stationsDates4, stationsMessages1, stationsMessages2, stationsMessages3, stationsMessages4, stationA_id, stationA_name, stationR_id, stationR_name) VALUE ('" + message_kafka['line'] + "', '" + message_kafka['name'] + "', '" +  message_kafka['sens'] + "', NOW(), '" + var_stationsDates_1 + "', '" +  var_stationsDates_2 + "', '" +  var_stationsDates_3 + "', '" +  var_stationsDates_4+ "', '" +  stationsMessages_1 + "', '" +  stationsMessages_2 + "', '" +  stationsMessages_3 + "', '" +  stationsMessages_4+ "', '" +  message_kafka['stationA_id']+ "', '" +  message_kafka['stationA_name'] + "', '" +  message_kafka['stationR_id'] + "', '" +  message_kafka['stationA_name'] + "')")
        #request = ('INSERT INTO stop_temps_reel (route_id, route_name, sens, Date_temps_reel, stationsDates1, stationsDates2, stationsDates3, stationsDates4, stationsMessages1, stationsMessages2, stationsMessages3, stationsMessages4, stationA_id, stationA_name, stationR_id, stationR_name) VALUE ("' + message_kafka['line'] + '", '" + message_kafka['name'].replace("'","\'") + "', '" +  message_kafka['sens'] + "', NOW(), '" + var_stationsDates_1 + "', '" +  var_stationsDates_2 + "', '" +  var_stationsDates_3 + "', '" +  var_stationsDates_4+ "', '" +  stationsMessages_1 + "', '" +  stationsMessages_2 + "', '" +  stationsMessages_3 + "', '" +  stationsMessages_4+ "', '" +  message_kafka['stationA_id']+ "', '" +  message_kafka['stationA_name'] + "', '" +  message_kafka['stationR_id'] + "', '" +  message_kafka['stationA_name'] + "')')
        print("0| " + request)
        infostation.execute(request)
        self.mariadb.commit()
        self.nb_infostation = infostation.rowcount





#    def infoStation(self, lat, lng):
#        print('infoStation')
#        infostation = self.mariadb.cursor()
#        request = ("SELECT sts2.stop_id, sts2.stop_name, sts2.stop_desc, s_tr.stop_sequence, rtes.route_id, rtes.route_short_name, rtes.route_type FROM stops AS sts2 LEFT JOIN stop_times AS s_tr ON s_tr.stop_id = sts2.stop_id LEFT JOIN trips AS tr ON tr.trip_id = s_tr.trip_id LEFT JOIN routes AS rtes ON rtes.route_id = tr.route_id WHERE sts2.stop_name = (SELECT DISTINCT sts1.stop_name FROM stops AS sts1 WHERE sts1.stop_lat = " + str(lat) + " AND sts1.stop_lon = " + str(lng) + ") AND s_tr.stop_sequence IS NOT NULL GROUP BY rtes.route_id")
#        print("0| " + request)
#        infostation.execute(request)
#        records = infostation.fetchall()
#        self.nb_infostation = infostation.rowcount
#        return records





