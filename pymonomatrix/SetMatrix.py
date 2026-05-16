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

    def _get_index(self, labels, item, list_name, item_type="Output"):
        try:
            return int(labels.index(item)) + 1
        except ValueError:
            print(f"{item_type} {item} not found in {list_name}")
            return None

    def set_volume(self, output, volume):
        # Set the volume for the given output
        # output is a string, volume is an int
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath",
        #  "Guest", "Office", "DeckUp", "Deck Down"
        # volume can be 0-100, V+, V-, MU, UM
        # returns True if successful, False if not
        output_index = self._get_index(self.output_audio_labels, output, "output_audio_labels")
        if output_index is None:
            return False
        if volume not in ("V+", "V-", "MU", "UM"):
            try:
                vol_val = int(volume)
            except ValueError:
                print(f"Volume {volume} is not a valid value")
                return False
            if vol_val < 10:
                volume = f"0{volume}"
        # This needs to have a body, but it doesn't matter what it is
        req_body = "CMD=AVOLUME0" + str(output_index) + ":" + str(volume) + "."
        return self.post_command(req_body)

    def set_video_output(self, output: str, input_val: str):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be 1-8
        # returns True if successful, False if not

        # find index of output in output_video_labels
        video_index = self._get_index(self.output_video_labels, output, "output_video_labels")
        if video_index is None:
            return False
        try:
            input_index = int(self.input_labels.index(input_val)) + 1
        except ValueError:
            print(f"Input {input_val} not found in input_labels")
            return False

        req_body = f"CMD=OUT0{video_index}:0{input_index}."
        return self.post_command(req_body)

    def set_audio_output(self, output: int, input_val: int):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be 1-8
        # returns True if successful, False if not

        # convert input to a string and pad with a 0 if less than 10
        audio_index = self._get_index(self.output_audio_labels, output, "output_audio_labels")
        if audio_index is None:
            return False

        try:
            input_index = int(self.input_labels.index(input_val)) + 1
        except ValueError:
            print(f"Input {input_val} not found in input_labels")
            return False

        input_str = str(input_index)
        if input_index < 10:
            input_str = f"0{input_str}"
        req_body = f"CMD=AUDIO0{audio_index}:{input_str}."
        return self.post_command(req_body)

    def post_command(self, req_body: str):
        # Post the command to the matrix
        print(req_body)
        response = requests.post(api_url, data=req_body, timeout=10)
        if response.status_code == 200:
            return True
        print(f"Failed to {req_body} Response code:{response.status_code}")
        return False
