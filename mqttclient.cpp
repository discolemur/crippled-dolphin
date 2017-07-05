#include "mqttclient.h"

MqttClient::MqttClient(const char *id, const char *host, int port) : mosquittopp(id)
{
    mosqpp::lib_init();         // Initialize libmosquitto

    int keepalive = 120; // seconds
    connect(host, port, keepalive);     // Connect to MQTT Broker
}

void MqttClient::on_connect(int rc)
{
    printf("Connected with code %d. \n", rc);

    if (rc == 0)
    {
        subscribe(NULL, "command/IGot");
    }
}

void MqttClient::on_subscribe(int mid, int qos_count, const int *granted_qos)
{
    printf("Subscription succeeded. \n");
}

void MqttClient::on_message(const struct mosquitto_message *message)
{
}

