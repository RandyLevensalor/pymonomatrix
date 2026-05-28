import argparse
from SetMatrix import SetMatrix
from config import setup_matrix_object

# Create the matrix status object
setMatrix = setup_matrix_object(SetMatrix)

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
