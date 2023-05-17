import pandas as pd
import datetime

def check_if_valid_data(df: pd.DataFrame):
    """
    valid format
    """

    if df.empty:
        print('No songs in the past 24hs!')
        return False

    if not pd.Series(df['played_at']).is_unique:
        raise Exception('Primary key check is violated!')

    if df.isnull().values.any():
        raise Exception('Null values!')

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception('At least one song does not come from the last 24 hourse')