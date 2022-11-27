import pandas as pd
import spotipy
import yaml
from spotipy.oauth2 import SpotifyOAuth
import sputil
from config import *
from data_function import offset_api_limit, get_artists_df, get_tracks_df, get_track_audio_df, get_all_playlist_tracks_df, get_recommendations

# https://developer.spotify.com/web-api/using-scopes/
scope = "user-library-read user-follow-read user-top-read playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id, client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
))



# Spotify API calls and data manipulation
# Save for later to be quickly read by multiple workflows
print("Getting, transforming, and saving top artist data...")
top_artists = offset_api_limit(sp, sp.current_user_top_artists())
top_artists_df = get_artists_df(top_artists)
top_artists_df.to_pickle("spotify/top_artists.pkl", protocol=4)

print("Getting, transforming, and saving followed artist data...")
followed_artists = offset_api_limit(sp, sp.current_user_followed_artists())
followed_artists_df = get_artists_df(followed_artists)
followed_artists_df.to_pickle("spotify/followed_artists.pkl", protocol=4)

print("Getting, transforming, and saving top track data...")
top_tracks = offset_api_limit(sp, sp.current_user_top_tracks())
top_tracks_df = get_tracks_df(top_tracks)
top_tracks_df = get_track_audio_df(sp, top_tracks_df)
top_tracks_df.to_pickle("spotify/top_tracks.pkl", protocol=4)

print("Getting, transforming, and saving saved track data...")
saved_tracks = offset_api_limit(sp, sp.current_user_saved_tracks())
saved_tracks_df = get_tracks_df(saved_tracks)
saved_tracks_df = get_track_audio_df(sp, saved_tracks_df)
saved_tracks_df.to_pickle("spotify/saved_tracks.pkl", protocol=4)

liked_playlist_tracks = pd.read_csv('../raw_output/tracks_from_playlists.csv')

print("Getting, transforming, and saving tracks recommendations...")
# Define a sample playlists to yield tracks to get recommendations for, 20 recommendations per track
recommendation_tracks = get_recommendations(sp, liked_playlist_tracks[liked_playlist_tracks['playlist'].isin(
    ["Happy Folk", "Morning Motivation"
        # , "On Repeat", "Soft Pop Hits", "Hit Rewind", "Chill Hits", "Mood Booster"
     ])].drop_duplicates(subset='id', keep="first")['id'].tolist())
print('Done getting tracks, start formatting tracks to pkl file')
recommendation_tracks_df = get_tracks_df(recommendation_tracks)
print(len(recommendation_tracks_df))
print('Getting track audio')
recommendation_tracks_df = get_track_audio_df(sp, recommendation_tracks_df)
recommendation_tracks_df.to_pickle("spotify/recommendation_tracks.pkl", protocol=4)
