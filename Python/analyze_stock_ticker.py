import os
import pandas as pd
import numpy as np


def read_file(csv_file: os.PathLike) -> pd.DataFrame:
    data = pd.read_csv(csv_file, index_col="Date", parse_dates=["Date"])
    data.sort_index(inplace=True)
    data['Gain'] = data['Close'] - data['Open']
    data['Direction'] = ['Up' if gain > 0 else "Down" for gain in data['Gain']]
    return data


def generate_streak_info(frame):
    data = frame['Direction'].to_frame()
    data['start_of_streak'] = data['Direction'].ne(data['Direction'].shift())
    data['streak_id'] = data.start_of_streak.cumsum()
    data['streak_counter'] = data.groupby('streak_id').cumcount() + 1
    days_with_streaks = pd.concat([frame, data['streak_counter']], axis=1)

    return days_with_streaks
