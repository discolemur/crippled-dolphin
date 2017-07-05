This file should tell you how to compile and run the MQTT server and client.


To download MQTT server:

    $ apt-get install mosquitto

To download c++ development library:

    $ apt-get install libmosquittopp-dev

To compile mosquitto parts (BROKEN!) :

    $ g++ -Wall -L /home/nick/code/mqtt/mosquitto-1.4.13/lib/cpp *.cpp -o client.o

To compile mongo parts :

    $ c++ --std=c++11 test.cpp -o test $(pkg-config --cflags --libs libmongocxx)





To run MongoDB :

mongod --port=27017 -dbpath database/

