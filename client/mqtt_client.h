#ifndef MQTTCLIENT_H
#define MQTTCLIENT_H

#include "mqtt/async_client.h"
#include <string>
#include <thread>
#include <chrono>
#include <ostream>
#include <vector>
#include <sstream>
#include <cstdlib>

using std::string;
using std::cout;
using std::endl;
using std::vector;
using std::stringstream;

class MqttClient
{

// Inner classes
private:

    /*
        Listens for messages.
    */
    class callback : public virtual mqtt::callback,
                    public virtual mqtt::iaction_listener
    {
        private:
            mqtt::connect_options * connOpts;
            MqttClient * client;
            string topic;
            
            vector<string> parseRequest(string msg)
            {
                vector<string> result;
                stringstream ss;
                ss.str(msg);
                stringstream word;
                char c;
                bool getting = false;
                while (ss.get(c))
                {
                    if (c == '\"')
                    {
                        getting = !getting;
                        if (!getting)
                        {
                            string req = word.str();
                            if (req != "request")
                            {
                                result.push_back(req);
                            }
                            word.str("");
                        }
                    }
                    else if (getting)
                    {
                        word.put(c);
                    }
                }
                return result;
            }
            // Callback for when a message arrives.
            // Right now, no matter what we assume the message is a ping request.
            void message_arrived(mqtt::const_message_ptr msg) override
            {
                //cout << "Received message" << endl;
                //cout << "\tPayload: " << msg->to_string() << "\n" << endl;
                vector<string> requests = this->parseRequest(msg->to_string());
                for (size_t i = 0; i < requests.size(); i++)
                {
                    if (requests[i] == "ping")
                    {
                        this->client->send_ping();
                    }
                    else if (requests[i] == "randomize")
                    {
                        this->client->send_ping();
                        int amt = rand() % this->client->get_lcycle();
                        std::this_thread::sleep_for(std::chrono::seconds(amt));
                    }
                    else if (requests[i] == "die")
                    {
                        this->client->stop();
                    }
                }
            }
            void on_failure(const mqtt::token& asyncActionToken) override
            {
                cout << "Connection failed." << endl;
            }
            void on_success(const mqtt::token& asyncActionToken) override
            {
                cout << "Connection success!" << endl;
                cout << "Listening at: " << this->topic << endl;
            }

        public:
            callback(
                    MqttClient * c,
                    mqtt::connect_options * opt,
                    string t
                    ) : connOpts(opt), client(c), topic(t) {}
            string get_topic() { return this->topic; }
    };

// Member variables
private:
    mqtt::async_client * client;
    mqtt::connect_options * connOpts;
    const string GUID;
    const int lcycle;
    callback * cb;
    mqtt::message_ptr ping_msg;
    bool keep_going;

public:
    MqttClient(
            const string guid,
            const int lcyc,
            const string host,
            const int port)
            : GUID(guid), lcycle(lcyc)
    {
        this->connOpts = new mqtt::connect_options();
        this->connOpts->set_keep_alive_interval(20);
        this->connOpts->set_clean_session(true);
        const string URI = "tcp://" + host + ":" + std::to_string(port);
        cout << URI << endl;
        this->client = new mqtt::async_client( URI, GUID );
        this->cb = new callback(this, this->connOpts, "/" + this->GUID);
        this->client->set_callback(*this->cb);
        const string ping_topic = "/sendping";
        const string payload = "{ \"GUID\":\"" + this->GUID + "\" }";
        this->ping_msg = mqtt::make_message(ping_topic, payload);
        this->ping_msg->set_qos(0);
        this->keep_going = true;
    }
    ~MqttClient()
    {
        delete this->cb;
        delete this->client;
        delete this->connOpts;
    }
    int get_lcycle() { return this->lcycle; }
    int send_ping()
    {
        try
        {
            this->client->publish(this->ping_msg);
            //cout << "ping" << endl;
        }
        catch (const mqtt::exception& exc)
        {
            std::cerr << "Error: " << exc.what() << " ["
                << exc.get_reason_code() << "]" << endl;
            return 1;
        }
        return 0;
    }
    int stop()
    {
        this->keep_going = false;
        return 0;
    }
    int run()
    {
        try
        {
            // Connect
            mqtt::token_ptr token_conn = this->client->connect(*this->connOpts);
            token_conn->wait();
            // Subscribe to personal channel
            this->client->subscribe(this->cb->get_topic(), 0, nullptr, *this->cb);
            // Keep publishing a ping every cycle
            do {
                this->send_ping();
                std::this_thread::sleep_for(std::chrono::seconds(this->lcycle));
            } while (keep_going);
            this->client->disconnect();
        }
        catch (const mqtt::exception& exc)
        {
            std::cerr << "Error: " << exc.what() << " ["
                << exc.get_reason_code() << "]" << endl;
            return 1;
        }
        return 0;
    }
};

#endif
