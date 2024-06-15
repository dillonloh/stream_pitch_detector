import platform
import time

import numpy as np
from scipy.io.wavfile import write

from audio_streaming.linux_audio_stream import LinuxAudioStream
from audio_processing.audio_processor import AudioProcessor

OUTPUT_FILE = "shifted_audio.wav"
SEMITONES = -4
DURATION = 60


def main():
    # check if os is linux
    try:
        current_platform = platform.system().lower()
        if "linux" in current_platform:
            audio_stream = LinuxAudioStream()
        else:
            raise NotImplementedError(
                f"OS: {current_platform} is not currently supported"
            )

        audio_processor = AudioProcessor()
        audio_stream.start_stream()

        shifted_audio = []
        start_time = time.time()

        while (time.time() - start_time) < DURATION:
            chunk = audio_stream.stream_audio_chunk()
            pitch = audio_processor.get_chunk_pitch(chunk)
            print(f"Pitch: {pitch}")
            shifted_chunk = audio_processor.shift_pitch(chunk, semitones=SEMITONES)
            shifted_audio.append(shifted_chunk)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        audio_stream.stop_stream()

    # Concatenate all shifted audio chunks
    shifted_audio = np.concatenate(shifted_audio, axis=0)

    # Save the shifted audio to a file
    write(OUTPUT_FILE, audio_stream.rate, shifted_audio.astype(np.int16))


if __name__ == "__main__":
    main()
