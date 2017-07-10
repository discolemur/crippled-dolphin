#! /usr/bin/env python

import thread
from subprocess import call
import time

def run_client() :
    call(["./client.o", "-l", "2"])

_N_THREADS = 1000

try :
    for i in range(_N_THREADS) :
        thread.start_new_thread(run_client, ())
        time.sleep(.05)
except :
    print("ERROR: unable to start threads.")

while 1 :
    pass
