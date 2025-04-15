def latzel_calculation(t_10, t_50, t_90):

    mu = t_10 / t_90

    mu_values = [0.137, 0.174, 0.207, 0.261, 0.304, 0.340, 0.370, 0.396, 0.418, 0.438]
    n_alpha_table = {
        0.137: (2, 1.880, 0.596, 0.257),
        0.174: (2.5, 1.245, 0.460, 0.216),
        0.207: (3, 0.907, 0.374, 0.188),
        0.261: (4, 0.573, 0.272, 0.150),
        0.304: (5, 0.411, 0.214, 0.125),
        0.340: (6, 0.317, 0.176, 0.108),
        0.370: (7, 0.257, 0.150, 0.095),
        0.396: (8, 0.215, 0.130, 0.085),
        0.418: (9, 0.184, 0.115, 0.077),
        0.438: (10, 0.161, 0.103, 0.070)
        }


    closest_mu = min(mu_values, key=lambda x: abs(x - mu))

    n, alpha_10, alpha_50, alpha_90 = n_alpha_table[closest_mu]

    t_m = 1/3 * (alpha_10 * t_10 + alpha_50 * t_50 + alpha_90 * t_90)


    return t_m, n



def latzel_10_pid(k_s, t_m, n):

    # the numbers depend on parameter n
    controller_param_n_table = {
        2:      {'PI': (1.650, 1.55),   'PID': None},
        2.5:    {'PI': (1.202, 1.77),   'PID': None},
        3:      {'PI': (0.884, 1.96),   'PID': (2.543, 2.47, 0.66)},
        4:      {'PI': (0.656, 2.30),   'PID': (1.461, 2.92, 0.84)},
        5:      {'PI': (0.540, 2.59),   'PID': (1.109, 3.31, 0.99)},
        6:      {'PI': (0.468, 2.86),   'PID': (0.914, 3.66, 1.13)},
        7:      {'PI': (0.417, 3.10),   'PID': (0.782, 3.97, 1.25)},
        8:      {'PI': (0.379, 3.32),   'PID': (0.689, 4.27, 1.36)},
        9:      {'PI': (0.349, 3.53),   'PID': (0.617, 4.54, 1.47)},
        10:     {'PI': (0.325, 3.73),   'PID': (0.559, 4.80, 1.57)},
    }

    # select the right line for n
    params = controller_param_n_table[n]

    # extract values for pi- and pid-controller
    pi_params = params['PI']
    pid_params = params['PID']

    # there's no p-controller !!!
    lat_10_p_k_r = None

    # pi-controller
    lat_10_pi_k_r = pi_params[0] / k_s
    lat_10_pi_t_n = pi_params[1] * t_m

    # pid-controller
    if n < 3:
        lat_10_pid_k_r = None
        lat_10_pid_t_n = None
        lat_10_pid_t_v = None
    else:
        lat_10_pid_k_r = pid_params[0] / k_s
        lat_10_pid_t_n = pid_params[1] * t_m
        lat_10_pid_t_v = pid_params[2] * t_m


    return lat_10_p_k_r, lat_10_pi_k_r, lat_10_pi_t_n, lat_10_pid_k_r, lat_10_pid_t_n, lat_10_pid_t_v



def latzel_20_pid(k_s, t_m, n):

    # the numbers depend on parameter n
    controller_param_n_table = {
        2:      {'PI': (2.603, 1.55),   'PID': None},
        2.5:    {'PI': (1.683, 1.77),   'PID': None},
        3:      {'PI': (1.153, 1.96),   'PID': (3.510, 2.47, 0.66)},
        4:      {'PI': (0.802, 2.30),   'PID': (1.830, 2.92, 0.84)},
        5:      {'PI': (0.654, 2.59),   'PID': (1.337, 3.31, 0.99)},
        6:      {'PI': (0.561, 2.86),   'PID': (1.082, 3.66, 1.13)},
        7:      {'PI': (0.497, 3.10),   'PID': (0.922, 3.97, 1.25)},
        8:      {'PI': (0.451, 3.32),   'PID': (0.812, 4.27, 1.36)},
        9:      {'PI': (0.413, 3.53),   'PID': (0.727, 4.54, 1.47)},
        10:     {'PI': (0.384, 3.73),   'PID': (0.660, 4.80, 1.57)},
    }

    # select the right line for n
    params = controller_param_n_table[n]

    # extract values for pi- and pid-controller
    pi_params = params['PI']
    pid_params = params['PID']

    # there's no p-controller !!!
    lat_20_p_k_r = None

    # pi-controller
    lat_20_pi_k_r = pi_params[0] / k_s
    lat_20_pi_t_n = pi_params[1] * t_m

    # pid-controller
    if n < 3:
        lat_20_pid_k_r = None
        lat_20_pid_t_n = None
        lat_20_pid_t_v = None
    else:
        lat_20_pid_k_r = pid_params[0] / k_s
        lat_20_pid_t_n = pid_params[1] * t_m
        lat_20_pid_t_v = pid_params[2] * t_m


    return lat_20_p_k_r, lat_20_pi_k_r, lat_20_pi_t_n, lat_20_pid_k_r, lat_20_pid_t_n, lat_20_pid_t_v
