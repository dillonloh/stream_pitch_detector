import subprocess
import numpy as np
import aubio
import wave

# Parameters
CHUNK_SIZE = 512  # Number of frames per buffer, matching the expected input size for aubio
RATE = 44100  # Sampling rate
CHANNELS = 2  # Number of audio channels
FORMAT = np.int16  # Audio format
OUTPUT_FILE = 'output.wav'  # Output file for recording

def get_default_sink_monitor():
    """ Get the monitor source of the default sink """
    default_sink = subprocess.run(['pactl', 'get-default-sink'], capture_output=True, text=True).stdout.strip()
    sinks = subprocess.run(['pactl', 'list', 'short', 'sinks'], capture_output=True, text=True).stdout.splitlines()
    for sink in sinks:
        parts = sink.split()
        if parts[1] == default_sink:
            monitor_source = parts[1] + ".monitor"
            return monitor_source
    return None

# Get the monitor source of the default sink
DEVICE = get_default_sink_monitor()
if not DEVICE:
    raise Exception("Could not find the monitor source for the default sink.")

# Start the parec process
command = [
    'parec',
    '-d', DEVICE,
    '--rate', str(RATE),
    '--channels', str(CHANNELS),
    '--format', 's16le'
]

process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=CHUNK_SIZE)

# Initialize aubio pitch detection
pitch_detector = aubio.pitch("default", CHUNK_SIZE, CHUNK_SIZE, RATE)
pitch_detector.set_unit("Hz")
pitch_detector.set_silence(-40)


def process_audio_chunk(chunk):
    """ Process audio chunk to detect pitch """
    # Convert the byte data to numpy array
    audio_data = np.frombuffer(chunk, dtype=FORMAT)

    # If stereo, convert to mono by averaging the channels
    if CHANNELS == 2:
        audio_data = np.mean(audio_data.reshape(-1, 2), axis=1).astype(np.int16)

    # Print the first few samples of the audio data
    print("Audio data samples:", audio_data[:10])

    # Convert to float32 for aubio
    audio_data = audio_data.astype(np.float32)

    # Detect pitch
    pitch = pitch_detector(audio_data)[0]
    return pitch

print("Streaming, processing, and recording audio...")

# Open the output file for writing
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes per sample (s16le)
    wf.setframerate(RATE)

    try:
        first_chunk = True
        while True:
            # Read a chunk of audio data
            chunk = process.stdout.read(CHUNK_SIZE * CHANNELS * 2)  # 2 bytes per sample (s16le)
            if len(chunk) == 0:
                break
            # Write the audio chunk to the file
            wf.writeframes(chunk)
            # Process the audio chunk to detect pitch
            pitch = process_audio_chunk(chunk)
            print(f"Pitch: {pitch:.2f} Hz")

    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()


print("Streaming stopped.")
