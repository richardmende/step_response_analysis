import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import savgol_filter
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from general_systems_description import SystemModel
from load_filter import edit_csv
from quality_score import compute_quality_score



time, stepresponse = edit_csv('real_pt1_response.csv')

calculated_stepresponse = 1
