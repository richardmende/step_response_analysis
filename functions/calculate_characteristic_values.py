import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import trapezoid
from scipy.optimize import minimize_scalar
from scipy.interpolate import interp1d



def calculate_characteristic_value_for_every_method(best_system_description, best_order, best_fitting_params, best_fitting_step_response, time_values_response, step):

    if best_system_description == 'PT':

        K_infinity = best_fitting_params[0]
        K_S = K_infinity / (step[-1] - step[0])


        # t_sum method 1                                    # for pt1 also possible: t_sum = sum(best_fitting_params[1:])
        def objective(t_split, t, x, k_inf):

            idx = np.searchsorted(t, t_split)

            # A1: Fläche unterhalb der Sprungantwort bis t_i
            A1 = trapezoid(x[:idx] - step[0], t[:idx])

            # A2: Fläche zwischen Sprungantwort und k_inf ab t_i bis zum Ende
            A2 = trapezoid(k_inf - x[idx:], t[idx:])

            diff = abs(A1 - A2)

            return diff, A1, A2

        def minimize_and_get_A1_A2(t, x, k_inf, time_values_response):
            # Wrapper für die Objective-Funktion
            def wrapper(t_split):
                diff, A1, A2 = objective(t_split, t, x, k_inf)
                wrapper.A1 = A1  # Speichern von A1
                wrapper.A2 = A2  # Speichern von A2
                return diff

            result = minimize_scalar(wrapper, bounds=(time_values_response[1], time_values_response[-1]), method='bounded')
    
            # A1 und A2 nach der Minimierung abrufen
            return result, wrapper.A1, wrapper.A2
    
        result, A_1, A_2 = minimize_and_get_A1_A2(time_values_response, best_fitting_step_response, K_infinity, time_values_response)

        t_sum1 = result.x
        idx = np.searchsorted(time_values_response, t_sum1)


        # t_sum method 2

        A_sum = trapezoid(K_infinity - best_fitting_step_response, time_values_response)
        t_sum2 = A_sum / K_S

        # time percent
        percentages = [10, 20, 50, 80, 90]
        percentage_values = [(step[-1] - step[0]) * (p / 100.0) for p in percentages]

        time_percent_values = []

        for target in percentage_values:
            number = np.argmax(np.array(best_fitting_step_response) >= target)
            time_percent_values.append(time_values_response[number])


        # tangent
        if best_order == 1:         
            
            # ONLY POSSIBLE, IF THE SYSTEM HAS A DEAD TIME !!! HERE APPROXIMATED AS ONE TO BE ABLE TO CONTINUE!
            t_u = 1

            # calculating tangent

            tangent = time_values_response * best_fitting_params[0] / best_fitting_params[1]
            t_g = K_infinity * best_fitting_params[1] / best_fitting_params[0]                  # should be T1 !

        elif best_order >= 2:

            # calculating turning point
            first_derivative = np.gradient(best_fitting_step_response, time_values_response)
            second_derivative = np.gradient(first_derivative, time_values_response)

            zero_crossing = np.where(np.diff(np.sign(second_derivative)))[0]
            
            idx = zero_crossing[0]
            turning_point_time = time_values_response[idx]
            turning_point_value = best_fitting_step_response[idx]

            # turning point tangent
            slope = first_derivative[idx]
            y_axis_intercept = turning_point_value - slope * turning_point_time
            tangent = slope * time_values_response + y_axis_intercept               # turning_point_tangent

            t_u = - y_axis_intercept / slope                # MAYBE ADDITIONAL DEAD TIME; THIS HAS TO BE CONSIDERED
            t_g = (K_infinity - y_axis_intercept) / slope

        
        fig, axes = plt.subplots(2,2)

        # t_sum (method 1)
        # useful for marking the correct areas
        interp_func = interp1d(time_values_response, best_fitting_step_response)
        x_tsum1 = interp_func(t_sum1)
        t_before = np.append(time_values_response[time_values_response < t_sum1], t_sum1)
        x_before = np.append(best_fitting_step_response[time_values_response < t_sum1], x_tsum1)
        t_after = np.insert(time_values_response[time_values_response >= t_sum1], 0, t_sum1)
        x_after = np.insert(best_fitting_step_response[time_values_response >= t_sum1], 0, x_tsum1)


        axes[0,0].plot(time_values_response, best_fitting_step_response, label='step response')
        axes[0,0].fill_between(t_before, 0, x_before, alpha=0.4, label=f'$A_1$ = {A_1:.4f}', color='green')
        axes[0,0].fill_between(t_after, x_after, K_infinity, alpha=0.2, label=f'$A_2$ = {A_2:.4f}', color='limegreen')
        axes[0,0].plot([t_sum1, t_sum1], [step[0], K_infinity], color='orange', linestyle=':', label=f'$T_\\Sigma$ = {t_sum1:.4f}')
        axes[0,0].axhline(K_infinity, color='gray', linestyle=':', label=f'$K_\\infty$ = {K_infinity:.4f}')
        axes[0,0].set_xlabel('time $t$ [s]')
        axes[0,0].set_ylabel('step response $x(t)$')
        axes[0,0].set_title('T-sum (method 1)')
        axes[0,0].legend()
        axes[0,0].grid(True)

        # t_sum (method 2)
        axes[0,1].plot(time_values_response, best_fitting_step_response, label='step response')
        axes[0,1].fill_between(time_values_response, K_infinity, best_fitting_step_response, alpha=0.2, label=f'$A_\\Sigma$ = {A_sum:.4f}', color='limegreen')
        axes[0,1].plot([t_sum2, t_sum2], [step[0], K_infinity], color='orange', linestyle=':', label=f'$T_\\Sigma$ = {t_sum2:.4f}')
        axes[0,1].axhline(K_infinity, color='gray', linestyle=':', label=f'$K_\\infty$ = {K_infinity:.4f}')
        axes[0,1].set_xlabel('time $t$ [s]')
        axes[0,1].set_ylabel('step response $x(t)$')
        axes[0,1].set_title('T-sum (method 2)')
        axes[0,1].legend()
        axes[0,1].grid(True)

        # tangent
        axes[1,0].plot(time_values_response, best_fitting_step_response, label='step response')

        if best_order == 1:
            # tangent
            mask = time_values_response <= t_g
            tangent_times = time_values_response[mask]
            tangent_values = tangent[mask]
            tangent_tg_value = K_infinity            
            tangent_times = np.append(tangent_times, t_g)
            tangent_values = np.append(tangent_values, tangent_tg_value)

            axes[1,0].plot(tangent_times, tangent_values, label='tangent', linestyle=':', color='cyan')

        elif best_order >= 2:
            # turning point
            axes[1,0].scatter(turning_point_time, turning_point_value, color='cyan', zorder=5, label='turning point')

            # turning point tangent
            mask = (time_values_response >= t_u) & (time_values_response <= t_g)
            axes[1,0].plot(time_values_response[mask], tangent[mask], label='turning point tangent', linestyle='--', color='cyan')

            axes[1,0].plot([t_u, t_u], [step[0], K_infinity], color='green', linestyle=':', label=f'$T_u$ = {t_u:.2f} s')

        axes[1,0].plot([t_g, t_g], [step[0], K_infinity], color='limegreen', linestyle=':', label=f'$T_g$ = {t_g:.2f} s')
        axes[1,0].axhline(K_infinity, color='gray', linestyle=':', label=f'$K_\\infty$ = {K_infinity:.4f}')
        axes[1,0].set_xlabel('time $t$ [s]')
        axes[1,0].set_ylabel('step response $x(t)$')
        axes[1,0].set_title('tangent')
        axes[1,0].legend()
        axes[1,0].grid(True)

        # time percent
        axes[1,1].plot(time_values_response, best_fitting_step_response, label='step response')

        for i, percent in enumerate(percentages):
            colors = ['orange', 'limegreen', 'cyan', 'green', 'maroon']
            single_color = colors[i % len(colors)]
            axes[1,1].scatter(time_percent_values[i], percentage_values[i], label=f'$t_{{{percent}}}$ = {time_percent_values[i]:.2f} s', color=single_color, zorder=5)
            axes[1,1].plot([time_percent_values[i], time_percent_values[i]], [step[0], percentage_values[i]], color=single_color, linestyle='--', linewidth=1)
            axes[1,1].plot([step[0], time_percent_values[i]], [percentage_values[i], percentage_values[i]], color=single_color, linestyle='--', linewidth=1)
        
        axes[1,1].axhline(K_infinity, color='gray', linestyle=':', label=f'$K_\\infty$ = {K_infinity:.4f}')
        axes[1,1].set_xlabel('time $t$ [s]')
        axes[1,1].set_ylabel('step response $x(t)$')
        axes[1,1].set_title('time percent')
        axes[1,1].legend()
        axes[1,1].grid(True)

        fig.tight_layout()
        plt.show()
        
        characteristic_values = [K_S, t_sum1, t_sum2, t_u, t_g, time_percent_values]
    

    
    elif best_system_description == 'IT':

        if best_order == 1:

            first_derivative = np.gradient(best_fitting_step_response, time_values_response)

            slope = first_derivative[-1]

            endpoint_time = time_values_response[-1]
            endpoint_value = best_fitting_step_response[-1]

            y_axis_intercept = endpoint_value - slope * endpoint_time

            tangent = slope * time_values_response + y_axis_intercept


        elif best_order >= 2:

            # calculating turning point
            first_derivative = np.gradient(best_fitting_step_response, time_values_response)
            second_derivative = np.gradient(first_derivative, time_values_response)

            zero_crossing = np.where(np.diff(np.sign(second_derivative)))[0]
            
            idx = zero_crossing[0]
            turning_point_time = time_values_response[idx]
            turning_point_value = best_fitting_step_response[idx]

            # turning point tangent
            slope = first_derivative[idx]
            y_axis_intercept = turning_point_value - slope * turning_point_time
            tangent = slope * time_values_response + y_axis_intercept     # turning_point_tangent

        K_S = np.copy(slope)
        t_u = - y_axis_intercept / slope     # MAYBE ADDITIONAL DEAD TIME; THIS HAS TO BE CONSIDERED !!!
        t_g = 1

        plt.plot(time_values_response, best_fitting_step_response, label="time response", color="blue")

        if best_order == 1:
            # tangent
            plt.plot(time_values_response[(time_values_response >= t_u)], tangent[(time_values_response >= t_u)], label='tangent', linestyle='--', color='cyan')
            
        elif best_order >= 2:
            mask = (time_values_response >= t_u) & (time_values_response <= turning_point_time)
            # turning point tangent
            plt.plot(time_values_response[mask], tangent[mask], label='turning point tangent', linestyle='--', color='cyan')
            # turning point
            plt.scatter(turning_point_time, turning_point_value, color='cyan', zorder=5, label='turning point')


        # mark t_u
        plt.axvline(t_u, color='green', linestyle=':', label=f'$t_u$ = {t_u:.2f}s')

        plt.title("tangent")
        plt.xlabel("time $t$ [s]")
        plt.ylabel("step response $x(t)$")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
        characteristic_values = [K_S, t_u, t_g]


    return characteristic_values
