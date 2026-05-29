# python3.6

import argparse
import sys

from config import setup_matrix_object
from paho.mqtt import client as mqtt_client
from SetMatrix import SetMatrix


def connect_mqtt(client_id, username, password, broker, port) -> mqtt_client:
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


def subscribe(client: mqtt_client, topic: str, setMatrix: SetMatrix):
    def on_message(client, userdata, msg):
        payload_decoded = msg.payload.decode()
        print(f"Received `{payload_decoded}` from `{msg.topic}` topic")
        topic_suffix = msg.topic.removeprefix(topic)
        topic_suffix_split = topic_suffix.split("-")

        if len(topic_suffix_split) < 2:
            print(f"Warning: Ignored malformed topic '{msg.topic}' (missing hyphen delimiter)")
            return

        action_type = topic_suffix_split[1]
        index = topic_suffix_split[0]
        value = payload_decoded
        print(f"Type:{action_type} Index:{index} Value:{value}")

        allowed_types = ['volume', 'video_output', 'audio_output']
        if action_type not in allowed_types:
            print(f"Error: Invalid type '{action_type}' received in topic '{msg.topic}'")
            return

        try:
            set_function = getattr(setMatrix, f"set_{action_type}")
            set_function(index, value)
        except AttributeError:
            print(f"Warning: No handler found for type '{action_type}'")

    client.subscribe(f"{topic}#")
    client.on_message = on_message


def run(client_id, username, password, broker, port, topic, setMatrix):
    client = connect_mqtt(client_id, username, password, broker, port)
    subscribe(client, topic, setMatrix)
    try:
        rc = client.loop_forever()
        return rc
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        client.disconnect()
        return 0
    except Exception as e:
        print(f"Error during MQTT loop: {e}")
        return 1


if __name__ == '__main__':
    import uuid
    argparser = argparse.ArgumentParser()
    argparser.add_argument("user", help="username for the MQTT broker")
    argparser.add_argument("password", help="password for the MQTT broker")
    argparser.add_argument("broker", help="IP address of the MQTT broker")
    args = argparser.parse_args()
    username = args.user
    password = args.password
    broker = args.broker

    port = 1883
    topic = "pymonomatrix/set/"
    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{uuid.uuid4().hex}'

    setMatrix = setup_matrix_object(SetMatrix)

    sys.exit(run(client_id, username, password, broker, port, topic, setMatrix))
