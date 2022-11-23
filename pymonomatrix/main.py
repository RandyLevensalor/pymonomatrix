from MatrixStatus import MatrixStatus
from SetMatrix import SetMatrix

DEBUG = True

# Create the matrix status object
input_labels = ["Roku Ultra", "Roku 3", "Apple TV",
                "Chromecast", "Fire TV", "None", "None", "None"]
output_video_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "Rec Room", "Gym"]
output_audio_labels = ["Living Room", "Bar", "Master Bed",
                       "Master Bath", "Guest", "Office", "DeckUp", "Deck Down"]

curr_status = MatrixStatus(input_labels, output_video_labels, output_audio_labels)

if DEBUG:
    print(curr_status.volume[7])
    print(curr_status.mute[7])
    print(curr_status.video_output[0])
    print(curr_status.audio_output[0])
    print(curr_status.input_labels[0])
    print(curr_status.output_video_labels[0])
    print(curr_status.output_audio_labels[0])

setMatrix = SetMatrix(input_labels,
                      output_video_labels, output_audio_labels)
setMatrix.set_volume(8, "MU")
setMatrix.set_video_output(1, 5)
setMatrix.set_audio_output(1, 12)
