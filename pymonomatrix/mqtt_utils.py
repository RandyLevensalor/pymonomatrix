import time
from paho.mqtt import client as mqtt_client


def connect_mqtt(client_id, username, password, broker, port) -> mqtt_client:
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
