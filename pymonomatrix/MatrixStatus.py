import yaml
import requests
import logging


class MatrixStatus:
    def __init__(self, matrix_ip, input_labels, output_video_labels, output_audio_labels):
        self.api_url = f"http://{matrix_ip}//cgi-bin/MUH44TP_getsetparams.cgi"
        self.input_labels = input_labels
        self.output_video_labels = output_video_labels
        self.output_audio_labels = output_audio_labels
        self.video_output = [-1] * 8
        self.volume = [-1] * 8
        self.mute = [-1] * 8
        self.audio_output = [-1] * 8
        self.video_output_changed = [True] * 8
        self.volume_changed = [True] * 8
        self.mute_changed = [True] * 8
        self.audio_output_changed = [True] * 8
        self.session = requests.Session()

    def refresh(self):
        self.get_status()
        self.fix_yaml()
        if not hasattr(self, 'response_yaml') or not isinstance(self.response_yaml, dict):
            logging.error("Invalid or missing YAML response from matrix, skipping decode")
            return
        self.decode_volume()
        self.decode_mute()
        self.decode_video_output()
        self.decode_audio_output()

    def get_status(self):
        # This needs to have a body, but it doesn't matter what it is
        req_body = {"foo": "bar"}
        try:
            response = self.session.post(self.api_url, json=req_body, timeout=10)
            response.raise_for_status()
            self.response = response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching status from matrix: {e}")
            self.response = None

    def fix_yaml(self):
        if not self.response:
            return
        # Remove the "(" and ")" characters from the response string
        # convert response string to a yaml object
        import re
        fixed_response = re.sub(r':(?!\s)', ': ', self.response.strip().strip("()"))
        try:
            self.response_yaml = yaml.safe_load(fixed_response)
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML from matrix: {e}")
            self.response_yaml = None

    def _update_state(self, state_array, changed_array, index, new_value):
        changed = (new_value != state_array[index])
        if changed:
            changed_array[index] = True
            state_array[index] = new_value
        else:
            changed_array[index] = False
        return changed

    def decode_volume(self):
        # decode the volume
        temp = str(self.response_yaml.get("volume2", ""))

        for i in range(0, 8):
            # Chunk the volume in 3 character blocks
            # Remove "!" for volumes less than 100
            new_volume = int(temp[i * 3:i * 3 + 3].replace("!", ""))
            if self._update_state(self.volume, self.volume_changed, i, new_volume):
                print(f"Volume changed: {new_volume}")
                print(f"Volume bool: {bool(self.volume_changed[i])}")

    def decode_mute(self):
        # decode the mute
        temp = str(self.response_yaml.get("volume3", "")).zfill(8)

        for i in range(0, 8):
            # Chunk mute
            new_mute = temp[i:i + 1]
            self._update_state(self.mute, self.mute_changed, i, new_mute)

    def decode_video_output(self):
        # decode the video output
        temp = str(self.response_yaml.get("Outputbuttom", "")).zfill(8)

        for i in range(0, 8):
            # Chunk output
            new_output = self.input_labels[int(temp[i:i + 1]) - 1]
            self._update_state(self.video_output, self.video_output_changed, i, new_output)

    def decode_audio_output(self):
        # decode the audio output
        temp = str(self.response_yaml.get("hdmi_buttom", "")).zfill(16)

        for i in range(0, 8):
            # Chunk output
            new_output_index = int(temp[i * 2:i * 2 + 2]) - 1
            if new_output_index < 8:
                new_output = self.input_labels[new_output_index]
            else:
                new_output = self.output_video_labels[new_output_index - 8]
            self._update_state(self.audio_output, self.audio_output_changed, i, new_output)
