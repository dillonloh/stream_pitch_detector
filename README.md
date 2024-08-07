# Singing Learning Aid Swiss Knife (name pending improvements)

This repo essentially aims to be the ultimate open-source Karaoke aid that provides provides some useful tools for anyone who is learning to sing (like me!)

## Description

Features include:

1) Transcribing songs to check if you're are on pitch/what note you need to sing
2) Get the vocal range needed for a song with analysis on different parts of it (verse, chorus, bridge etc.)
3) Pitch shift songs to fall within your tessitura
4) Check your singing pitch/tempo against song target pitch/tempo
5) Do all of the above but with live streaming audio from their system output without need for a microphone
6) Do all of the above but with live streaming audio from sites like Youtube/Spotify etc. without the need to download an mp3 etc. and plugging it into Audacity first.

## Getting Started

### Dependencies

You need to either be on Linux (Ubuntu 22.04 tested) or Windows (>Windows 10 necessary due to WASAPI requirement)
Dependencies can be installed via pip and the requirements.txt file.

To setup:
```bash
git clone https://github.com/dillonloh/stream_pitch_detector.git
cd stream_pitch_detector # project root
cd stream_pitch_detector # source root
pip install -r requirements.txt # install dependencies
```

### Executing program

To try it out, simply run the main.py file in the source code root. You can modify the top constant variables to suit your needs.
```
cd stream_pitch_detector # you should now be in stream_pitch_detector/stream_pitch_detector/
python main.py
```

## Authors

Contributors names and contact info

Dillon Loh (loh.dillon@gmail.com)


## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

* [aubio](https://aubio.org/) for the pitch detection tools
* HarkMusic Singapore for building my love of (learning to) sing
