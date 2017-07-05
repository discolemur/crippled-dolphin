#! /usr/bin/env python

from pymongo import MongoClient
import time
import random
random.seed()

def check_presence(posts, dead) :
    for entry in posts.find() :
        client = entry.get('client')
        seen = entry.get('time')
        if client not in dead and (int(time.time()) - seen) > 10 :
            print('%s died :(' %client)
            dead.add(client)
    return dead


if __name__ == '__main__':
    dbclient = MongoClient('mongodb://localhost:8213')
    db = dbclient.test_database
    posts = db.posts
    dead = set()
    while(True) :
        dead = check_presence(posts, dead)
