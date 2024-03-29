# Class Soap RATP
from zeep import Client


class soapRATP:
    def __init__(self, config, path_base):
        self.config = config
        self.path_base = path_base
        try:
            self.ratp_client = Client(self.path_base + '/Soap/' + self.config["wsdl"])
            self.line_t = self.ratp_client.get_type('ns0:Line')
            self.station_t = self.ratp_client.get_type('ns0:Station')
            self.direction_t = self.ratp_client.get_type('ns0:Direction')
            self.mission_t = self.ratp_client.get_type('ns0:Mission')
        except:
            print('erreur de connexion soap RATP')
        else:
            print("soap RATP OK !!")

    def stop_horaire(self, line, station, sens, stops):
        ratp_horaire = {}

        oline = self.line_t(id=line)
        ostation = self.station_t(line = oline, name=station)
        odirection = self.direction_t(sens = sens)
        missions = self.ratp_client.service.getMissionsNext(station=ostation, direction=odirection)
        ratp_horaire = {
            'line' : missions['argumentDirection']['line']['code'],
            'name' : missions['argumentDirection']['name'],
            'sens' : missions['argumentDirection']['sens']
        }

        ratp_horaire['stationA_id'] = missions['argumentStation']['geoPointA']['id']
        ratp_horaire['stationA_name'] = missions['argumentStation']['geoPointA']['name']
        ratp_horaire['stationR_id'] = missions['argumentStation']['geoPointR']['id']
        ratp_horaire['stationR_name'] = missions['argumentStation']['geoPointR']['name']
        # info temps reel-------------------------
        stationsDates = []
        stationsMessages = []

        for mission in missions['missions']:
          stationsDates.append(mission['stationsDates'][0])
          stationsMessages.append(mission['stationsMessages'][0])

        ratp_horaire['stationsDates'] = stationsDates
        ratp_horaire['stationsMessages'] = stationsMessages

        print(ratp_horaire)
        return ratp_horaire
