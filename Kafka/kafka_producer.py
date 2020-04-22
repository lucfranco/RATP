#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from kafka import KafkaProducer


if __name__ == "__main__":
    load_dotenv()

    # Configuration-----------------
    bootstrap_servers = [os.getenv("aws_kafka_name") + ':9092']
    topic_name = 'ratp-1'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
    print(f"Connexion : {bootstrap_servers}")

    try:
        ack = producer.send(topic_name, b'Hello World!!!!!!!!')
        metadata = ack.get()
    except Exception as e:
        print(e)
    else:
        print(metadata.topic)
        print(metadata.partition)



'''
import json
import time
import datetime
import urllib.request

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="15.236.9.122:9092")

date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
message = (f"message : mon message {date}")
print(message)
print(json.dumps(message).encode())
producer.send("test", json.dumps(message).encode())
'''
