#include "mqtt_client.h"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <map>

using std::string;
using std::to_string;
using std::printf;
using std::stoi;
using std::srand;

const string _DEFAULT_PORT = "1883";
const string _DEFAULT_HOST = "10.42.0.1";
const string _DEFAULT_LCYCLE = "10";

string get_arg(int argc, char* argv[], string option, string _DEFAULT)
{
    string arg = _DEFAULT;
    for (int i = 0; i < argc; i++)
    {
        if (string(argv[i]) == option)
        {
            arg = string(argv[i+1]);
            break;
        }
    }
    return arg;
}

int has_option(int argc, char* argv[], string option)
{
    bool result = false;
    for (int i = 0; i < argc; i++)
    {
        if (string(argv[i]) == option)
        {
            result = true;
            break;
        }
    }
    return result;
}

int display_help()
{
    cout << "OPTIONS:\n\t-help display this help message and exit\n\t-p [port_number]\n\t-h [host]\n\t-l [ping cycle length]\n" << endl;
    return 0;
}

int main(int argc, char* argv[])
{
    if (has_option(argc, argv, "-help"))
    {
        display_help();
        return 0;
    }
    int port = stoi(get_arg(argc, argv, "-p", _DEFAULT_PORT));
    string host = get_arg(argc, argv, "-h", _DEFAULT_HOST);
    int lcycle = stoi(get_arg(argc, argv, "-l", _DEFAULT_LCYCLE));
    srand(time(NULL));
    const string GUID = "GUID-" + to_string(rand());
    // 3 is the cycle length the server expects.
    // You may use 7 or higher to simulate routine death and restart.
    printf("Client process started.\n");
    MqttClient * mqttHdl;
    mqttHdl = new MqttClient(GUID, lcycle, host, port);
    mqttHdl->run();
    delete mqttHdl;
    printf("Client process ended.\n");
    return 0;
}

