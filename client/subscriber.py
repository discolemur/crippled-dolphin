#! /usr/bin/env python

"""
A small example subscriber
"""
import paho.mqtt.client as paho
import time
import random
import json
from read_config import read_config
random.seed()

GUID = None
ping_msg = None

def send_ping(client) :
    global GUID
    global ping_msg
    if ping_msg is None :
        ping_msg = json.dumps({'GUID':GUID})
    client.publish("/sendping", payload=ping_msg)

def on_message(client, userdata, msg) :
    content = json.loads(msg.payload)
    if content['request'] == 'ping' :
        print('HI!')
        send_ping(client)

if __name__ == '__main__':
    config = read_config()
    client = paho.Client()
    client.on_message = on_message

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect(config['mqtt_host'], config['mqtt_port'], 60)

    GUID = 'GUID-%d' %random.randint(1000,9999)
    #GUID = 'GUID-1822'
    client.subscribe("/%s" %GUID, 0)

    print('ID: %s' %GUID)
    while client.loop() == 0:
        send_ping(client)
        time.sleep(config['lcycle'])
        pass

