import pandas as pd

from scipy.signal import savgol_filter



def edit_csv(csv_file_path):

    df = pd.read_csv(csv_file_path)

    time_values = df['Time'].values
    response_values = df['Response'].values

    smoothed_values_savgol = savgol_filter(response_values, window_length=151, polyorder=3)


    return time_values, smoothed_values_savgol
