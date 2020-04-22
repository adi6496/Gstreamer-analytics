import sys
import traceback
import argparse
from argparse import ArgumentParser
import os
import subprocess
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject  # noqa:F401,F402


def run_webcam():

    parser = ArgumentParser(add_help=False)
    _args = parser.add_argument_group('Options')
    _args.add_argument("-d", "--detection_model", help="Required. Path to an .xml file with object detection model",
                   required=True, type=str)
    device = "/dev/video0"
    args = parser.parse_args()
    pipeline_str = "v4l2src device={} ! decodebin ! videoconvert ! video/x-raw ! gvadetect model={} ! gvawatermark ! timeoverlay ! "\
        "x264enc ! mpegtsmux ! hlssink location=video_files/segment%06d.ts playlist-location=video_files/index.m3u8 target-duration=10" \
        .format(device, args.detection_model)


    return pipeline_str


def run_youtube(input_url):

    parser = ArgumentParser(add_help=False)
    _args = parser.add_argument_group('Options')
    _args.add_argument("-d", "--detection_model", help="Required. Path to an .xml file with object detection model",
                   required=True, type=str)
    args = parser.parse_args()

    youtube_dl_str = "youtube-dl --format " +  "\"best[ext=mp4][protocol=https]\"" + " --get-url " + input_url
    print(youtube_dl_str)
    location = subprocess.check_output(youtube_dl_str, shell=True).decode()
    print(location)
    pipeline_str = "souphttpsrc is-live=true location={} ! decodebin ! videoconvert ! video/x-raw ! gvadetect model={} ! queue ! gvawatermark ! "\
         "x264enc ! mpegtsmux ! hlssink location=video_files/segment%06d.ts playlist-location=video_files/index.m3u8 target-duration=10" \
        .format(location, args.detection_model)

    return pipeline_str


# Initializes Gstreamer, it's variables, paths
Gst.init(sys.argv)

input_device = input("Choose video source - 1.Webcam  2.Youtube video (type 1 or 2)")

if input_device == "1":
    command = run_webcam()
else:
    input_url = input("Enter the URL of the youtube video: ")
    command = run_youtube(input_url)

# DEFAULT_PIPELINE = "v4l2src ! decodebin ! videoconvert ! video/x-raw ! gvadetect model=intel_models/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml ! "\
#         "gvawatermark ! timeoverlay ! "\
#         "x264enc ! mpegtsmux ! hlssink location=video_files/segment%06d.ts playlist-location=video_files/index.m3u8 target-duration=10"

# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--pipeline", required=False,
#                 default=DEFAULT_PIPELINE, help="Gstreamer pipeline without gst-launch")

# args = vars(ap.parse_args())


def on_message(bus: Gst.Bus, message: Gst.Message, loop: GObject.MainLoop):
    mtype = message.type
    """
        Gstreamer Message Types and how to parse
        https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
    """
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()

    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(err, debug)
        loop.quit()

    elif mtype == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(err, debug)

    return True


# command = args["pipeline"]

# Gst.Pipeline https://lazka.github.io/pgi-docs/Gst-1.0/classes/Pipeline.html
# https://lazka.github.io/pgi-docs/Gst-1.0/functions.html#Gst.parse_launch
pipeline = Gst.parse_launch(command)

# https://lazka.github.io/pgi-docs/Gst-1.0/classes/Bus.html
bus = pipeline.get_bus()

# allow bus to emit messages to main thread
bus.add_signal_watch()

# Start pipeline
pipeline.set_state(Gst.State.PLAYING)

# Init GObject loop to handle Gstreamer Bus Events
loop = GObject.MainLoop()

# Add handler to specific signal
# https://lazka.github.io/pgi-docs/GObject-2.0/classes/Object.html#GObject.Object.connect
bus.connect("message", on_message, loop)

try:
    loop.run()
except Exception:
    traceback.print_exc()
    loop.quit()

# Stop Pipeline
pipeline.set_state(Gst.State.NULL)