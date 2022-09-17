import os
import spotipy
import spotipy.util as util
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from config import *

base_url = 'https://api.spotify.com/v1/'
auth_header = None


def login(base_url):
    # username = 'ux6eps888djgn79vsn00f3315'
    # client_id = 'ce7b531c8cf249d3b73d1e7bea6342fd'
    # client_secret = '703a710a017f48048d74f6d67ec9ecf2'
    # redirect_uri = 'http://localhost:7777/callback'

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
        #print(json)
        if js is None:
            js = json['track']
        assert key in js, msg
        return js[key]

    title = assert_key('name', 'No name key in JSON')
    artists = assert_key('artists', 'No artists key in JSON')
    track_uri = assert_key('uri', 'No track uri key in JSON')

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

    d['popularity'] = assert_key('popularity', 'No popularity for track')

    return d


if auth_header is None:
    auth_header = login(base_url)