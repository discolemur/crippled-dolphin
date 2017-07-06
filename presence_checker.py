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

lcycle = 10

def check_presence(posts) :
    global lcycle
    start = int(time.time())
    # Find all living clients in the database
    for entry in posts.find({'is_dead':False}) :
        client = str(entry.get('client'))
        seen = entry.get('time')
        if (int(time.time()) - seen) > 2 * lcycle :
            # Update database with notice of death
            result = posts.update_one({'client':entry.get('client')}, {'$set':{'is_dead':True}}, upsert=False)
            print('%s died.' %entry.get('client'))
    next_check = start + lcycle
    difference = next_check - int(time.time())
    if difference > 0 :
        time.sleep(difference)

def main(args) :
    dbclient = MongoClient('mongodb://%s:%d' %(args.moh, args.mop))
    db = dbclient.test_database
    posts = db.posts
    while(True) :
        check_presence(posts)

if __name__ == '__main__' :
    from pymongo import MongoClient
    import time
    import random
    random.seed()
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--mongo_host', type='string', default='localhost', dest='moh')
    parser.add_option('--mongo_port', type=int, default=27017, dest='mop')
    options, args = parser.parse_args()
    main(options)

