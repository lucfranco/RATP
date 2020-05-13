# Class Soap RATP
from zeep import Client


class soapRATP:
    def __init__(self, config):
        self.config = config
        print(self.config)
        try:
            ratp_client = Client(config["wsdl_file"])

            line_t = ratp_client.get_type('ns0:Line')
            station_t = ratp_client.get_type('ns0:Station')
            direction_t = ratp_client.get_type('ns0:Direction')
            mission_t = ratp_client.get_type('ns0:Mission')
        except:
            print('erreur de connexion soap RATP')
        else:
            print("soap RATP OK !!")
