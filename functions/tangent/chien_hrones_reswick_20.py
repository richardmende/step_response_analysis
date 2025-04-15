def chien_hrones_reswick_20_pid(k_s, t_u, t_g):

    # constant factor for k_r of different controller types
    factor = t_g / (k_s * t_u)

    # p-controller
    chr_20_p_k_r = 0.7 * factor

    # pi-controller
    chr_20_pi_k_r = 0.6 * factor
    chr_20_pi_t_n = 1 * t_u

    # pid-controller
    chr_20_pid_k_r = 0.95 * factor
    chr_20_pid_t_n = 1.35 * t_u
    chr_20_pid_t_v = 0.47 * t_u


    return chr_20_p_k_r, chr_20_pi_k_r, chr_20_pi_t_n, chr_20_pid_k_r, chr_20_pid_t_n, chr_20_pid_t_v
