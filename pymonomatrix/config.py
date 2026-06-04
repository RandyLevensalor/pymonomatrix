import os
import yaml
import logging

DEFAULT_CONFIG_FILE = "config.yaml"

def load_config():
    config_file = os.environ.get("PYMONOMATRIX_CONFIG", DEFAULT_CONFIG_FILE)

    # Try to resolve relative to module if not found in current directory
    if not os.path.exists(config_file):
        # Could be we are running from inside the pymonomatrix directory or outside
        module_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(module_dir)
        possible_path = os.path.join(root_dir, config_file)
        if os.path.exists(possible_path):
            config_file = possible_path

    default_config = {
        "input_labels": [f"Input {i}" for i in range(1, 9)],
        "output_video_labels": [f"Output {i}" for i in range(1, 9)],
        "output_audio_labels": [f"Output {i}" for i in range(1, 9)]
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            try:
                config = yaml.safe_load(f) or {}
                # Update default config with the values loaded from file
                default_config.update(config)
                return default_config
            except yaml.YAMLError as e:
                logging.error(f"Error parsing config file {config_file}: {e}")
    else:
        logging.warning(f"Configuration file {config_file} not found. Using default labels.")

    # Default values if file doesn't exist or parsing fails
    return default_config


def get_matrix_ip():
    matrix_ip = os.getenv("MONOPRICE_MATRIX_IP")
    if not matrix_ip:
        raise ValueError("MONOPRICE_MATRIX_IP environment variable is not set")
    return matrix_ip

def setup_matrix_object(matrix_class):
    matrix_ip = get_matrix_ip()
    config = load_config()
    input_labels = config.get("input_labels")
    output_video_labels = config.get("output_video_labels")
    output_audio_labels = config.get("output_audio_labels")
    return matrix_class(matrix_ip, input_labels, output_video_labels, output_audio_labels)

def parse_mqtt_args():
    import argparse
    import uuid
    argparser = argparse.ArgumentParser()
    argparser.add_argument("user", help="username for the MQTT broker")
    argparser.add_argument("password", help="password for the MQTT broker")
    argparser.add_argument("broker", help="IP address of the MQTT broker")
    args = argparser.parse_args()

    username = args.user
    password = args.password
    broker = args.broker
    client_id = f'python-mqtt-{uuid.uuid4().hex}'

    return username, password, broker, client_id
