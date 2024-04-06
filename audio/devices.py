import sys
import os
import pyaudio

pitch_detector_dir = os.path.join(os.path.dirname(__file__), '..', '..')
normalized_path = os.path.abspath(pitch_detector_dir)
if normalized_path not in sys.path:
    sys.path.append(normalized_path)

from config.text_colours import textcolors
from .processing import callback

p = pyaudio.PyAudio()

def find_loopback_output() -> None:
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(textcolors.green + str(device_info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (device_info["name"], p.get_host_api_info_by_index(device_info["hostApi"])["name"]))
        if check_wasapi(device_info) and check_stereo_mix(device_info):
            print(textcolors.green + "Found WASAPI Stereo Mix device!" + textcolors.end)
            return device_info
    
def check_wasapi(device_info: str) -> bool:
    return (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1

def check_stereo_mix(device_info: str) -> bool:
    """ Check if either 'Stereo Mix' or 'ステレオ ミキサー' is in the device name """
    stereo_mix_names = ["Stereo Mix", "ステレオ ミキサー"]
    return any(name in device_info["name"] for name in stereo_mix_names)

def open_stream() -> None:
    device_info = find_loopback_output()
    print(device_info["index"])
    frames_per_buffer = 512
    channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
    print(p.get_device_info_by_index(device_info["index"]))
    stream = p.open(format=pyaudio.paInt16,
                  channels=channelcount,
                  rate=int(device_info["defaultSampleRate"]),
                  input=True,
                  input_device_index=device_info["index"],
                  frames_per_buffer=frames_per_buffer,
                  as_loopback=True)

    return stream

stream = open_stream()