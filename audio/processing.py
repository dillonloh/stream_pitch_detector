import numpy as np
import pyaudio

def process_audio(data):
    """
    Process the audio data.
    This example converts the byte data to a numpy array and prints the max value.
    Replace or expand this function to apply effects, analyze the audio, etc.
    """
    audio_data = np.frombuffer(data, dtype=np.int16)
    print(f"Max amplitude in chunk: {np.max(audio_data)}")

def callback(in_data, frame_count, time_info, status):
    process_audio(in_data)
    return (None, pyaudio.paContinue)