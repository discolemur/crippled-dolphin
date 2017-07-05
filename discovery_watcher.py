#! /usr/bin/env python

"""
A small example subscriber
"""
from pymongo import MongoClient
import paho.mqtt.client as paho
import time

db = None
posts = None

def on_message(mosq, obj, msg):
#    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    print('Received message!')
    result = posts.update_one({"client":msg.payload}, {"time":int(time.time())})
    

if __name__ == '__main__':
    dbclient = MongoClient('mongodb://localhost:8213')
    db = dbclient.test_database
    posts = db.posts

    client = paho.Client()
    client.on_message = on_message

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("localhost", 8080, 60)
    client.subscribe("/GUID/sendping", 0)

    while client.loop() == 0:
        pass

