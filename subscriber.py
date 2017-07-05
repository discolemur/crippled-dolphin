#! /usr/bin/env python

"""
A small example subscriber
"""
import paho.mqtt.client as paho
import time
import random
random.seed()

if __name__ == '__main__':
    client = paho.Client()

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect("localhost", 8080, 60)

#    client.subscribe("/GUID/sendping", 0)

    coolID = random.randint(1000000,9999999)
    print('ID: %d' %coolID)

    client.publish("/GUID/sendping", payload=coolID)
    while client.loop() == 0:
        time.sleep(3)
        client.publish("/GUID/sendping", payload=coolID)
        pass

