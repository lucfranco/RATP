# SOAP RATP
# -*- coding: utf-8 -*-
import io
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import avro.schema
from avro.io import DatumReader, DatumWriter
from kafka import KafkaProducer

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

# Configuration Kafka-----------------
bootstrap_servers = [os.getenv("aws_kafka_ip") + ':9092']
topic_name = 'stops_real_time'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

if __name__ == "__main__":
    missions = soap_ratp.stop_horaire('M13', 'Mairie de Saint-Ouen', 'A', [])
    try:
        SCHEMA = avro.schema.Parse(open(path_shema).read())
        writer = DatumWriter(SCHEMA)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(missions, encoder)
        raw_bytes = bytes_writer.getvalue()
    except:
        print('erreur avro')
        try:
            topic_name = 'erreur_stops_real_time'
            ack = producer.send(topic_name, raw_bytes)
            metadata = ack.get()
        except Exception as e:
            print(e)
        else:
            print(metadata.topic)
            print(raw_bytes)
    else:
        print('ok avro')
        try:
            topic_name = 'stops_real_time'
            ack = producer.send(topic_name, raw_bytes)
            metadata = ack.get()
        except Exception as e:
            print(e)
        else:
            print(metadata.topic)
            print(raw_bytes)
'''


    writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema)
    writer.append(missions)
    writer.close()

    reader = DataFileReader(open("users.avro", "rb"), DatumReader())
    for user in reader:
        print(user)
    reader.close()
'''
