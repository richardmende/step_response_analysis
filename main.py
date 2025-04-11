import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import savgol_filter
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


from numpy import exp


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
            response = t 
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



pt1_system = SystemModel(model_type='PT', order=1, parameters={'K':1.2, 'T1': 5})

calculated_response = pt1_system.step_response(time_values)




# metrics
mae = mean_absolute_error(smoothed_values_savgol, calculated_response)
mse = mean_squared_error(smoothed_values_savgol, calculated_response)
rmse = np.sqrt(mse)
nrmse = rmse / (np.max(smoothed_values_savgol) - np.min(smoothed_values_savgol))

r2 = r2_score(smoothed_values_savgol, calculated_response)
transformed_r2 = np.abs(r2 - 1)

mape = np.mean(np.abs((smoothed_values_savgol - calculated_response) / smoothed_values_savgol))
smape = np.mean(2 * np.abs(calculated_response - smoothed_values_savgol) / (np.abs(smoothed_values_savgol) + np.abs(calculated_response)))
transformed_smape = np.exp(10 * smape) - 1


quality_score = 10 * transformed_r2 + 3 * mape + 2 * mse + 2 * rmse + nrmse + transformed_smape + mae   # best performance means lowest value

print(quality_score)


plt.plot(time_values, response_values, label='real step response', color='red')
plt.plot(time_values, smoothed_values_savgol, label='smoothed step response', color='green')
plt.plot(time_values, calculated_response, label='calculated step response', color='blue')
plt.xlabel('time [s]')
plt.ylabel('step response x(t)')
plt.title('comparison between real and calculated step response')
plt.legend()
plt.show()
