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
    std::srand(time(NULL));
    const int port = 1883;
    const string ipAddress = "10.42.0.1";
    const string GUID = "GUID-" + to_string(rand());
    // 3 is the cycle the server expects. We use 7 to simulate routine death and restart.
    const int lcycle = 7;
    printf("Client process started.\n");
    MqttClient * mqttHdl;
    mqttHdl = new MqttClient(GUID, lcycle, ipAddress, port);
    mqttHdl->run();
    delete mqttHdl;
    printf("Client process ended.\n");
    return 0;
}

