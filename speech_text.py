from gtts import gTTS
from playsound import playsound

# Configure gTTs (Speech to Text)

def speech_command(text):
    text = str(text)
    tts = gTTS(text, lang='en')
    tts.save('sound/speech.mp3')
    playsound('sound/speech.mp3')

