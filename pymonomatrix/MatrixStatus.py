import yaml
import requests

api_url = "http://192.168.0.178//cgi-bin/MUH44TP_getsetparams.cgi"


class MatrixStatus:
    def __init__(self, input_labels, output_video_labels, output_audio_labels):
        self.input_labels = input_labels
        self.output_video_labels = output_video_labels
        self.output_audio_labels = output_audio_labels
        self.video_output = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.volume = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.mute = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.audio_output = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.video_output_changed = [True, True, True, True, True, True, True, True]
        self.volume_changed = [True, True, True, True, True, True, True, True]
        self.mute_changed = [True, True, True, True, True, True, True, True]
        self.audio_output_changed = [True, True,
                                     True, True, True, True, True, True]

    def refresh(self):
        self.get_status()
        self.fix_yaml()
        self.decode_volume()
        self.decode_mute()
        self.decode_video_output()
        self.decode_audio_output()

    def get_status(self):
        # This needs to have a body, but it doesn't matter what it is
        req_body = {"foo": "bar"}
        self.response = requests.post(api_url, json=req_body).text

    def fix_yaml(self):
        # Remove the "(" and ")" characters from the response string
        temp_string = self.response
        temp_string = temp_string.replace("(", "")
        temp_string = temp_string.replace(")", "")

        # convert response string to a yaml object
        self.response_yaml = yaml.safe_load(temp_string)

    def decode_volume(self):
        # decode the volume
        temp = self.response_yaml["volume2"]

        for i in range(0, 8):
            # Chunk the volume in 3 character blocks
            # Remove "!" for volumes less than 100
            new_volume = int(temp[i * 3:i * 3 + 3].replace("!", ""))
            # print(f"new_volume: {new_volume}, old_volume: {self.volume[i]}")
            if new_volume != self.volume[i]:
                print(f"Volume changed: {new_volume}")
                self.volume_changed[i] = True
                print(f"Volume bool: {bool(self.volume_changed[i])}")
                self.volume[i] = new_volume
            else:
                self.volume_changed[i] = False

    def decode_mute(self):
        # decode the mute
        temp = self.response_yaml["volume3"]

        for i in range(0, 8):
            # Chunk mute
            new_mute = temp[i:i + 1]
            if new_mute != self.mute[i]:
                self.mute_changed[i] = True
                self.mute[i] = new_mute
            else:
                self.mute_changed[i] = False

    def decode_video_output(self):
        # decode the video output
        temp = self.response_yaml["Outputbuttom"]

        for i in range(0, 8):
            # Chunk output
            new_output = self.input_labels[int(temp[i:i + 1]) - 1]
            if new_output != self.video_output[i]:
                self.video_output_changed[i] = True
                self.video_output[i] = new_output
            else:
                self.video_output_changed[i] = False

    def decode_audio_output(self):
        # decode the audio output
        temp = self.response_yaml["hdmi_buttom"]

        for i in range(0, 8):
            # Chunk output
            new_output_index = int(temp[i * 2:i * 2 + 2]) - 1
            if new_output_index < 8:
                new_output = self.input_labels[new_output_index]
            else:
                new_output = self.output_video_labels[new_output_index - 8]
            if new_output != self.audio_output[i]:
                self.audio_output_changed[i] = True
                self.audio_output[i] = new_output
            else:
                self.audio_output_changed[i] = False
