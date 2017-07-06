#include "mqtt_client.h"
#include <cstdio>
#include <string>

// For random number GUID
#include <cstdlib>

using std::string;
using std::to_string;
using std::printf;

int main()
{
    const int port = 1883;
    const string ipAddress = "10.42.0.1";
    const string GUID = "GUID-" + to_string(rand());
    printf("Client process started.\n");
    MqttClient * mqttHdl;
    mqttHdl = new MqttClient(GUID, ipAddress, port);
    mqttHdl->run();
    delete mqttHdl;
    printf("Client process ended.\n");
    return 0;
}
