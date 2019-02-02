from gtts import gTTS
#from playsound import playsound
import pygame

# Configure gTTs (Speech to Text)

def speech_command(text):
    pygame.init()
    text = str(text)
    tts = gTTS(text, lang='en')
    tts.save('sound/speech.mp3')
    pygame.mixer.music.load("sound/speech.mp3")
    pygame.mixer.music.play()
    #playsound('sound/speech.mp3')

