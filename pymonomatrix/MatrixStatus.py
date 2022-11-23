import yaml
import requests

api_url = "http://192.168.0.178//cgi-bin/MUH44TP_getsetparams.cgi"


class MatrixStatus:
    def __init__(self, input_labels, output_video_labels, output_audio_labels):
        self.input_labels = input_labels
        self.output_video_labels = output_video_labels
        self.output_audio_labels = output_audio_labels
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
        self.volume = []

        for i in range(0, 8):
            # Chunk the volume in 3 character blocks
            # Remove "!" for volumes less than 100
            self.volume.append(temp[i * 3:i * 3 + 3].replace("!", ""))

    def decode_mute(self):
        # decode the mute
        temp = self.response_yaml["volume3"]
        self.mute = []

        for i in range(0, 8):
            # Chunk mute
            self.mute.append(temp[i:i + 1])

    def decode_video_output(self):
        # decode the video output
        temp = self.response_yaml["Outputbuttom"]
        self.video_output = []

        for i in range(0, 8):
            # Chunk output
            self.video_output.append(temp[i:i + 1])

    def decode_audio_output(self):
        # decode the audio output
        temp = self.response_yaml["hdmi_buttom"]
        self.audio_output = []

        for i in range(0, 8):
            # Chunk output
            self.audio_output.append(temp[i * 2:i * 2 + 2])
