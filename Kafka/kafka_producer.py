#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kafka import KafkaProducer

bootstrap_servers = ['15.236.9.122:9092']
topicName = 'test'

producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

ack = producer.send(topicName, b'Hello World!!!!!!!!')
metadata = ack.get()
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
