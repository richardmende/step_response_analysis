import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



def compute_quality_score(y_real, y_model):

    mae = mean_absolute_error(y_real, y_model)
    mse = mean_squared_error(y_real, y_model)
    rmse = np.sqrt(mse)
    nrmse = rmse / (np.max(y_real) - np.min(y_real))
    
    r2 = r2_score(y_real, y_model)
    transformed_r2 = np.abs(r2 - 1)

    mape = np.mean(np.abs((y_real - y_model) / y_real))
    smape = np.mean(2 * np.abs(y_model - y_real) / (np.abs(y_real) + np.abs(y_model)))
    transformed_smape = np.exp(10 * smape) - 1

    quality_score = 10 * transformed_r2 + 3 * mape + 2 * mse + 2 * rmse + nrmse + transformed_smape + mae


    return quality_score
