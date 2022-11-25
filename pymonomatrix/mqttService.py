from MatrixStatus import MatrixStatus
from paho.mqtt import client as mqtt_client
import time
import random
import argparse


# Create the matrix status object
input_labels = ["Roku Ultra", "Roku 3", "Apple TV",
                "Chromecast", "Fire TV", "None", "None", "None"]
output_video_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "Rec Room", "Gym"]
output_audio_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]

curr_status = MatrixStatus(
    input_labels, output_video_labels, output_audio_labels)

# MQTT Parameters

port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, curr_status):
    while True:
        time.sleep(3)
        curr_status.refresh()
        classes = ["volume", "mute", "video_output", "audio_output"]
        for curr_class in classes:
            publish_class(client, curr_status, curr_class)


def publish_class(client, curr_status, topic_class):
    # assign curr_status.volume to a local variable
    value = getattr(curr_status, topic_class)
    for i in range(0, 8):
        msg = value[i]
        topic = f"pymonomatrix/{i}-{topic_class}"
        result = client.publish(topic, str(msg))
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    curr_status = MatrixStatus(
        input_labels, output_video_labels, output_audio_labels)

    client = connect_mqtt()
    client.loop_start()
    publish(client, curr_status)


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
