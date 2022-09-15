# from data_collection import data_crawling
# import os
# from os.path import join, isfile
# import pandas as pd
# from time import sleep
# from datetime import datetime
# import requests
# from config import *
#
# def main():
#     # recover streamings data_crawling
#     token = data_crawling.get_token(username, client_id,
#                               client_secret, redirect_uri, scope)
#
#     # streamings = data_crawling.get_streamings()
#     # print(f'Recovered {len(streamings)} streamings.')
#     #
#     # # getting a list of unique tracks in our data_crawling
#     # # Add artist names too as multiple artist can have same song name
#     # tracks = set([f"{streaming['trackName']}___{streaming['artistName']}" for streaming in streamings])
#     # print(f'Discovered {len(tracks)} unique tracks.')
#     #
#     # # getting saved ids for tracks
#     # track_ids = data_crawling.get_saved_ids(tracks)
#     #
#     # # checking tracks that still miss idd
#     # tracks_missing_idd = len([track for track in tracks if track_ids.get(track) is None])
#     # print(f'There are {tracks_missing_idd} tracks missing ID.')
#     #
#     # if tracks_missing_idd > 0:
#     #     # using spotify API to recover track ids
#     #     # note: this methods works only for tracks.
#     #     # podcasts and other items will be ignored.
#     #     print('Connecting to Spotify to recover tracks IDs.')
#     #     sleep(3)
#     #     id_length = 22
#     #     for track, idd in track_ids.items():
#     #         if idd is None:
#     #             try:
#     #                 found_idd = data_crawling.get_api_id(track, token)
#     #                 track_ids[track] = found_idd
#     #                 print(f"{found_idd:<{id_length}} : {', '.join(track.split('___'))}")
#     #             except:
#     #                 pass
#     #
#     #     # how many tracks did we identify?
#     #     identified_tracks = [track for track in track_ids
#     #                          if track_ids[track] is not None]
#     #     print(f'Successfully recovered the ID of {len(identified_tracks)} tracks.')
#     #
#     #     # how many items did we fail to identify?
#     #     n_tracks_without_id = len(track_ids) - len(identified_tracks)
#     #     print(f"Failed to identify {n_tracks_without_id} items. "
#     #           "However, some of these may not be tracks (e.g. podcasts).")
#     #
#     #     # using pandas to save tracks ids (so we don't have to API them in the future)
#     #     ids_path = 'raw_output/track_ids.csv'
#     #     ids_dataframe = pd.DataFrame.from_dict(track_ids,
#     #                                            orient='index')
#     #     ids_dataframe.to_csv(ids_path)
#     #     print(f'track ids saved to {ids_path}.')
#     #
#     # # recovering saved features
#     # track_features = data_crawling.get_saved_features(tracks)
#     # tracks_without_features = [track for track in tracks if track_features.get(track) is None]
#     # print(f"There are still {len(tracks_without_features)} tracks without features.")
#     # path = 'raw_output/features.csv'
#     #
#     # # connecting to spotify API to retrieve missing features
#     # if len(tracks_without_features):
#     #     print('Connecting to Spotify to extract features...')
#     #     acquired = 0
#     #     for track, idd in track_ids.items():
#     #         if idd is not None and track in tracks_without_features:
#     #             try:
#     #                 features = data_crawling.get_api_features(idd, token)
#     #                 track_features[track] = features
#     #                 features['albumName'], features['albumID'] = data_crawling.get_album(idd, token)
#     #                 if features:
#     #                     acquired += 1
#     #                     print(f"Acquired features: {', '.join(track.split('___'))}. Total: {acquired}")
#     #             except:
#     #                 features = None
#     #     tracks_without_features = [track for track in tracks if track_features.get(track) is None]
#     #     print(f'Successfully recovered features of {acquired} tracks.')
#     #     if len(tracks_without_features):
#     #         print(f'Failed to identify {len(tracks_without_features)} items. Some of these may not be tracks.')
#     #
#     #     # saving features
#     #     features_dataframe = pd.DataFrame(track_features).T
#     #     features_dataframe.to_csv(path)
#     #     print(f'Saved features to {path}.')
#     #
#     # # joining features and streamings
#     # print('Adding features to streamings...')
#     # streamings_with_features = []
#     # for streaming in sorted(streamings, key=lambda x: x['endTime']):
#     #     track = streaming['trackName'] + "___" + streaming['artistName']
#     #     features = track_features.get(track)
#     #     if features:
#     #         streamings_with_features.append({'name': track, **streaming, **features})
#     # print(f'Added features to {len(streamings_with_features)} streamings.')
#     # print('Saving streamings...')
#     # df_final = pd.DataFrame(streamings_with_features)
#     # df_final.to_csv('raw_output/final.csv')
#     # perc_featured = round(len(streamings_with_features) / len(streamings) if len(streamings) else 0 * 100, 2)
#     # print(f"Done! Percentage of streamings with features: {perc_featured}%.")
#     # print("Run the script again to try getting more information from Spotify.")
#
#
# if __name__ == '__main__':
#     main()

