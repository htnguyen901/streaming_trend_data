import os
import json as json_func
from os.path import join, isfile
from data_collection import sputil as sp
import pandas as pd
import requests as r
from datetime import datetime

path = os.getcwd()
raw_csv_folder = path + '/raw_output/'
dbt_seed_folder = path + '/dbt/data/'
print(raw_csv_folder)

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

        #get track features
        id = track['id']
        response = r.get(sp.base_url + 'audio-features/' + id ,headers=sp.auth_header)
        json = response.json()
        track_features = json
        track['features'] =json_func.dumps(track_features)

        played_at = track_obj['played_at']
        played_at = datetime.strptime(played_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        track['timestamp'] = played_at.timestamp()
        track['created_at'] = datetime.now().timestamp()

        tracks.append(track)

    print('Fetched %d new tracks' % len(tracks))

    # reorder the DataFrame so that it is in chronological order
    df = pd.DataFrame(tracks).iloc[::-1]

    # if we already have a recently_played.csv file,
    # then open it in append mode so that previous history isn't overwritten
    # and header=False so that the header doesn't appear halfway through the file

    recent_fname = join(root_dir,raw_csv_folder, 'recently_played.csv')
    dbt_fname = join(root_dir,dbt_seed_folder, 'recently_played.csv')
    fmode = 'w'
    inc_header = True

    if isfile(recent_fname) or isfile(dbt_fname):
        fmode = 'a'
        inc_header = False

    #save file to raw folder for backup
    with open(recent_fname,fmode, errors='ignore') as f:
        df.to_csv(f, header=inc_header, sep=',', line_terminator='\n', encoding='utf-8')

    #also save file to dbt data folder

    with open(dbt_fname, fmode, encoding='utf-8', errors='ignore') as f:
        df.to_csv(f, header=inc_header, sep=',', line_terminator='\n', encoding='utf-8')

if __name__ == '__main__':
    get_recent()