#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


# Path file .env / import-----------------
import_path="/www/ubuntu_xenial/Formation/Data_University/__DS/certif/RATP"
load_dotenv(dotenv_path=import_path + '/.env')
sys.path.insert(0, import_path + '/class_python')

from class_db_mariadb import gestionMARIADB
from class_db_cassandra import gestionCASSANDRA
#from cassandra.cluster import Cluster


# Config MariaDB--------------------------------
mariadb_config = {
    'user': os.getenv("mariadb_user"),
    'passwd': os.getenv("mariadb_pass"),
    'host': os.getenv("mariadb_host"),
    'database': os.getenv("mariadb_base")
}
ratp_mysql = gestionMARIADB(mariadb_config)

# Config Cassandra--------------------------------
cassandra_config = {
    'ip': os.getenv("cassandra_ip"),
    'keyspace': os.getenv("cassandra_keyspace")
}
ratp_cassandra = gestionCASSANDRA(cassandra_config)



if __name__ == "__main__":
    routes = ratp_mysql.RouteGlobal(4801,100)
    ratp_cassandra.insertRoutes(routes)







    #cluster = Cluster([cassandra_config["ip"]],port=9042)
    #session = cluster.connect(cassandra_config["keyspace"],wait_for_all_pools=True)
    #session.execute('USE ' + cassandra_config["keyspace"])



    '''
    rows = session.execute('SELECT * FROM users')
    for row in rows:
        print(row)
        print(row.age,row.name,row.username)

    name = "Bill Gates"
    username = "qqwweerr"
    age = 76

    session.execute(
    """
    INSERT INTO users (name, username, age)
    VALUES (%s, %s, %s)
    """,
    (name, username, age)
    )
    '''
    #session.execute(f'INSERT INTO users (name, username, age) VALUES ('{name}', '{username}', '{age}')')























'''
import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


logging.basicConfig(level=logging.INFO)

server_config = {
                "host": "192.168.255.130",
                "port": "9042",
                "user": "",
                "password": "",
                "keySpace": "certif_test"
    }
keyspace = server_config['keySpace']
auth_provider = PlainTextAuthProvider(username=server_config['user'],password=server_config['password'])
node_ips = [server_config['host']]

#cluster = Cluster(contact_points=node_ips,
#        load_balancing_policy=None,
#        port=int(server_config['port']),
#        auth_provider=auth_provider,
#        protocol_version=3)

cluster = Cluster(contact_points=node_ips,
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
        port=int(server_config['port']),
        auth_provider=auth_provider,
        protocol_version=3)


session = cluster.connect()
session.set_keyspace(keyspace)



def cassandra_connection():
    """
    Connection object for Cassandra
    :return: session, cluster
    """
    cluster = Cluster(['192.168.255.130'], port=9042)
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS certif2_test
        WITH REPLICATION =
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
        """)
    return session, cluster


#if __name__ == "__main__":
#    cassandra_connection()
#    logging.info('Not callable')
'''
