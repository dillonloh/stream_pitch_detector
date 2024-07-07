import numpy as np
import pyaudiowpatch as pyaudio

from audio_streaming.audio_stream import AudioStream


class WindowsAudioStream(AudioStream):
    def __init__(
        self,
        os: str = "windows",
        chunk_size: int = 512,
        rate: int = 44100,
        channels: int = 2,
        format: np.dtype = np.int16,
    ):
        self.os = "windows"
        self.chunk_size = chunk_size
        self.rate = rate
        self.channels = channels
        self.format = format
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self) -> None:
        """
        Start the audio stream

        """
        device_info = self.find_loopback_output()
        channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
        self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=int(device_info["defaultSampleRate"]),
                    input=True,
                    input_device_index=device_info["index"],
                    frames_per_buffer=self.chunk_size,
        )

    def stop_stream(self) -> None:
        """
        Stop the audio stream

        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        else:
            raise Exception("Stream is not running")
        
    def stream_audio_chunk(self) -> np.ndarray:
        """If the stream is running, read a chunk of audio data from the stream

        Returns:
            np.ndarray: A chunk of audio data
        """
        if not self.stream:
            raise Exception("Stream is not running")
        
        chunk_bin = self.stream.read(self.chunk_size)
        chunk = np.frombuffer(chunk_bin, dtype=self.format).reshape(-1, self.channels)

        return chunk
    
    def find_loopback_output(self) -> dict:
        """
        Try to find loopback device that is currently being used as the default WASAPI-based output device.
        Does this by comparing the default output device name with the loopback device names.
        Unfortunately, this is the most adequate way at the moment.

        Returns:
            dict: The loopback device info
        """
        
        try:
            # Get default WASAPI info
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            raise Exception("Could not find WASAPI host API")
    
        # Get default WASAPI speakers
        default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in self.p.get_loopback_device_info_generator():

                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break

            else:
                raise Exception("Could not find Loopback Device")
        
        print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        return default_speakers
