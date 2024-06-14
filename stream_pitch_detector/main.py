import platform

from audio_streaming.linux_audio_stream import LinuxAudioStream
from audio_processing.audio_processor import AudioProcessor


def main():
    
    # check if os is linux
    current_platform = platform.system().lower()
    if "linux" in current_platform:
        audio_stream = LinuxAudioStream()
    else:
        raise NotImplementedError(f"OS: {current_platform} is not currently supported")

    audio_processor = AudioProcessor()
    audio_stream.start_stream()
    while True:
        chunk = audio_stream.stream_audio_chunk()
        pitch = audio_processor.get_chunk_pitch(chunk)
        print(f"Pitch: {pitch}")
        
if __name__ == "__main__":

    main()