# SOAP RATP
# -*- coding: utf-8 -*-
import io
import os
import sys
from dotenv import load_dotenv
import avro.schema
from avro.io import DatumReader, DatumWriter
from kafka import KafkaConsumer

# Path file .env / Class-----------------
path_origin = str(os.path.abspath(sys.argv[0]))[1:].split('/')
path_base = '/' + '/'.join(path_origin[0:(path_origin.index('RATP') + 1)])

path_env = path_base + '/.env'
load_dotenv(dotenv_path=path_env)

path_import = path_base + '/class_python'
sys.path.insert(0, path_import)

from class_soap_ratp import soapRATP
from class_db_mariadb import gestionMARIADB

# Config MariaDB--------------------------------
mariadb_config = {
    'user': os.getenv("mariadb_user"),
    'passwd': os.getenv("mariadb_pass"),
    'host': os.getenv("mariadb_host"),
    'database': os.getenv("mariadb_base")
}
ratp_mysql = gestionMARIADB(mariadb_config)


# Config Soap--------------------------------
soap_config = {
    'wsdl': os.getenv("wsdl_file")
}
soap_ratp = soapRATP(soap_config, path_base)
#---------------------------------------------

# Path Shema AVRO --------------------------------------------
path_shema = path_base + '/Soap/'  + 'stop_horaire.avsc'
SCHEMA = avro.schema.Parse(open(path_shema).read())

# Configuration Kafka-----------------
bootstrap_servers = [os.getenv("aws_kafka_ip") + ':9092']


if __name__ == "__main__":
    load_dotenv()

    # Configuration-----------------
    bootstrap_servers = [os.getenv("aws_kafka_ip") + ':9092']
    topic_name = 'stops_real_time'
    consumer = KafkaConsumer (
        topic_name,
        group_id = 'group1',
        bootstrap_servers = bootstrap_servers,
        auto_offset_reset = 'earliest')
    print(f"Connexion : {bootstrap_servers}")

    try:
        for message in consumer:
            bytes_reader = io.BytesIO(message.value)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(SCHEMA)
            stop = reader.read(decoder)
            ratp_mysql.stop_temps_reel(stop)
            print(stop)
    except KeyboardInterrupt:
        sys.exit()
