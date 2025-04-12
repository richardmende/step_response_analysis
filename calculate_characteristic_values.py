import numpy as np

def calculate_characteristic_value_for_every_method(best_fitting_params, best_fitting_time_response, time_values_response):

    K_S = best_fitting_params[0]

    T_sum = sum(best_fitting_params[1:])


    # calculating turning point
    first_derivative = np.gradient(best_fitting_time_response, time_values_response)
    second_derivative = np.gradient(first_derivative, time_values_response)

    zero_crossing = np.where(np.diff(np.sign(second_derivative)))[0]

    if len(zero_crossing) == 0:
        print("no turning point available")
        return None, None
    
    idx = zero_crossing[0]
    turning_point_time = time_values_response[idx]
    turning_point_value = best_fitting_time_response[idx]

    # turning point tangent
    slope = first_derivative[idx]
    y_axis_intercept = turning_point_value - slope * turning_point_time
    turning_point_tangent = slope * time_values_response - y_axis_intercept





    characteristic_values = K_S, T_sum#, T_u, T_g, t_10, t_20, t_50, t_80, t_90

    return characteristic_values