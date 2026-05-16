# python3.6

import random
import argparse
from SetMatrix import SetMatrix
from paho.mqtt import client as mqtt_client
from config import load_config


port = 1883
topic = "pymonomatrix/set/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

# Load configuration
config = load_config()
input_labels = config.get("input_labels")
output_video_labels = config.get("output_video_labels")
output_audio_labels = config.get("output_audio_labels")

setMatrix = SetMatrix(input_labels,
                      output_video_labels, output_audio_labels)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload_decoded = msg.payload.decode()
        print(f"Received {payload_decoded} from {msg.topic} topic")
        topic_suffix = msg.topic.removeprefix(topic)
        topic_suffix_split = topic_suffix.split("-")

        if len(topic_suffix_split) < 2:
            print(f"Warning: Ignored malformed topic '{msg.topic}' (missing hyphen delimiter)")
            return

        type = topic_suffix_split[1]
        index = topic_suffix_split[0]
        value = payload_decoded
        print(f"Type:{type} Index:{index} Value:{payload_decoded}")

        try:
            set_function = getattr(setMatrix, f"set_{type}")
            set_function(index, value)
        except AttributeError:
            print(f"Warning: No handler found for type '{type}'")
    client.subscribe(f"{topic}#")
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("user", help="username for the MQTT broker")
    argparser.add_argument("password", help="password for the MQTT broker")
    argparser.add_argument("broker", help="IP address of the MQTT broker")
    args = argparser.parse_args()
    username = args.user
    password = args.password
    broker = args.broker

    run()
