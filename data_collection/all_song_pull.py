import os
import json as json_func
from os.path import join, isfile
import sputil as sp
import pandas as pd
import requests
from datetime import datetime
from sputil import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.chdir('..')
path = os.getcwd()
raw_csv_folder = path + '/raw_output/'
dbt_seed_folder = path + '/dbt/data/'
os.chdir('data_collection')
print(raw_csv_folder)

# Get liked playlists and all songs from those
def get_tracks_playlist():
    root_dir = os.getcwd()
    params = {'limit': '50'}

    print('get_track_playlist')

    # .next.txt stores a timestamp of the last listened track fetched
    # we can pass this timestamp to the Spotify API and we will only
    # get songs listened to after this timestamp

    # response = requests.get(
    #     sp.base_url + 'me/playlists',
    #     params=params,
    #     headers=sp.auth_header)

    spo = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    ))
    print('done spo')
    json = spo.current_user_playlists(limit=50, offset=0)
    print('done get json')
    playlists = []

    for playlist_obj in json['items']:

        if playlist_obj['name'] == 'spotify-recommender-tracks':
            continue

        playlist_id = playlist_obj['id']
        playlist_desc = playlist_obj['description']
        playlist_name = playlist_obj['name']

        playlist = {'id': '\'' + playlist_id + '\'',
                    'name': '\'' + playlist_name + '\'',
                    'description': playlist_desc}
        print('done get playlist object')
        response = requests.get(sp.base_url + 'playlists/' + playlist_id + '/tracks' ,headers=sp.auth_header)
        #json = spo.playlist_items(playlist_id=playlist_id)
        json = response.json()
        playlist_tracks = json

        tracks = []
        for track_obj in playlist_tracks['items']:
            if track_obj['track'] is None:
                continue

            track = sp.format_track(track_obj, True)
            print('done format track')
            #get genres
            track_ = track_obj['track']
            artist = track_['artists']
            artist_id = artist[0]['id']
            #response = requests.get(sp.base_url + 'artists/' + artist_id, headers=sp.auth_header)
            #print(response.text)
            #artist_obj = response.json
            json_artist = spo.artist(artist_id=artist_id)
            print(json_artist)
            artist_obj = json_artist
            track['genres'] = get_artist_genre(artist_obj)

            # get track features
            track['playlist'] = playlist_name
            id = track['id']
            #response = requests.get(sp.base_url + 'audio-features/' + id, headers=sp.auth_header)
            json_features = spo.audio_features(tracks=[id])
            #json = response.json()
            track_features = json_features
            track['features'] = json_func.dumps(track_features)
            track['created_at'] = datetime.now().timestamp()

            tracks.append(track)
        print(f'Fetched {len(tracks)} tracks from playlist: {playlist_name}')

        # reorder the DataFrame so that it is in chronological order
        df = pd.DataFrame(tracks).iloc[::-1]

        # if we already have a recently_played.csv file,
        # then open it in append mode so that previous history isn't overwritten
        # and header=False so that the header doesn't appear halfway through the file

        recent_fname = join(path, raw_csv_folder, 'tracks_from_playlists.csv')
        dbt_fname = join(path, dbt_seed_folder, 'tracks_from_playlists.csv')
        fmode = 'w'
        inc_header = True

        if isfile(recent_fname) or isfile(dbt_fname):
            fmode = 'a'
            inc_header = False

        # save file to raw folder for backup
        with open(recent_fname, fmode, errors='ignore') as f:
            df.to_csv(f, header=inc_header, sep=',', line_terminator='\n', encoding='utf-8')

        # also save file to dbt data folder

        with open(dbt_fname, fmode, encoding='utf-8', errors='ignore') as f:
            df.to_csv(f, header=inc_header, sep=',', line_terminator='\n', encoding='utf-8')

        playlists.append(playlist)
    df_playlists = pd.DataFrame(playlists)

    with open(path+'/raw_output/liked_playlist.csv', 'w', encoding='utf-8', errors='ignore') as f:
        df_playlists.to_csv(f, header=True, sep=',', line_terminator='\n', encoding='utf-8')

    with open(path+'/dbt/data/liked_playlist.csv', 'w', encoding='utf-8', errors='ignore') as f:
        df_playlists.to_csv(f, header=True, sep=',', line_terminator='\n', encoding='utf-8')

    print('Fetched %d playlists' % len(playlists))

get_tracks_playlist()

