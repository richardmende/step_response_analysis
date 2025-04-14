import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy.integrate import trapezoid
from scipy.optimize import minimize_scalar



def calculate_characteristic_value_for_every_method(best_system_description, best_order, best_fitting_params, best_fitting_time_response, time_values_response):

    if best_system_description == 'PT':

        K_infinity = best_fitting_params[0]
        
        # Skalierung auf Einheitssprung beachten !!!
        # K_S = K_infinity / step_hight !!!

        # hier zur VEREINFACHUNG und NACHVOLLZIEHBARKEIT!!!
        K_S = K_infinity


        def objective(t_split, t, x, k_inf):

            # t_sum
            idx = np.searchsorted(t, t_split)

            # A1: Fläche unterhalb der Sprungantwort bis t_i
            A1 = trapezoid(x[:idx], t[:idx])                    # include starting value of input jump, here it is considered as 0 !!!

            # A2: Fläche zwischen Sprungantwort und k_inf ab t_i bis zum Ende
            A2 = trapezoid(k_inf - x[idx:], t[idx:])

            diff = abs(A1 - A2)

            return diff

        result = minimize_scalar(objective, args=(time_values_response, best_fitting_time_response, K_infinity), bounds = (time_values_response[1], time_values_response[-1]), method='bounded')

        t_sum = result.x
        idx = np.searchsorted(time_values_response, t_sum)

        plt.plot(time_values_response, best_fitting_time_response, label='Sprungantwort $x(t)$')
        plt.fill_between(time_values_response[:idx], 0, best_fitting_time_response[:idx], alpha=0.3, label='A1', color='green')
        plt.fill_between(time_values_response[idx:], best_fitting_time_response[idx:], K_infinity, alpha=0.3, label='A2', color='limegreen')
        plt.axvline(t_sum, color='red', linestyle='--', label=f'$T_\\Sigma$ = {t_sum:.4f}')
        plt.axhline(K_infinity, color='gray', linestyle=':', label='$K_\\infty$')
        plt.xlabel('Zeit $t$')
        plt.ylabel('Sprungantwort $x(t)$')
        plt.title('T-Summenverfahren (Direkte Variante)')
        plt.legend()
        plt.grid(True)
        plt.show()

        # before: t_sum = sum(best_fitting_params[1:])


        # time percent
        percentages = [10, 20, 50, 80, 90]
        percentage_values = [K_S * (p / 100.0) for p in percentages]

        time_percent_values = []

        for target in percentage_values:
            number = np.argmax(np.array(best_fitting_time_response) >= target)
            time_percent_values.append(time_values_response[number])


        # tangent
        if best_order == 1:         
            
            # ONLY POSSIBLE, IF THE SYSTEM HAS A DEAD TIME !!! HERE APPROXIMATED AS ONE TO BE ABLE TO CONTINUE!
            t_u = 1

            # calculating tangent

            tangent = time_values_response * best_fitting_params[0] / best_fitting_params[1]
            t_g = K_infinity * best_fitting_params[1] / best_fitting_params[0]                  # should be T1 !

        else:

            # calculating turning point
            first_derivative = np.gradient(best_fitting_time_response, time_values_response)
            second_derivative = np.gradient(first_derivative, time_values_response)

            zero_crossing = np.where(np.diff(np.sign(second_derivative)))[0]
            
            idx = zero_crossing[0]
            turning_point_time = time_values_response[idx]
            turning_point_value = best_fitting_time_response[idx]

            # turning point tangent
            slope = first_derivative[idx]
            y_axis_intercept = turning_point_value - slope * turning_point_time
            tangent = slope * time_values_response + y_axis_intercept     # turning_point_tangent

            t_u = - y_axis_intercept / slope                # MAYBE ADDITIONAL DEAD TIME; THIS HAS TO BE CONSIDERED
            t_g = (K_infinity - y_axis_intercept) / slope
        
        characteristic_values = K_S, t_sum, t_u, t_g, time_percent_values
    

    
    elif best_system_description == 'IT':

        if best_order == 1:

            first_derivative = np.gradient(best_fitting_time_response, time_values_response)

            slope = first_derivative[-1]

            endpoint_time = time_values_response[-1]
            endpoint_value = best_fitting_time_response[-1]

            y_axis_intercept = endpoint_value - slope * endpoint_time

            tangent = slope * time_values_response + y_axis_intercept


        elif best_order >= 2:

            # calculating turning point
            first_derivative = np.gradient(best_fitting_time_response, time_values_response)
            second_derivative = np.gradient(first_derivative, time_values_response)

            zero_crossing = np.where(np.diff(np.sign(second_derivative)))[0]
            
            idx = zero_crossing[0]
            turning_point_time = time_values_response[idx]
            turning_point_value = best_fitting_time_response[idx]

            # turning point tangent
            slope = first_derivative[idx]
            y_axis_intercept = turning_point_value - slope * turning_point_time
            tangent = slope * time_values_response + y_axis_intercept     # turning_point_tangent
           
        K_S = np.copy(slope)
        t_u = - y_axis_intercept / slope     # MAYBE ADDITIONAL DEAD TIME; THIS HAS TO BE CONSIDERED
        t_g = 1

        characteristic_values = K_S, t_u, t_g


    plt.figure(figsize=(10, 6))

    # Plot der Sprungantwort
    plt.plot(time_values_response, best_fitting_time_response, label="time response", color="blue")

    if best_system_description == 'PT':

        # Markiere den Endwert K_S
        plt.axhline(K_S, color='red', linestyle='--', label=f'K_S = {K_S:.2f}')

        # Markiere die Zeitpunkte t_10, t_20, t_50, t_80, t_90
        for i, percent in enumerate(percentages):
            plt.scatter(time_percent_values[i], percentage_values[i], label=f't_{percent} = {time_percent_values[i]:.2f}s', zorder=5)

        if best_order == 1:
            # tangent
            plt.plot(time_values_response[time_values_response <= t_g], tangent[time_values_response <= t_g], label='tangent', linestyle='--', color='cyan')

        if best_order >= 2:
            # turning point tangent
            plt.plot(time_values_response[(time_values_response >= t_u) & (time_values_response <= t_g)], tangent[(time_values_response >= t_u) & (time_values_response <= t_g)], label='turning point tangent', linestyle='--', color='cyan')
            # turning point
            plt.scatter(turning_point_time, turning_point_value, color='cyan', zorder=5, label='turning point')
    
    if best_system_description == 'IT':

        if best_order == 1:
            # tangent
            plt.plot(time_values_response[(time_values_response >= t_u)], tangent[(time_values_response >= t_u)], label='tangent', linestyle='--', color='cyan')
        
        if best_order >= 2:
            # turning point tangent
            plt.plot(time_values_response[(time_values_response >= t_u)], tangent[(time_values_response >= t_u)], label='turning point tangent', linestyle='--', color='cyan')
            # turning point
            plt.scatter(turning_point_time, turning_point_value, color='cyan', zorder=5, label='turning point')


    # mark t_u
    plt.axvline(t_u, color='green', linestyle='--', label=f't_u = {t_u:.2f}s')
    
    if best_system_description == 'PT':
        # mark t_g
        plt.axvline(t_g, color='orange', linestyle='--', label=f't_g = {t_g:.2f}s')

        # mark t_sum
        plt.axvline(t_sum, color='purple', linestyle='--', label=f't_sum = {t_sum:.2f}s')


    plt.title("Sprungantwort und wichtige Zeitpunkte")
    plt.xlabel("time [s]")
    plt.ylabel("step response response")
    plt.legend(loc="best")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


    return characteristic_values
