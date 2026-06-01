import argparse
from SetMatrix import SetMatrix
from config import load_config

DEBUG = False

# Load configuration
config = load_config()
input_labels = config.get("input_labels")
output_video_labels = config.get("output_video_labels")
output_audio_labels = config.get("output_audio_labels")

# Create the matrix status object
setMatrix = SetMatrix(input_labels,
                      output_video_labels, output_audio_labels)

if DEBUG:
    setMatrix.set_volume(8, "MU")
    setMatrix.set_video_output(1, 5)
    setMatrix.set_audio_output(1, 12)

# parse the command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("type", help="type to set [volume, video_output, audio_output]")
argparser.add_argument("index", help="index of the item 0-7")
argparser.add_argument("value", help="value to set")
args = argparser.parse_args()

if args.type == "volume":
    setMatrix.set_volume(args.index, args.value)
elif args.type == "video_output":
    setMatrix.set_video_output(args.index, args.value)
elif args.type == "audio_output":
    setMatrix.set_audio_output(args.index, args.value)
