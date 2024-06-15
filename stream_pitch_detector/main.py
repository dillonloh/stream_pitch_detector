import platform
import time

import numpy as np
from scipy.io.wavfile import write

from audio_streaming.linux_audio_stream import LinuxAudioStream
from audio_processing.audio_processor import AudioProcessor

OUTPUT_FOLDER = "output"


def main(
    chunk_size=2048,
    sample_rate=44100,
    semitones=0,
    duration=-1,
    output_file="shifted_audio.wav",
):
    # check if os is linux
    try:
        current_platform = platform.system().lower()
        if "linux" in current_platform:
            audio_stream = LinuxAudioStream(chunk_size=chunk_size, rate=sample_rate)
        else:
            raise NotImplementedError(
                f"OS: {current_platform} is not currently supported"
            )

        audio_processor = AudioProcessor(
            buffer_size=chunk_size, hop_size=chunk_size, sample_rate=sample_rate
        )
        audio_stream.start_stream()

        shifted_audio = []
        start_time = time.time()

        if duration < 0:  # if duration is not explicitly set, record forever
            duration = float("inf")

        while (time.time() - start_time) < duration:
            chunk = audio_stream.stream_audio_chunk()
            pitch = audio_processor.get_chunk_pitch(chunk)
            print(f"Pitch: {pitch}")
            shifted_chunk = audio_processor.shift_pitch(chunk, semitones=semitones)
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
    write(
        f"{OUTPUT_FOLDER}/{output_file}",
        audio_stream.rate,
        shifted_audio.astype(np.int16),
    )


if __name__ == "__main__":
    main(
        chunk_size=2048,
        sample_rate=44100,
        semitones=-4,
        duration=60,
        output_file="shifted_audio.wav",
    )
