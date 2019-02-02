import speech_recognition as sr
from subprocess import call
import CheckRec
from playsound import playsound
import speech_text as speech


def audio_recognition(status, language):
    # obtain audio from the microphone
    listening = status
    r = sr.Recognizer()
    lang = language

    with sr.Microphone(device_index=0) as source:
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        if listening:
            playsound('sound/siri.mp3')
        print("Spotify Assistant is listening...")
        if not listening:
            audio = r.listen(source, timeout=5.0)
        if listening:
            audio = r.listen(source, timeout=10.0)

        try:
            print("Spotify Assistant thinks you said " + r.recognize_google(audio, language=lang))

            if listening and validate_command(r.recognize_google(audio, language=lang)):
                speech.speech_command(r.recognize_google(audio, language=lang))
            else:
                if listening:
                    while not validate_command(r.recognize_google(audio, language=lang).lower()):
                        playsound('sound/repeat.mp3')
                        print("Spotify Assistant is listening...")
                        audio = r.listen(source, timeout=10.0)
                        print("Spotify Assistant thinks you said " + r.recognize_google(audio, language=lang))

                    speech.speech_command(r.recognize_google(audio, language=lang))

            return r.recognize_google(audio, language=lang).lower()

        except sr.UnknownValueError:
            print("Spotify Assistant could not understand audio")
            #playsound('sound/siri_close.mp3')

        except sr.RequestError as e:
            print("Could not request results from Spotify Assistant Recognition service; {0}".format(e))

    return r.recognize_google(audio, language=lang).lower()


def validate_command(command):
    correct_commands = ['start', 'stop', 'next track', 'previous track', 'repeat', 'shuffle on', 'shuffle off', 'up volume',
                        'volume up', 'play', 'down volume', 'volume down', 'play album', 'play playlist', 'play my tracks',
                        'suggest me', 'app volume', 'volume app', 'english language', 'italian language', 'language']
    cmd, correct_cmd = CheckRec.replace_type(correct_commands, command.lower())
    for s in correct_commands:
        if s in command:
            return True
