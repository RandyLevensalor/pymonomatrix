import os
import yaml

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
        "input_labels": ["Roku Ultra", "Roku 3", "Apple TV", "Chromecast", "Fire TV", "None", "None", "None"],
        "output_video_labels": ["Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "Rec Room", "Gym"],
        "output_audio_labels": ["Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            try:
                config = yaml.safe_load(f) or {}
                # Update default config with the values loaded from file
                default_config.update(config)
                return default_config
            except yaml.YAMLError as e:
                print(f"Error parsing config file {config_file}: {e}")
    else:
        print(f"Warning: Configuration file {config_file} not found. Using default labels.")

    # Default values if file doesn't exist or parsing fails
    return default_config
