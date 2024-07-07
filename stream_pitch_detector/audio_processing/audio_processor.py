import aubio
import math
from typing import Optional

from librosa.effects import pitch_shift
import numpy as np

# each note's number of half steps away from C in its octave
STEP_TO_NOTE_MAP = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}

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
    
    def get_chunk_note(self, chunk: np.ndarray) -> Optional[str]:
        """Get the note of an audio chunk

        Args:
            chunk (np.ndarray): The audio chunk
            
        Returns:
            str: The note of the audio chunk
            None: If the pitch is 0 and ignore_zeros is True

        """

        pitch = self.get_chunk_pitch(chunk)
        
        if pitch == 0.0:
            return None
            
        note = self._convert_pitch_to_letter_notes(pitch)

        return note


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

    def _convert_pitch_to_letter_notes(self, pitch: float) -> str:
        """Convert pitch frequency to letter notes (e.g. A4, C#5, etc.)

        Args:
            pitch (float): The pitch frequency

        Returns:
            str: The letter note
        """

        # Convert pitch frequency to nearest MIDI note, where A4 is 440Hz.
        # Reference: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
        midi_note = round(69 + (12 * math.log2(pitch / 440)))
    
        # Convert MIDI note to letter notes (e.g. A4, C#5, etc.), where C0 is midi note 12
        octave = (midi_note // 12) - 1
        # calculate step difference from C to get note
        step_diff = midi_note % 12
        letter_note = STEP_TO_NOTE_MAP[step_diff]

        return f"{letter_note}{octave}"
    