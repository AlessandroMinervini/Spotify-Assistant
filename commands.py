from playsound import playsound

# Define all the functions of Spotify Assistant:

# Modify the playback status:
# 1 - Start/resume
# 2 - Pause
# 3 - Next track
# 4 - Previous track
# 5 - Shuffle Mode
# 6 - Repeat (Track, Context, Off)
# 7 - Manage volume


def start_playback(voice_command, sp):
    default_command = 'start'
    if default_command in voice_command:
        playsound('sound/notification.mp3')
        current = sp.start_playback()


def pause(voice_command, sp):
    default_command_1 = 'stop'
    default_command_2 = 'pause'
    if default_command_1 in voice_command or default_command_2 in voice_command:
        playsound('sound/notification.mp3')
        current = sp.pause_playback()


def next_track(voice_command, sp):
    default_command = 'next track'
    if default_command in voice_command:
        playsound('sound/notification.mp3')
        current = sp.next_track()


def previous_track(voice_command, sp):
    default_command = 'previous track'
    if default_command in voice_command:
        playsound('sound/notification.mp3')
        current = sp.previous_track()


def shuffle(voice_command, sp):
    default_command_1 = 'shuffle on'
    default_command_2 = 'shuffle off'
    if default_command_1 in voice_command or default_command_2 in voice_command:
        if default_command_1 in voice_command:
            current = sp.shuffle(True)
            playsound('sound/notification.mp3')
        elif default_command_2 in voice_command:
            current = sp.shuffle(False)
            playsound('sound/notification.mp3')


def repeat(voice_command, sp):
    repeat_track = 'repeat track'
    repeat_context = 'repeat all'
    repeat_off = 'repeat off'
    if repeat_track in voice_command:
        playsound('sound/notification.mp3')
        current = sp.repeat('track')
    if repeat_context in voice_command:
        playsound('sound/notification.mp3')
        current = sp.repeat('context')
    if repeat_off in voice_command:
        playsound('sound/notification.mp3')
        current = sp.repeat('off')


def volume(voice_command, sp):
    up_volume = 'up volume'
    app_volume = 'app volume'
    low_volume = 'down volume'
    volume_app = 'volume app'
    volume_down = 'volume down'
    if up_volume in voice_command or app_volume in voice_command or volume_app in voice_command:
        playsound('sound/notification.mp3')
        sp.volume(99)
    if low_volume in voice_command or volume_down in voice_command:
        playsound('sound/notification.mp3')
        sp.volume(50)


# Search and play
# 1 - Play a track/artist
# 2 - Play an album
# 3 - Play a playlist and change the mood
# 4 - Play my saved tracks
# 5 - Play an Artist


def play_a_track(voice_command, sp):
    default_command = 'play'
    uris = []
    if 'album' not in voice_command and 'playlist' not in voice_command and 'tracks' not in voice_command:
        if default_command in voice_command:
            query = voice_command.replace('play', '')
            query = query.replace('please', '')
            query = query.replace('  ', '')
            try:
                results = sp.search(query, type='track', limit=10)
                for i, t in enumerate(results['tracks']['items']):
                    uri = t['uri']
                    uris.append(uri)
                playsound('sound/notification.mp3')
                current = sp.start_playback(uris=uris)
                if len(uris) == 0:
                    playsound('sound/no_tracks.mp3')
            except:
                playsound('sound/no_tracks.mp3')
                print('No track found')


def play_an_album(voice_command, sp):
    default_command_1 = 'play'
    default_command_2 = 'album'
    if default_command_1 in voice_command and default_command_2 in voice_command:
        query = voice_command.replace('play', '')
        query = query.replace('please', '')
        query = query.replace('album', '')
        query = query.replace('  ', '')
        try:
            results = sp.search(query, type='album', limit=1)
            for i, t in enumerate(results['albums']['items']):
                uri = t['uri']
            playsound('sound/notification.mp3')
            current = sp.start_playback(context_uri=uri)
            if len(uri) == 0:
                playsound('sound/no_albums.mp3')
        except:
            playsound('sound/no_albums.mp3')
            print('No album found')


def play_a_playlist(voice_command, sp):
    default_command_1 = 'play'
    default_command_2 = 'playlist'
    if default_command_1 in voice_command and default_command_2 in voice_command:
        query = voice_command.replace('playlist', '')
        query = query.replace('please', '')
        query = query.replace('play', '')
        query = query.replace('  ', '')
        try:
            results = sp.search(query, type='playlist', limit=1)
            for i, t in enumerate(results['playlists']['items']):
                uri = t['uri']
            playsound('sound/notification.mp3')
            current = sp.start_playback(context_uri=uri)
            if len(uri) == 0:
                playsound('sound/no_playlists.mp3')
        except:
            playsound('sound/no_playlists.mp3')
            print('No playlist found')


def play_saved_tracks(voice_command, sp):
    default_command_1 = 'play'
    default_command_2 = 'my'
    default_command_3 = 'tracks'
    uris = []
    if default_command_1 in voice_command and default_command_2 in voice_command and default_command_3 in voice_command:
        try:
            results = sp.current_user_saved_tracks()
            for item in results['items']:
                track = item['track']
                uris.append(track['uri'])
            playsound('sound/notification.mp3')
            current = sp.start_playback(uris = uris)
            if len(uris) == 0:
                playsound('sound/no_saved.mp3')
        except:
            playsound('sound/no_saved.mp3')
            print('No saved tracks')

