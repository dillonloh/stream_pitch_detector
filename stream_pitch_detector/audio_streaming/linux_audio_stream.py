import subprocess

import aubio
import numpy as np

from audio_streaming.audio_stream import AudioStream

class LinuxAudioStream(AudioStream):
    
    def __init__(self, os: str = "linux", chunk_size: int = 1024, 
                 rate: int = 44100, channels: int = 2, format: np.dtype = np.int16):
        self.os = "linux"
        self.chunk_size = chunk_size
        self.rate = rate
        self.channels = channels
        self.format = format
        self.device = self._get_default_sink_monitor()

        self.parec_command = [
            'parec',
            '-d', self.device,
            '--rate', str(self.rate),
            '--channels', str(self.channels),
            '--format', 's16le'
        ]

        self.stream_process = None

    def _get_default_sink_monitor(self) -> str:
        """ 
        Get the monitor source of the default sink 
        
        Returns:
            str: The monitor source of the default sink

        Raises:
            Warning: If the monitor source for the default sink could not be found
        """
        default_sink = subprocess.run(['pactl', 'get-default-sink'], capture_output=True, text=True).stdout.strip()
        sinks = subprocess.run(['pactl', 'list', 'short', 'sinks'], capture_output=True, text=True).stdout.splitlines()
        for sink in sinks:
            parts = sink.split()
            if parts[1] == default_sink:
                monitor_source = parts[1] + ".monitor"
                return monitor_source
            
        raise Warning("Could not find the monitor source for the default sink.")
    
    def start_stream(self):
        """
        Start the audio stream
        
        """
        if not self.stream_process:
            self.stream_process = subprocess.Popen(self.parec_command, stdout=subprocess.PIPE, bufsize=self.chunk_size)
        
        else:
            raise Warning("Stream is already running")
        
    def stop_stream(self):
        """
        Stop the audio stream
        
        """
        if self.stream_process:
            self.stream_process.terminate()
            self.stream_process = None
        
        else:    
            raise Exception("Stream is not running")
    

    def stream_audio_chunk(self) -> np.ndarray:
        """
        Return a chunk of audio data from the stream
        
        Returns:
            np.ndarray: The audio data chunk
        
        """
        if not self.stream_process:
            raise Exception("Stream is not running")

        chunk_bin = self.stream_process.stdout.read(self.chunk_size * self.channels * 2)
        
        # reshape the data to the correct shape [chunk_size, channels]
        # works since the data from the stereo channels is interleaved
        chunk = np.frombuffer(chunk_bin, dtype=self.format).reshape(-1, self.channels)

        return chunk
    
