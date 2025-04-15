def ziegler_nichols_pid(k_s, t_u, t_g):

    # constant factor for k_r of different controller types
    factor = t_g / (k_s * t_u)

    # p-controller
    zn_p_k_r = factor

    # pi-controller
    zn_pi_k_r = 0.9 * factor
    zn_pi_t_n = 3.33 * t_u

    # pid-controller
    zn_pid_k_r = 1.2 * factor
    zn_pid_t_n = 2 * t_u
    zn_pid_t_v = 0.5 * t_u


    return zn_p_k_r, zn_pi_k_r, zn_pi_t_n, zn_pid_k_r, zn_pid_t_n, zn_pid_t_v
