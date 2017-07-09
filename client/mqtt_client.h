#ifndef MQTTCLIENT_H
#define MQTTCLIENT_H

#include "mqtt/async_client.h"
#include <string>
#include <thread>
#include <chrono>
#include <ostream>

using std::string;
using std::cout;
using std::endl;

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
            mqtt::async_client * client;
            string topic;

            // Callback for when a message arrives.
            void message_arrived(mqtt::const_message_ptr msg) override
            {
                cout << "Received message" << endl;
                cout << "\tPayload: " << msg->to_string() << "\n" << endl;
                // TODO if asked for ping, send another ping.
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
                    mqtt::async_client * c,
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
        this->cb = new callback(this->client, this->connOpts, "/" + this->GUID);
        this->client->set_callback(*this->cb);
    }
    ~MqttClient()
    {
        delete this->client;
        delete this->connOpts;
        delete this->cb;
    }

    mqtt::message_ptr ping_msg()
    {
        const string ping_topic = "/sendping";
        const string payload = "{ \"client\":\"" + this->GUID + "\" }";
        mqtt::message_ptr msg = mqtt::make_message(ping_topic, payload);
        msg->set_qos(0);
        return msg;
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
            // Create message
            mqtt::message_ptr msg = this->ping_msg();
            // Keep publishing a ping every cycle
            do {
                this->client->publish(msg);
                std::this_thread::sleep_for(
                    std::chrono::seconds(this->lcycle));
            } while (true);
            this->client->disconnect();
        }
        catch (const mqtt::exception& exc)
        {
            std::cerr << "Error: " << exc.what() << " ["
                << exc.get_reason_code() << "]" << std::endl;
            return 1;
        }
        return 0;
    }
};

#endif
