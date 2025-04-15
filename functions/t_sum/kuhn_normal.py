def kuhn_normal_pid(k_s, t_sum):

    # there's no p-controller !!!
    kuhn_norm_p_k_r = None

    # pi-controller
    kuhn_norm_pi_k_r = 0.5 / k_s
    kuhn_norm_pi_t_n = 0.5 * t_sum

    # pid-controller
    kuhn_norm_pid_k_r = 1 / k_s
    kuhn_norm_pid_t_n = 0.667 * t_sum
    kuhn_norm_pid_t_v = 0.167 * t_sum

    return kuhn_norm_p_k_r, kuhn_norm_pi_k_r, kuhn_norm_pi_t_n, kuhn_norm_pid_k_r, kuhn_norm_pid_t_n, kuhn_norm_pid_t_v
