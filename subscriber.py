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

def on_message(mosq, obj, msg) :
    print('Received message:')
    print(json.loads(msg.payload))

if __name__ == '__main__':
    config = read_config()
    client = paho.Client()

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect(config['mqtt_host'], config['mqtt_port'], 60)

    #GUID = 'GUID-%d' %random.randint(1000,9999)
    GUID = 'GUID-1822'
    client.subscribe("/%s" %GUID, 0)
    client.on_message = on_message

    print('ID: %s' %GUID)
    dump = json.dumps({'client':GUID})
    while client.loop() == 0:
        client.publish("/sendping", payload=dump)
        time.sleep(3)
        pass

