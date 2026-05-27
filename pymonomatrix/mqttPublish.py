from MatrixStatus import MatrixStatus
from paho.mqtt import client as mqtt_client
import time
import random
import argparse
from config import setup_matrix_object

def connect_mqtt(client_id, username, password, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    
    # Add a retry loop for the initial connection
    while True:
        try:
            client.connect(broker, port)
            return client
        except Exception as e:
            print(f"Network unreachable ({e}). Retrying in 5 seconds...")
            time.sleep(5)


def publish(client_id, username, password, broker, port, curr_status):
    client = connect_mqtt(client_id, username, password, broker, port)
    client.loop_start()

    classes = ["volume", "mute", "video_output", "audio_output"]
    while True:
        time.sleep(1)
        curr_status.refresh()
        for curr_class in classes:
            publish_class(client, curr_status, curr_class)


def publish_class(client, curr_status, topic_class):
    # assign curr_status.volume to a local variable
    value = getattr(curr_status, topic_class)
    changed = getattr(curr_status, f"{topic_class}_changed")

    if topic_class in ("volume", "mute", "audio_output"):
        labels = curr_status.output_audio_labels
    else:
        labels = curr_status.output_video_labels

    for i in range(0, 8):
        if bool(changed[i]):
            msg = value[i]
            room = labels[i]
            topic = f"pymonomatrix/{room}-{topic_class}"
            result = client.publish(topic, str(msg), qos=0, retain=True)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run(client_id, username, password, broker, port, curr_status):
    publish(client_id, username, password, broker, port, curr_status)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("user", help="username for the MQTT broker")
    argparser.add_argument("password", help="password for the MQTT broker")
    argparser.add_argument("broker", help="IP address of the MQTT broker")
    args = argparser.parse_args()
    username = args.user
    password = args.password
    broker = args.broker

    port = 1883
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    # Create the matrix status object
    curr_status = setup_matrix_object(MatrixStatus)

    run(client_id, username, password, broker, port, curr_status)
