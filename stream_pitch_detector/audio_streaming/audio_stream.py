import numpy as np

class AudioStream:
    
    def __init__(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def stream_audio_chunk(self) -> np.ndarray:
        """
        Return a chunk of audio data from the stream
        
        Returns:
            np.ndarray: The audio data chunk
        
        """
        raise NotImplementedError("This method should be overridden by subclasses")
    