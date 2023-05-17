import os
import pandas as pd
import requests
import datetime
from datetime import timedelta
import logging
from dotenv import load_dotenv


logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

load_dotenv()

DATABASE_LOCATION = os.getenv('DATABASE_LOCATION')

USER_ID = os.getenv('USER_ID')

TOKEN = os.getenv('TOKEN')

def extract_data():
    """
    Function that allows the download of information from
    Spotify
    """


    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }


    try:
        r = requests.get(
            f"https://api.spotify.com/v1/me/player/recently-played",
            headers=headers)
    except:
        raise Exception(f'The Spotify request went wrong')

    if r.status_code != 200:
        raise Exception(f'Something in the Spotify request went wrong: {r.status_code}')


    data = r.json()


    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []


        today = datetime.datetime.now()

      yesterday = today - timedelta(days=1)


    for song in data['items']:
        if yesterday.strftime('%Y-%m-%d') == song['played_at'][0:10]:
            # We just want to grab songs from yesterday
            song_names.append(song['track']['name'])
            artist_names.append(song['track']['album']['artists'][0]['name'])

            played_at_list.append(song['played_at'])
            timestamps.append(song['played_at'][0:10])


    song_dict = {
        'song_name': song_names,
        'artist_name': artist_names,
        'played_at': played_at_list,
        'timestamp': timestamps
    }


    song_df = pd.DataFrame(
        song_dict,
        columns=['song_name', 'artist_name', 'played_at', 'timestamp']
    )

    logging.info(song_df)

    return song_df