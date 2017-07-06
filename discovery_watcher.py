#! /usr/bin/env python

'''
Discovery Watcher

Subscribes to an MQTT broker.

Any message that can be interpretted
as a python dictionary
containing the key "client"
is logged in a mongo database
with the time received.
'''

# TODO print out when dead comes alive again

posts = None

def on_message(mosq, obj, msg):
    global posts
#    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    content = json.loads(msg.payload)
    if not isinstance(content, dict) :
        return
    if 'client' in content :
        result = posts.update_one({'client':content['client']}, {"$set":{'time':int(time.time()),'is_dead':False}}, upsert=True)
        print('Received message from %s' %content['client'])
 
def init_db(host, port) :
    global posts
    dbclient = MongoClient('mongodb://%s:%d' %(host, port))
    db = dbclient.test_database
    posts = db.posts

def watch_mqtt(host, port) :
    client = paho.Client()
    client.on_message = on_message
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect(host, port, 60)
    client.subscribe('/sendping', 0)
    while client.loop() == 0:
        pass

def main(args) :
    init_db(args.moh, args.mop)
    watch_mqtt(args.mqh, args.mqp)

if __name__ == '__main__':
    import optparse
    import time
    import json
    from pymongo import MongoClient
    import paho.mqtt.client as paho
    parser = optparse.OptionParser()
    parser.add_option('--mongo_host', type='string', default='localhost', dest='moh')
    parser.add_option('--mongo_port', type=int, default=27017, dest='mop')
    parser.add_option('--mqtt_host', type='string', default='localhost', dest='mqh')
    parser.add_option('--mqtt_port', type=int, default=1883, dest='mqp')
    options, args = parser.parse_args()
    main(options)

