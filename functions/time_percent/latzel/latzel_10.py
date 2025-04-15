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
