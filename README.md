# Spotify Assistant
Spotify Assistant is a voice assistant designed for Spotify with the recognition of the user's face to suggest a track or an artist.

## Implementation
The language used is Python and to develop the assistant are used the technologies:
- Spotify Web API (Spotipy) - https://spotipy.readthedocs.io/en/latest/
- Speech recognition - https://github.com/Uberi/speech_recognition
- Face recognition - https://github.com/ageitgey/face_recognition
- PyQt5

## How does it works?
### Speech recognition
The interaction with the assistant is through two step:
- The waiting for the wake word
- The waiting for the command requested from user

<p align="center">
  <img width="400" height="220" src="https://github.com/AlessandroMinervini/Spotify-Assistant/blob/master/imagestoreadme/speechflow.jpg">
</p>

### Example of interaction between user and the assistant

<p align="center">
  <img width="400" height="350" src="https://github.com/AlessandroMinervini/Spotify-Assistant/blob/master/imagestoreadme/flow.png">
</p>

## Commands available

- Start
- Stop/pause
- Next track
- Previous track
- Repeat track/all/off
- Shuffle on/off
- Down/up volume
- Play track / artist / playlist / mood / saved tracks
- Switch language, english/italian

## Now launch the assistant!

### Requirements


| Software  | Version | Required|
| ------------- | ------------- |  ------------- |
| Python | >= 3.5  | Yes    |
| Numpy  | Tested on 1.13 |    Yes     |
| Scipy  | >= 1.0  | Yes   |
| PyQt5 | >= 5.9.1  | Yes
| qdarkstyle  | >= 2.6.5  |Optional |






