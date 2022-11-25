import requests

api_url = "http://192.168.0.178//cgi-bin/MMX32_Keyvalue.cgi"


class SetMatrix:
    def __init__(self, input_labels, output_video_labels, output_audio_labels):
        self.input_labels = input_labels
        self.output_video_labels = output_video_labels
        self.output_audio_labels = output_audio_labels

    def set_volume(self, output, volume):
        # Set the volume for the given output
        # output is a string, volume is an int
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath",
        #  "Guest", "Office", "DeckUp", "Deck Down"
        # volume can be 0-100, V+, V-, MU, UM
        # returns True if successful, False if not

        # This needs to have a body, but it doesn't matter what it is
        req_body = "CMD=AVOLUME0" + str(output) + ":" + volume + "."
        return self.post_command(req_body)

    def set_video_output(self, output: int, input: int):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be 1-8
        # returns True if successful, False if not

        # This needs to have a body, but it doesn't matter what it is
        req_body = "CMD=OUT0" + str(output) + ":0" + str(input) + "."
        return self.post_command(req_body)

    def set_audio_output(self, output: int, input: int):
        # Set the input for the given output
        # output can be "Living Room", "Bar", "Master Bed", "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"
        # input can be 1-8
        # returns True if successful, False if not

        # convert input to a string and pad with a 0 if less than 10
        input_str = str(input)
        if input < 10:
            input_str = "0" + input_str
        req_body = "CMD=AUDIO0" + str(output) + ":" + input_str + "."
        return self.post_command(req_body)

    def post_command(self, req_body: str):
        # Post the command to the matrix
        print(req_body)
        response = requests.post(api_url, data=req_body)
        if response.status_code == 200:
            return True
        print("Failed to " + req_body + " Response code:" + str(response.status_code))
        return False
