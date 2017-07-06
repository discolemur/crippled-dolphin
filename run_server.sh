#! /bin/bash


#mosquitto -p 1883 &

mongod --port=27017 --dbpath=/home/nick/code/mqtt/database/ &


python presence_checker.py --mongo_host localhost --mongo_port 27017 &

python discovery_watcher.py --mongo_host localhost --mongo_port 27017 --mqtt_host localhost --mqtt_port 1883 &



