def oppelt_pid(k_s, t_u, t_g):

    # constant factor for k_r of different controller types
    factor = t_g / (k_s * t_u)

    # p-controller
    opp_p_k_r = factor

    # pi-controller
    opp_pi_k_r = 0.8 * factor
    opp_pi_t_n = 3 * t_u

    # pid-controller
    opp_pid_k_r = 1.2 * factor
    opp_pid_t_n = 2 * t_u
    opp_pid_t_v = 0.42 * t_u


    return opp_p_k_r, opp_pi_k_r, opp_pi_t_n, opp_pid_k_r, opp_pid_t_n, opp_pid_t_v
