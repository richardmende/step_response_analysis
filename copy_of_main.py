import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp

from scipy.signal import savgol_filter
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



class SystemModel:
    def __init__(self, model_type, order, parameters):
        self.model_type = model_type    # PT or IT
        self.order = order              # 1 / 2 / 3 / 4, dependent on the number of delay time constants of the system
        self.parameters = parameters    # K / T1 / T2 / ...
    

    def step_response(self, t):

        if self.model_type == 'PT':
            response = self.parameters['K']
            for i in range(1, self.order + 1):
                T = self.parameters[f'T{i}']
                response *= (1 - exp(-t / T))
            return response
        
        elif self.model_type == 'IT':
            response = np.copy(t)
            for i in range(1, self.order + 1):
                T = self.parameters[f'T{i}']
                response *= (1 - exp(-t / T))
            return response
        
        else:
            raise ValueError("Unknown description!")


csv_file_path = 'real_pt1_response.csv'

df = pd.read_csv(csv_file_path)

time_values = df['Time'].values
response_values = df['Response'].values

smoothed_values_savgol = savgol_filter(response_values, window_length=151, polyorder=3)


model_types = ['PT', 'IT']
max_order = 3

best_overall_score = float('inf')
best_overall_model = None
best_overall_params = None



for model_type in model_types:
    for order in range(1, max_order + 1):
        print(f"Optimizing {model_type}{order}...")

        def objective(params):
            param_dict = {'K': params[0]}
            for i in range(1, order + 1):
                param_dict[f'T{i}'] = params[i]

            try:
                model = SystemModel(model_type=model_type, order=order, parameters=param_dict)
                response = model.step_response(time_values)
            except:
                return np.inf
            

            mae = mean_absolute_error(smoothed_values_savgol, response)
            mse = mean_squared_error(smoothed_values_savgol, response)
            rmse = np.sqrt(mse)
            nrmse = rmse / (np.max(smoothed_values_savgol) - np.min(smoothed_values_savgol))
            r2 = r2_score(smoothed_values_savgol, response)
            transformed_r2 = np.abs(r2 - 1)
            mape = np.mean(np.abs((smoothed_values_savgol - response) / smoothed_values_savgol))
            smape = np.mean(2 * np.abs(response - smoothed_values_savgol) /
                            (np.abs(smoothed_values_savgol) + np.abs(response)))
            transformed_smape = np.exp(10 * smape) - 1
            

            score = (
                10 * transformed_r2 +
                3 * mape +
                2 * mse +
                2 * rmse +
                nrmse +
                transformed_smape +
                mae
            )
            
            return score

        x0 = [1.0] * (order + 1)
        bounds = [(0.001, 2)] + [(0.2, time_values[-1])] * order

        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

        score = result.fun
        params = result.x

        print(f"Score: {score:.4f}, Params: {params}")

        if score < best_overall_score:
            best_overall_score = score
            best_overall_model = (model_type, order)
            best_overall_params = params



print("\nBest model found:")
print(f"Type: {best_overall_model[0]}{best_overall_model[1]}")
print(f"Params: {best_overall_params}")
print(f"Score: {best_overall_score:.4f}")

param_dict = {'K': best_overall_params[0]}
for i in range(1, best_overall_model[1] + 1):
    param_dict[f'T{i}'] = best_overall_params[i]

best_model = SystemModel(
    model_type=best_overall_model[0],
    order=best_overall_model[1],
    parameters=param_dict
)
best_response = best_model.step_response(time_values)



plt.plot(time_values, smoothed_values_savgol, label='step response (smoothed)', color='green')
plt.plot(time_values, best_response, label=f'{best_overall_model[0]}{best_overall_model[1]} fit', color='blue')
plt.xlabel('time [s]')
plt.ylabel('step response x(t)')
plt.title('Best system model fit')
plt.legend()
plt.show()