# To run as a local cron job, edit your crontab like so:
#
# SPOTIPY_USER_ID=<redacted>
# SPOTIPY_CLIENT_ID=<redacted>
# SPOTIPY_CLIENT_SECRET=<redacted>
# script_path=<redacted>
# SPPATH=$script_path
# python_path=/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
#
# PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
#
# 0 8 * * * cd $script_path && $python_path get_recents.py >> $script_path/cron_log.log
# 0 12 * * * cd $script_path && $python_path get_recents.py >> $script_path/cron_log.log
# 0 16 * * * cd $script_path && $python_path get_recents.py >> $script_path/cron_log.log
# 0 20 * * * cd $script_path && $python_path get_recents.py >> $script_path/cron_log.log
# 0 23 * * * cd $script_path && $python_path get_recents.py >> $script_path/cron_log.log

# Take a look at https://gist.github.com/SamL98/ff1448aa1f92bf671a549357449192e5 if you want to learn about sputil
import os
from os.path import join, isfile
from data_collection import sputil as sp
import pandas as pd
import requests as r
from datetime import datetime


def get_recent():
    root_dir = os.getcwd()
    params = {'limit': '50'}

    # .next.txt stores a timestamp of the last listened track fetched
    # we can pass this timestamp to the Spotify API and we will only
    # get songs listened to after this timestamp

    next_fname = join(root_dir, '.next.txt')
    if isfile(next_fname):
        with open(next_fname) as f:
            params['after'] = int(f.read())

    response = r.get(
        sp.base_url + 'me/player/recently-played',
        params=params,
        headers=sp.auth_header)
    print(response.text)

    assert response.status_code == 200, 'Request responded with non-200 status %d' % r.status_code

    assert response.json, 'No json from request'
    json = response.json()

    assert 'cursors' in json, 'No cursor object in json'
    cursor_obj = json['cursors']

    assert 'after' in cursor_obj, 'No after key in cursor json'
    after = cursor_obj['after']

    with open(next_fname, 'w') as f:
        f.write(after)

    assert 'items' in json, 'No item key in json'

    tracks = []
    for track_obj in json['items']:
        track = sp.format_track(track_obj, True)

        played_at = track_obj['played_at']
        played_at = datetime.strptime(played_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        track['timestamp'] = played_at.timestamp()

        tracks.append(track)

    print('Fetched %d new tracks' % len(tracks))

    # reorder the DataFrame so that it is in chronological order
    df = pd.DataFrame(tracks).iloc[::-1]

    # if we already have a recently_played.csv file,
    # then open it in append mode so that previous history isn't overwritten
    # and header=False so that the header doesn't appear halfway through the file

    recent_fname = join(root_dir, 'recently_played.csv')
    fmode = 'w'
    inc_header = True

    if isfile(recent_fname):
        fmode = 'a'
        inc_header = False

    with open(recent_fname, fmode) as f:
        df.to_csv(f, header=inc_header)


if __name__ == '__main__':
    get_recent()