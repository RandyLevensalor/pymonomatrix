import os
import requests

matrix_ip = os.getenv("MONOPRICE_MATRIX_IP")
if not matrix_ip:
    raise ValueError("MONOPRICE_MATRIX_IP environment variable is not set")
api_url = f"http://{matrix_ip}//cgi-bin/MMX32_Keyvalue.cgi"


class SetMatrix:
    def __init__(self, input_labels, output_video_labels, output_audio_labels):
        self.input_labels = input_labels
        self.output_video_labels = output_video_labels
        self.output_audio_labels = output_audio_labels

        self._input_labels_map = {label: i for i, label in enumerate(input_labels)}
        self._output_video_labels_map = {label: i for i, label in enumerate(output_video_labels)}
        self._output_audio_labels_map = {label: i for i, label in enumerate(output_audio_labels)}
        self.session = requests.Session()

    def _get_index(self, labels_map, item, list_name, item_type="Output"):
        try:
            return labels_map[item] + 1
        except KeyError:
            print(f"{item_type} {item} not found in {list_name}")
            return None

    def set_volume(self, output, volume):
        # Set the volume for the given output
        # output is a string, volume is an int
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath",
        #  "Guest", "Office", "DeckUp", "Deck Down"
        # volume can be 0-100, V+, V-, MU, UM
        # returns True if successful, False if not
        output_index = self._get_index(self._output_audio_labels_map, output, "output_audio_labels")
        if output_index is None:
            return False
        if volume not in ("V+", "V-", "MU", "UM"):
            try:
                vol_val = int(volume)
            except ValueError:
                print(f"Volume {volume} is not a valid value")
                return False
            volume = str(volume).zfill(2)
        # This needs to have a body, but it doesn't matter what it is
        req_body = f"CMD=AVOLUME0{output_index}:{volume}."
        return self.post_command(req_body)

    def set_video_output(self, output: str, input_val: str):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be a string matching an input label (e.g. "Roku Ultra", "Roku 3", etc.)
        # returns True if successful, False if not

        # find index of output in output_video_labels
        video_index = self._get_index(self._output_video_labels_map, output, "output_video_labels")
        if video_index is None:
            return False

        input_index = self._get_index(self._input_labels_map, input_val, "input_labels", "Input")
        if input_index is None:
            return False

        req_body = f"CMD=OUT0{video_index}:0{input_index}."
        return self.post_command(req_body)

    def set_audio_output(self, output: str, input_val: str):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be a string matching an input label (e.g. "Roku Ultra", "Roku 3", etc.)
        # returns True if successful, False if not

        # convert input to a string and pad with a 0 if less than 10
        audio_index = self._get_index(self._output_audio_labels_map, output, "output_audio_labels")
        if audio_index is None:
            return False

        input_index = self._get_index(self._input_labels_map, input_val, "input_labels", "Input")
        if input_index is None:
            return False

        input_str = str(input_index).zfill(2)
        req_body = f"CMD=AUDIO0{audio_index}:{input_str}."
        return self.post_command(req_body)

    def post_command(self, req_body: str):
        # Post the command to the matrix
        print(req_body)
        response = self.session.post(api_url, data=req_body, timeout=10)
        if response.status_code == 200:
            return True
        print(f"Failed to {req_body} Response code:{response.status_code}")
        return False
