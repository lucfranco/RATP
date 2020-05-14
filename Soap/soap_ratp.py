# SOAP RATP
# -*- coding: utf-8 -*-
import io
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import avro.schema
from avro.io import DatumReader, DatumWriter

# Path file .env / Class-----------------
path_origin = str(os.path.abspath(sys.argv[0]))[1:].split('/')
path_base = '/' + '/'.join(path_origin[0:(path_origin.index('RATP') + 1)])

path_env = path_base + '/.env'
load_dotenv(dotenv_path=path_env)

path_import = path_base + '/class_python'
sys.path.insert(0, path_import)

from class_soap_ratp import soapRATP
# Config Soap--------------------------------
soap_config = {
    'wsdl': os.getenv("wsdl_file")
}
soap_ratp = soapRATP(soap_config, path_base)
#---------------------------------------------

# Path Shema AVRO --------------------------------------------
path_shema = path_base + '/Soap/'  + 'stop_horaire.avsc'
schema = avro.schema.Parse(open(path_shema).read())

if __name__ == "__main__":
    missions = soap_ratp.stop_horaire('M13', 'Mairie de Saint-Ouen', 'A', [])

    SCHEMA = avro.schema.Parse(open(path_shema).read())
    writer = DatumWriter(SCHEMA)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)



    if writer.write(missions, encoder):
        raw_bytes = bytes_writer.getvalue()

    raise Exception('My error!')
'''

    writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema)
    writer.append(missions)
    writer.close()

    reader = DataFileReader(open("users.avro", "rb"), DatumReader())
    for user in reader:
        print(user)
    reader.close()
'''
