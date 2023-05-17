import os
import sqlalchemy
import pandas as pd
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlite3
import logging


logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)


from dotenv import load_dotenv

load_dotenv()

DATABASE_LOCATION = os.getenv('DATABASE_LOCATION')

def load_data(song_df: pd.DataFrame):
    """
    load data into database
    """

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)

    conn = sqlite3.connect('myplayedtracks.sqlite')
    cursor = conn.cursor()
    meta = MetaData(engine)
    insp = sqlalchemy.inspect(engine)
    if not insp.has_table('my_played_tracks'):
        sql_create_table = Table(
            'my_played_tracks',
            meta,
            Column('song_name', String),
            Column('artist_name', String),
            Column('played_at', String, primary_key=True),
            Column('timestamp', String)
        )
    meta.create_all()

    try:
        song_df.to_sql('my_played_tracks', engine, index=False, if_exists='append')
    except:
        logging.info('Data already exists in the database')

    conn.close()

    logging.info('Close database successfully')