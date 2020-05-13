# Class Soap RATP
from zeep import Client


class soapRATP:
    def __init__(self, config, path_base):
        self.config = config
        self.path_base = path_base
        try:
            ratp_client = Client(self.path_base + '/Soap/' + self.config["wsdl"])
            self.line_t = ratp_client.get_type('ns0:Line')
            self.station_t = ratp_client.get_type('ns0:Station')
            self.direction_t = ratp_client.get_type('ns0:Direction')
            self.mission_t = ratp_client.get_type('ns0:Mission')
        except:
            print('erreur de connexion soap RATP')
        else:
            print("soap RATP OK !!")

    def stop_horaire(self, line, station, sens, stops):
        ratp_horaire = {}

        oline = self.line_t(id=line)
        ostation = self.station_t(line = oline, name=station)
        odirection = self.direction_t(sens = sens)
        missions = ratp_client.service.getMissionsNext(station=ostation, direction=odirection)
        ratp_horaire = {
            'line' : missions['argumentDirection']['line']['code'],
            'name' : missions['argumentDirection']['name'],
            'sens' : missions['argumentDirection']['sens']
        }
        return ratp_horaire
