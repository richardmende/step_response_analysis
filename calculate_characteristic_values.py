import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_characteristic_value_for_every_method(best_fitting_params, best_fitting_time_response, time_values_response):

    K_infinity = best_fitting_params[0]
    
    # Skalierung auf Einheitssprung beachten !!!
    # K_S = K_infinity / step_hight !!!

    # hier zur VEREINFACHUNG und NACHVOLLZIEHBARKEIT!!!
    K_S = K_infinity


    # t_sum
    t_sum = sum(best_fitting_params[1:])


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
    turning_point_tangent = slope * time_values_response + y_axis_intercept

    t_u = - y_axis_intercept / slope
    t_g = (K_S - y_axis_intercept) / slope


    # time percent
    percentages = [10, 20, 50, 80, 90]
    percentage_values = [K_S * (p / 100.0) for p in percentages]

    time_percent_values = []

    for target in percentage_values:
        number = np.argmax(np.array(best_fitting_time_response) >= target)
        time_percent_values.append(time_values_response[number])

    plt.figure(figsize=(10, 6))

    # Plot der Sprungantwort
    plt.plot(time_values_response, best_fitting_time_response, label="time response", color="blue")

    # Markiere den Endwert K_S
    plt.axhline(K_S, color='red', linestyle='--', label=f'K_S = {K_S:.2f}')

    # Markiere die Zeitpunkte t_10, t_20, t_50, t_80, t_90
    for i, percent in enumerate(percentages):
        plt.scatter(time_percent_values[i], percentage_values[i], label=f't_{percent} = {time_percent_values[i]:.2f}s', zorder=5)


    # turning point tangent
    plt.plot(time_values_response[(time_values_response >= t_u) & (time_values_response <= t_g)], turning_point_tangent[(time_values_response >= t_u) & (time_values_response <= t_g)], label='turning point tangent', linestyle='--', color='cyan')
    # turning point
    plt.scatter(turning_point_time, turning_point_value, color='cyan', zorder=5, label='turning point')


    # Markiere Verzugszeit t_u und Ausgleichszeit t_g
    plt.axvline(t_u, color='green', linestyle='--', label=f't_u = {t_u:.2f}s')
    plt.axvline(t_g, color='orange', linestyle='--', label=f't_g = {t_g:.2f}s')

    # Markiere Gesamtzeit t_sum
    plt.axvline(t_sum, color='purple', linestyle='--', label=f't_sum = {t_sum:.2f}s')

    # Labels und Titel
    plt.title("Sprungantwort und wichtige Zeitpunkte")
    plt.xlabel("time [s]")
    plt.ylabel("step response response")
    plt.legend(loc="best")
    plt.grid(True)

    # Anzeigen des Plots
    plt.tight_layout()
    plt.show()


    characteristic_values = K_S, t_sum, t_u, t_g, time_percent_values

    return characteristic_values
