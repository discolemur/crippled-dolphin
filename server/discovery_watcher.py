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

posts = None

def on_message(mosq, obj, msg):
    global posts
    content = json.loads(msg.payload)
    #print('Received message from %s' %content['GUID'])
    #print(content)
    if not isinstance(content, dict) :
        return
    if 'GUID' in content :
        entry = posts.find_one({'client':content['GUID']})
        if entry is not None and 'statement' in content :
            if content['statement'] == 'dead' :
                result = posts.update_one({'client':content['GUID']}, {"$set":{'time':int(time.time()),'is_dead':True}}, upsert=True)
        else :
            if entry is not None and entry['is_dead'] :
                print('%s has restarted.' %entry['client'])
            result = posts.update_one({'client':content['GUID']}, {"$set":{'time':int(time.time()),'is_dead':False}}, upsert=True)
 
def init_db(host, port) :
    global posts
    dbclient = MongoClient('mongodb://%s:%d' %(host, port))
    db = dbclient.ping_database
    posts = db.posts

def watch_mqtt(host, port) :
    client = paho.Client()
    client.on_message = on_message
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect(host, port, 60)
    client.subscribe('/sendping', 0)
    client.loop_forever()

def main(config) :
    init_db(config['mongo_host'], config['mongo_port'])
    watch_mqtt(config['mqtt_host'], config['mqtt_port'])

if __name__ == '__main__':
    import time
    import json
    from pymongo import MongoClient
    import paho.mqtt.client as paho
    from read_config import read_config
    main(read_config())

