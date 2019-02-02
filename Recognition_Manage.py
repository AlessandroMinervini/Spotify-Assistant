import os, sys
import spotipy
import commands
import CheckRec
import spotipy.util as util
from Recognition import audio_recognition
from json.decoder import JSONDecodeError
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gtts import gTTS
from playsound import playsound


class Rec_Thread(QThread):
    def __init__(self):
        super().__init__()
        self.active = False
        self.name = 'Alessandro'
        self.username = '1166734650'
        self.client_id = '0cda611f9fce4934b3f3c3cda8ff5aed'
        self.client_secret = '145e5f6f56794a5aa224625c4f86341d'
        self.redirect_uri = 'https://www.google.it/'
        self.scope = 'user-modify-playback-state user-library-read user-read-playback-state'
        self.open_cmd = ''
        self.lang = 'en'
        # Erase cache and prompt for user permission
        try:
            self.token = util.prompt_for_user_token(self.username, self.scope, self.client_id, self.client_secret, self.redirect_uri )
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(self.username, self.scope, self.client_id,self.client_secret,self.redirect_uri)

        # Configure Spotify
        self.sp = spotipy.Spotify(auth=self.token)

    def run(self):
        self.active = True
        while self.active:
            try:
                self.open_cmd = ''
                self.open_loop()
                playsound('sound/listening.mp3')
                correct_cmd = audio_recognition(True, self.lang)
                commands.start_playback(correct_cmd, self.sp)
                commands.pause(correct_cmd, self.sp)
                commands.next_track(correct_cmd, self.sp)
                commands.previous_track(correct_cmd, self.sp)
                commands.repeat(correct_cmd, self.sp)
                commands.shuffle(correct_cmd, self.sp)
                commands.volume(correct_cmd, self.sp)
                commands.play_a_track(correct_cmd, self.sp)
                commands.play_an_album(correct_cmd, self.sp)
                commands.play_a_playlist(correct_cmd, self.sp)
                commands.play_saved_tracks(correct_cmd, self.sp)
                self.language(correct_cmd)
            except:
                print('Invalid command or timeout')

    def open_loop(self):
        while 'spotify' not in self.open_cmd.lower():
            self.open_cmd = audio_recognition(False, 'en')

    def listen_loop(self):
        self.start()

    def deactivate(self):
        """ Method called to stop and deactivate this Thread """
        self.active = False
        self.quit()
        if self.isRunning():
            self.quit()

    def language(self, vocal_command):
        default_command_1 = 'english language'
        default_command_2 = 'italian language'
        status_lang = 'language'
        if default_command_1 in vocal_command.lower() or default_command_2 in vocal_command.lower() or status_lang in vocal_command.lower():
            if default_command_1.lower() in vocal_command:
                self.lang = 'en'
                playsound('sound/notification.mp3')
            elif default_command_2.lower() in vocal_command:
                self.lang = 'it-IT'
                playsound('sound/notification.mp3')
            elif status_lang in vocal_command:
                if self.lang == 'en':
                    playsound('sound/en_lang.mp3')
                else:
                    playsound('sound/it_lang.mp3')



