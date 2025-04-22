import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp
from scipy.signal import savgol_filter
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from functions.calculate_characteristic_values import calculate_characteristic_value_for_every_method



def step_response(model_type, order, parameters, t):
    
    if model_type == 'PT':
        if order == 1:
            savgol = round(len(t) / 10)
        elif order >= 2:
            savgol = round(len(t) / 3)
    elif model_type == 'IT':
        savgol = round(t[-1] / 3)

    if savgol % 2 == 0:
        savgol += 1

    if model_type == 'PT':
        response = parameters['K']
        for i in range(1, order + 1):
            T = parameters[f'T{i}']
            response *= (1 - np.exp(-t / T))
        return response, savgol
    
    elif model_type == 'IT':
        response = np.copy(t)
        for i in range(1, order + 1):
            T = parameters[f'T{i}']
            response *= np.clip((1 - np.exp(-t / T)), 0, 1) 
        return response, savgol
    
    else:
        raise ValueError("Unknown description!")

def procedure():
    csv_file_path = 'data_for_pt_systems/real_pt1_response.csv'
    df = pd.read_csv(csv_file_path)

    time_values = df['Time'].values
    response_values = -df['Response'].values
    step_values = df['Step Response'].values

    max_value = np.max(response_values)
    min_value = np.min(response_values)


    model_types = ['PT', 'IT']
    best_overall_score = float('inf')
    best_overall_model = None
    best_overall_params = None
    best_window_length_for_savgol = None

    max_order = 20

    for model_type in model_types:

        skip_model_type = False  # cancel flag

        for order in range(1, max_order + 1):
            print(f"\nOptimizing {model_type}{order} ...")

            def objective(params):
                if model_type == 'PT':
                    param_dict = {'K': params[0]}
                    for i in range(1, order + 1):
                        param_dict[f'T{i}'] = params[i]
                elif model_type == 'IT':
                    param_dict = {}
                    for i in range(order):
                        param_dict[f'T{i+1}'] = params[i]
                else:
                    return np.inf

                try:
                    response, window_length_for_savgol = step_response(model_type=model_type, order=order, parameters=param_dict, t=time_values)
                except:
                    return np.inf

                smoothed_values_savgol = savgol_filter(response_values, window_length=window_length_for_savgol, polyorder=3)

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


            if model_type == 'PT':
                x0 = [1.0] + [0.5 * time_values[-1] / (max_order - n + 1) for n in range(1, order + 1)]
                if abs(max_value) >= abs(min_value):
                    bounds = [(min_value, 2*max_value)] + [(time_values[1], time_values[-1])] * order
                else:
                    bounds = [(2*min_value, max_value)] + [(time_values[1], time_values[-1])] * order
            
            if model_type == 'IT':
                x0 = [((n / (order + 1)) ** 1.5) * time_values[-1] for n in range(1, order + 1)]
                bounds = [(time_values[1], time_values[-1])] * order

            result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

            score = result.fun
            params = result.x

            print(f"Score: {score:.4f} \nParams: {params}")

            # early cancel loop
            if score > 100000:
                print(f"\nScore for {model_type}1 exceeds 100000. Skipping all further {model_type}-models.")
                skip_model_type = True  # cancel this model type
                break

            if score < best_overall_score:
                best_overall_score = score
                best_overall_model = (model_type, order)
                best_overall_params = params


    best_fitting_model_type = best_overall_model[0]
    best_fitting_order = best_overall_model[1]


    print("\n\nBest model found")
    print(f"Type: {best_fitting_model_type}{best_fitting_order}")
    print(f"Params: {best_overall_params}")
    print(f"Score: {best_overall_score:.4f}\n")



    if best_fitting_model_type == 'PT':
        param_dict = {'K': best_overall_params[0]}
        for i in range(1, best_fitting_order + 1):
            param_dict[f'T{i}'] = best_overall_params[i]
    elif best_fitting_model_type == 'IT':
        param_dict = {}
        for i in range(best_fitting_order):
            param_dict[f'T{i+1}'] = best_overall_params[i]


    best_response, best_window_length_for_savgol = step_response(
        model_type=best_fitting_model_type,
        order=best_fitting_order,
        parameters=param_dict,
        t=time_values
    )


    smoothed_values_savgol = savgol_filter(response_values, window_length=best_window_length_for_savgol, polyorder=3)

    fig, axes = plt.subplots(1, 2)

    axes[0].plot(time_values, response_values, label='Real Step Response', color='red')
    axes[0].plot(time_values, smoothed_values_savgol, label='Smoothed Step Response', color='green', linestyle='--')
    axes[0].set_xlabel('Time [s]')
    axes[0].set_ylabel('Step Response x(t)')
    axes[0].set_title('Comparison between Real and Smoothed Step Response')
    axes[0].legend()

    axes[1].plot(time_values, smoothed_values_savgol, label='Smoothed Step Response', color='green', linestyle='--')
    axes[1].plot(time_values, best_response, label=f'Best Fit ({best_fitting_model_type}{best_fitting_order})', color='blue')
    axes[1].set_xlabel('Time [s]')
    axes[1].set_ylabel('Step Response x(t)')
    axes[1].set_title('Comparison between Smoothed Step Response and Best Fit of System Models')
    axes[1].legend()

    plt.tight_layout()
    plt.show()


    char_values = calculate_characteristic_value_for_every_method(best_fitting_model_type, best_fitting_order, best_overall_params, best_response, time_values, step_values)
    

    return best_fitting_model_type, best_fitting_order, char_values
