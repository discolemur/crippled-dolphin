#! /usr/bin/env python

'''
Presence Checker

Checks the database continually
for all known clients.

Compare time of last message received
to the current time.

If it has been at least two cycles since last seen,
consider that client dead, and
the is_dead flag in the database is set.
'''

def request_ping(mqtt_client, GUID) :
    dump = json.dumps({'request_ping':True})
    print('Requesting ping on channel /%s' %GUID)
    mqtt_client.publish("/%s" %GUID, payload=dump)

def check_presence(posts, mqtt_client, lcycle) :
    start = int(time.time())
    # Find all living clients in the database
    for entry in posts.find({'is_dead':False}) :
        client = str(entry.get('client'))
        seen = entry.get('time')
        if (int(time.time()) - seen) > 2 * lcycle :
            # Update database with notice of death
            result = posts.update_one({'client':entry.get('client')}, {'$set':{'is_dead':True}}, upsert=False)
            request_ping(mqtt_client, entry.get('client'))
            print('%s died.' %entry.get('client'))
    next_check = start + lcycle
    difference = next_check - int(time.time())
    if difference > 0 :
        time.sleep(difference)

def main(config) :
    dbclient = MongoClient('mongodb://%s:%d' %(config['mongo_host'], config['mongo_port']))
    db = dbclient.ping_database
    posts = db.posts
    mqtt_client = paho.Client()
    mqtt_client.connect(config['mqtt_host'], config['mqtt_port'], 60)
    while(True) :
        check_presence(posts, mqtt_client, config['lcycle'])

if __name__ == '__main__' :
    import paho.mqtt.client as paho
    from pymongo import MongoClient
    from read_config import read_config
    import time
    import random
    import json
    random.seed()
    main(read_config())

