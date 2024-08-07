import os
import platform
import time
import traceback

import numpy as np
from scipy.io.wavfile import write

from audio_streaming.linux_audio_stream import LinuxAudioStream
from audio_streaming.windows_audio_stream import WindowsAudioStream
from audio_processing.audio_processor import AudioProcessor

OUTPUT_FOLDER = "output"


def main(
    chunk_size=2048,
    sample_rate=44100,
    semitones=0,
    duration=-1,
    output_file="shifted_audio",
):
    # Check if the output folder exists, if not create it
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    audio_stream = None
    
    # check if os is linux
    try:
        current_platform = platform.system().lower()
        print(f"Running on OS: {current_platform}")
        if "linux" in current_platform:
            audio_stream = LinuxAudioStream(chunk_size=chunk_size, rate=sample_rate)
        elif "windows" in current_platform:
            audio_stream = WindowsAudioStream(chunk_size=chunk_size, rate=sample_rate)
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
            pitch = audio_processor.get_chunk_note(chunk)
            print(f"Pitch: {pitch}")
            shifted_chunk = audio_processor.shift_pitch(chunk, semitones=semitones)
            shifted_audio.append(shifted_chunk)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    except Exception as e:
        print(traceback.format_exc())
        exit(1)

    finally:
        if audio_stream is not None:
            audio_stream.stop_stream()
        
    
    # Concatenate all shifted audio chunks
    shifted_audio = np.concatenate(shifted_audio, axis=0)
    output_file_name = f"{OUTPUT_FOLDER}/{output_file}_{semitones}.wav"
    # Save the shifted audio to a file

    write(
        output_file_name,
        audio_stream.rate,
        shifted_audio.astype(np.int16),
    )


if __name__ == "__main__":
    main(
        chunk_size=2048,
        sample_rate=44100,
        semitones=7,
        duration=60,
        output_file="shifted_audio",
    )
