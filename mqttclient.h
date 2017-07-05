#ifndef MQTTCLIENT_H
#define MQTTCLIENT_H

#include <mosquittopp.h>
#include <string>
#include <cstdio>

class MqttClient : public mosqpp::mosquittopp
{
public:
    MqttClient(const char *id, const char *host, int port);
    ~MqttClient();

    void on_connect(int rc);
    void on_message(const struct mosquitto_message *message);
    void on_subscribe(int mid, int qos_count, const int *granted_qos);
};

#endif
