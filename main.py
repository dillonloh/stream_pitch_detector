import pyaudio

from config.text_colours import textcolors
from audio.devices import stream
defaultframes = 512

p = pyaudio.PyAudio()

def main():

    # Start streaming

    print(textcolors.blue + "Streaming... Press Ctrl+C to stop." + textcolors.end)

    # Keep running stream until Ctrl+C
    try:
        while stream.is_active():
            pass
    except KeyboardInterrupt:
        pass

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
