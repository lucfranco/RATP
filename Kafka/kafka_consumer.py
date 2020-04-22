#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from kafka import KafkaConsumer

if __name__ == "__main__":
    load_dotenv()

    # Configuration-----------------
    bootstrap_servers = [os.getenv("aws_kafka_name") + ':9092']
    topic_name = 'ratp-1'
    consumer = KafkaConsumer (
        topic_name,
        group_id = 'group1',
        bootstrap_servers = bootstrap_servers,
        auto_offset_reset = 'earliest')
    print(f"Connexion : {bootstrap_servers}")

    try:
        for message in consumer:
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
    except KeyboardInterrupt:
        sys.exit()


'''
from kafka import KafkaConsumer
from kafka.version import __version__


#consumer = KafkaConsumer("position_station", bootstrap_servers="15.236.9.122:9092", group_id="GRP-position-station")
consumer = KafkaConsumer(bootstrap_servers="15.236.9.122:9092")
print(__version__)
print(consumer.topics())


#for message in consumer:
#    print(message)
#    #print(json.loads(message.value.decode("utf-8")))




# from kafka import KafkaConsumer
#
# # To consume latest messages and auto-commit offsets
# consumer = KafkaConsumer('position_station',
#                          group_id='GRP-position-station',
#                          bootstrap_servers=['15.236.9.122:9092'])
# for message in consumer:
#     # message value and key are raw bytes -- decode if necessary!
#     # e.g., for unicode: `message.value.decode('utf-8')`
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))
'''
