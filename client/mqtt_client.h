#ifndef MQTTCLIENT_H
#define MQTTCLIENT_H

#include "mqtt/async_client.h"
#include <string>

class MqttClient
{
private:
	mqtt::async_client * client;

public:
    MqttClient(const std::string GUID, const std::string host, const int port)
    {
        const std::string URI = "tcp://" + host + ":" + std::to_string(port);
	this->client = new mqtt::async_client( URI, GUID );
    }
    ~MqttClient()
    {
	    delete this->client;
    }

    void on_connect() {}
    void on_message() {}
    void on_subscribe() {}
    void run() {}
};

#endif
