# # Spotipy lib: https://github.com/plamere/spotipy
#
# import ast
# import requests
# import spotipy.util as util
# from typing import List
# from os import listdir
# from config import *
#
# base_url = 'https://api.spotify.com/v1/'
#
# def get_streamings(path: str = 'my_data') -> List[dict]:
#     files = ['my_data/' + x for x in listdir(path)
#              if x.split('.')[0][:-1] == 'StreamingHistory']
#
#     all_streamings = []
#
#     for file in files:
#         with open(file, 'r', encoding='UTF-8') as f:
#             new_streamings = ast.literal_eval(f.read())
#             all_streamings += [streaming for streaming
#                                in new_streamings]
#     return all_streamings
#
# def get_token(username, client_id, client_secret, redirect_uri,scope):
#     token = util.prompt_for_user_token(username=username,
#                                        scope=scope,
#                                        client_id=client_id,
#                                        client_secret=client_secret,
#                                        redirect_uri=redirect_uri)
#     return token
#
# def get_headers(base_url):
#     '''Performs a query on Spotify API to get a track ID.
#     See https://curl.trillworks.com/'''
#
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer ' + get_token(username, client_id,
#                               client_secret, redirect_uri, scope),
#     }
#     return headers
#
# # get id of tracks to get features
# def get_api_id(track_info: str, token: str,
#                artist: str = None) -> str:
#     '''Performs a query on Spotify API to get a track ID.
#     See https://curl.trillworks.com/'''
#
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer ' + token,
#     }
#     track_name = track_info.split("___")[0]
#     params = [
#         ('q', track_name),
#         ('type', 'track'),
#     ]
#     artist = track_info.split("___")[-1]
#     if artist:
#         params.append(('artist', artist))
#
#     try:
#         response = requests.get('https://api.spotify.com/v1/search',
#                                 headers=headers, params=params, timeout=5)
#         json = response.json()
#         results = json['tracks']['items']
#         first_result = json['tracks']['items'][0]
#         # Check if searched artist is in response as the first one isn't
#         # necessarily the right one
#         if artist:
#             for result in results:
#                 if artist.strip() == result['artists'][0]['name'].strip():
#                     track_id = result['id']
#                     return track_id
#         # If specific artist is not found from results, use the first one
#         track_id = first_result['id']
#         return track_id
#     except:
#         return None
#
# # to avoid duplicated ids that already retrived and saved
# def get_saved_ids(tracks, path: str = 'raw_output/track_ids.csv') -> dict:
#     track_ids = {track: None for track in tracks}
#     folder, filename = path.split('/')
#     if filename in listdir(folder):
#         try:
#             idd_dataframe = pd.read_csv('raw_output/track_ids.csv',
#                                         names=['name', 'idd'])
#             idd_dataframe = idd_dataframe[1:]  # removing first row
#             added_tracks = 0
#             for index, row in idd_dataframe.iterrows():
#                 if not row[1] == 'nan':  # if the id is not nan
#                     track_ids[row[0]] = row[1]  # add the id to the dict
#                     added_tracks += 1
#             print(f'Saved IDs successfully recovered for {added_tracks} tracks.')
#         except:
#             print('Error. Failed to recover saved IDs!')
#             pass
#     return track_ids
#
#
# def get_api_features(track_id: str, token: str) -> dict:
#     sp = spotipy.Spotify(auth=token)
#     try:
#         features = sp.audio_features([track_id])
#         return features[0]
#     except:
#         return None
#
# def get_album(track_id: str, token: str) -> dict:
#     sp = spotipy.Spotify(auth=token)
#     try:
#         album = sp.track(track_id)
#         album_id = album['album']['id']
#         album_name = album['album']['name']
#         return album_name, album_id
#     except:
#         return None, None
#
# def get_saved_features(tracks, path = 'raw_output/features.csv'):
#     folder, file = path.split('/')
#     track_features = {track: None for track in tracks}
#     if file in listdir(folder):
#         features_df = pd.read_csv(path, index_col = 0)
#         n_recovered_tracks = 0
#         for track in features_df.index:
#             features = features_df.loc[track, :]
#             if not features.isna().sum():          #if all the features are there
#                 track_features[track] = dict(features)
#                 n_recovered_tracks += 1
#         print(f"Added features for {n_recovered_tracks} tracks.")
#         return track_features
#     else:
#         print("Did not find features file.")
#         return track_features


# Partial library I wrote a while ago that is a wrapper for spotipy.
# I'm not particularly proud of the code so I only posted what's needed to understand
# my get_recents.py gist

import os
import spotipy.util as util

base_url = 'https://api.spotify.com/v1/'
auth_header = None


def login(base_url):
    username = 'ux6eps888djgn79vsn00f3315'
    client_id = 'ce7b531c8cf249d3b73d1e7bea6342fd'
    client_secret = '703a710a017f48048d74f6d67ec9ecf2'
    redirect_uri = 'http://localhost:7777/callback'

    # After being redirected (to a nonexistent localhost page), copy and paste the url containing the auth code
    # into the terminal and spotipy will parse the code and get the resulting OAuth token.
    token = util.prompt_for_user_token(
        username,
        'user-read-recently-played user-library-read user-modify-playback-state playlist-modify-public',
        client_id=client_id, client_secret=client_secret,
        redirect_uri=redirect_uri)
    assert token, 'Token is nil'
    auth_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    auth_header = {'Authorization': 'Bearer ' + token}
    print(f'token is', token)
    return auth_header


def format_track(json, include_duration=False):
    def assert_key(key, msg, js=None):
        if js is None: js = json
        assert key in js, msg
        return js[key]

    title = assert_key('name', 'No name key in JSON')
    artists = assert_key('artists', 'No artists key in JSON')

    assert len(artists) > 0, 'Artists length 0'
    artist = artists[0]
    name = assert_key('name', 'No name for artist', js=artist)

    id = assert_key('id', 'No id for track')

    d = {'title': '\'' + title + '\'',
         'artist': '\'' + name + '\'',
         'id': id}

    if include_duration:
        duration = assert_key('duration_ms', 'No duration for track')
        d['duration'] = duration

    return d


if auth_header is None:
    auth_header = login(base_url)