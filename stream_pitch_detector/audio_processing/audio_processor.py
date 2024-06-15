import aubio

from librosa.effects import pitch_shift
import numpy as np


class AudioProcessor:
    """Class for processing audio chunks"""

    def __init__(
        self,
        buffer_size: int = 512,
        hop_size: int = 512,
        sample_rate: int = 44100,
        unit: str = "Hz",
        tolerance: float = 0.8,
    ):
        """Initialise audio processor

        Args:
            buffer_size (int, optional): The buffer size. Defaults to 1024.
            hop_size (int, optional): The hop size. Defaults to 512.
            sample_rate (int, optional): The sample rate. Defaults to 44100.

        """
        self.buffer_size = buffer_size
        self.hop_size = hop_size
        self.sample_rate = sample_rate
        self.pitch_detector = aubio.pitch(
            "default", self.buffer_size, self.hop_size, self.sample_rate
        )
        self.pitch_detector.set_unit(unit)
        self.pitch_detector.set_tolerance(tolerance)

    def get_chunk_pitch(self, chunk: np.ndarray) -> float:
        """Get the pitch of an audio chunk
        Reference: https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py

        Args:
            chunk (np.ndarray): The audio chunk

        Returns:
            float: The pitch of the audio chunk

        """

        # aubio requires float32 input
        chunk = chunk.astype(np.float32)

        # check if stereo
        if chunk.shape[1] == 2:
            # convert to mono by averaging the channels for each sample
            chunk = np.mean(chunk, axis=1)

        # Get the pitch from the chunk
        pitch = self.pitch_detector(chunk)[0]

        return pitch

    def shift_pitch(self, chunk: np.ndarray, semitones: float = 0) -> np.ndarray:
        """
        Shift the pitch of an audio chunk
        Reference: https://librosa.org/doc/latest/generated/librosa.effects.pitch_shift.html#librosa.effects.pitch_shift

        Args:
            chunk (np.ndarray): The audio chunk
            semitones (float): The number of semitones to shift the pitch by

        Returns:
            np.ndarray: The pitch shifted audio chunk

        """

        # check if stereo
        if chunk.shape[1] == 2:
            # convert to mono by averaging the channels for each sample
            chunk = np.mean(chunk, axis=1)

        shifted_chunk = pitch_shift(
            chunk, sr=self.sample_rate, n_steps=semitones, n_fft=chunk.shape[0]
        )  # avoid padding by setting n_fft to chunk size

        return shifted_chunk
