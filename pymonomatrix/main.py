import requests
from MatrixStatus import MatrixStatus

DEBUG = True

api_url = "http://192.168.0.178//cgi-bin/MUH44TP_getsetparams.cgi"

# This needs to have a body, but it doesn't matter what it is
req_body = {"foo": "bar"}

response = requests.post(api_url, json=req_body)

input_labels = ["Roku Ultra", "Roku 3", "Apple TV",
                "Chromecast", "Fire TV", "None", "None", "None"]
output_video_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "Rec Room", "Gym"]
output_audio_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]

if response.status_code == 200:
    response_string = response.text
    curr_status = MatrixStatus(response_string, input_labels, output_video_labels, output_audio_labels)

if DEBUG:
    print(curr_status.volume[0])
    print(curr_status.mute[0])
    print(curr_status.video_output[0])
    print(curr_status.audio_output[0])
    print(curr_status.input_labels[0])
    print(curr_status.output_video_labels[0])
    print(curr_status.output_audio_labels[0])
