import time

from config import setup_matrix_object, parse_mqtt_args
from mqtt_utils import connect_mqtt
from MatrixStatus import MatrixStatus


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
    username, password, broker, client_id = parse_mqtt_args()

    port = 1883

    # Create the matrix status object
    curr_status = setup_matrix_object(MatrixStatus)

    run(client_id, username, password, broker, port, curr_status)
