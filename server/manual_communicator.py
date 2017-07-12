#! /usr/bin/env python

'''
Manual Communicator

'''

def is_alive(posts, GUID) :
    if GUID is None :
        return False
    entry = posts.find_one({'client':GUID})
    if entry is None :
        sys.stderr.write('\tERROR: COULD NOT FIND %s IN THE DATABASE\n' %GUID)
        return False
    return not entry.get('is_dead')

def request_ping(mqtt_client, posts, GUID) :
        if not is_alive(posts, GUID) :
            print('Sorry, %s is dead or not available.' %GUID)
        else :
            dump = json.dumps({'request':'ping'})
            mqtt_client.publish("/%s" %GUID, payload=dump)

def kill_client(mqtt_client, posts, GUID) :
    if not is_alive(posts, GUID) :
        print('Sorry, %s is already dead or not available.' %GUID)
    else :
        dump = json.dumps({'request':'die'})
        mqtt_client.publish("/%s" %GUID, payload=dump)

def randomize_interval(mqtt_client, posts, GUID) :
    if GUID is not None and is_alive(posts, GUID) :
        dump = json.dumps({'request':'randomize'})
        mqtt_client.publish("/%s" %GUID, payload=dump)
    else :
        print('Sorry, %s is dead or not available.' %GUID)

def randomize_pings(mqtt_client, posts, GUID) :
    if GUID is not None :
        randomize_interval(mqtt_client, posts, GUID)
    else :
        for entry in posts.find({'is_dead':False}) :
            GUID = entry.get('client')
            randomize_interval(mqtt_client, posts, GUID)

def run(mqtt_client, posts, opt) :
    if opt == 'i' :
        print('Randomize ping interval offset.')
        one = raw_input('Default is to randomize all client ping intervals. To specify one client, type \'y\': ')
        GUID = None
        if one == 'y' :
            GUID = raw_input('Which client? (GUID): ')
        else :
            print('Randomizing all client ping intervals.')
        randomize_pings(mqtt_client, posts, GUID)
    if opt == 'k' :
        print('Kill client process.')
        GUID = raw_input('Which client? (GUID): ')
        kill_client(mqtt_client, posts, GUID)
    if opt == 'r' :
        print('Request a ping from client.')
        GUID = raw_input('Which client? (GUID): ')
        request_ping(mqtt_client, posts, GUID)

def get_mqtt_client(config) :
    mqtt_client = paho.Client()
    mqtt_client.connect(config['mqtt_host'], config['mqtt_port'], 60)
    return mqtt_client

def get_db_posts(config) :
    dbclient = MongoClient('mongodb://%s:%d' %(config['mongo_host'], config['mongo_port']))
    db = dbclient.ping_database
    posts = db.posts
    return posts

def main(config, args, options) :
    print('MQTT Communicator')
    posts = get_db_posts(config)
    mqtt_client = get_mqtt_client(config)
    if args.r or args.GUID is not None :
        GUID = args.GUID
        if not args.r :
            print('In automatic mode, option \'r\' is required.')
        print(options)
        print('Automatic mode not yet enabled.')
        return 0
    opt = ''
    while(opt != 'exit') :
        print('\n\tManual Mode')
        print('i -- randomize ping interval offset.')
        print('r -- request ping from client.')
        print('k -- kill client process.')
        print('exit -- exit this program.\n')
        opt = raw_input('Which task: ')
        run(mqtt_client, posts, opt)
    print('Bye.')

if __name__ == '__main__' :
    import paho.mqtt.client as paho
    from pymongo import MongoClient
    from read_config import read_config
    import json
    import sys
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--GUID', action='store', type='string', help='GUID of client.', dest='GUID')
    parser.add_option('-r', action='store_true', help='Randomize ping offsets. Randomizes one if GUID is specified, otherwise all are randomized.', dest='r')
    args, options = parser.parse_args()
    print(args)
    print(options)
    main(read_config(), args, options)

