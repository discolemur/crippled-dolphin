//#include "mqttclient.h"
#include "mosquitto-1.4.13/lib/cpp/mosquittopp.h"
#include <cstdio>
#include <string>

const int port = 1883;
const std::string ipAddress = "192.168.1.139";
const std::string clientName = "MySpecialName";

int main()
{
    printf("Client process started.\n");
    mosqpp::lib_version(NULL, NULL, NULL);
    //MqttClient * mqttHdl;
    //mqttHdl = new MqttClient(clientName.c_str(), ipAddress.c_str(), port);
    //delete mqttHdl;
    printf("Client process ended.\n");
    return 0;
}
