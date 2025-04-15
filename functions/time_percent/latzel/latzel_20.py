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
