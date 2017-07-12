#! /usr/bin/env python

import thread
from subprocess import call
import time
import random

random.seed(0)
_N_THREADS = 1

def run_client() :
    call(["./client.o", "-l", "2", "-g", "GUID-%d"%random.randint(1000,9999)])

try :
    for i in range(_N_THREADS) :
        thread.start_new_thread(run_client, ())
        time.sleep(.05)
except :
    print("ERROR: unable to start threads.")

while 1 :
    pass
