from scipy.optimize import minimize
from numpy import inf

from quality_score import compute_quality_score
from general_systems_description import SystemModel


def optimize_model(model_type, order, time_values, smoothed_values):
    def objective(params):
        # Mapping der Parameter in dict
        param_dict = {'K': params[0]}
        for i in range(1, order + 1):
            param_dict[f'T{i}'] = params[i]

        # Modell erzeugen
        model = SystemModel(model_type=model_type, order=order, parameters=param_dict)
        try:
            response = model.step_response(time_values)
        except:
            return inf  # Fehlerhafte Systeme direkt bestrafen

        # Score berechnen
        score = compute_quality_score(smoothed_values, response)
        return score

    # Startwerte (z. B. K=1.0, T_i = 1.0)
    x0 = [1.0] * (order + 1)
    
    # Parametergrenzen: K > 0, T_i > 0
    bounds = [(0.01, 10)] * (order + 1)

    result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

    best_params = result.x
    best_score = result.fun

    return best_score, best_params
