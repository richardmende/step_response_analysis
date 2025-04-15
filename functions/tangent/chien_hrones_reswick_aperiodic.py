def chien_hrones_reswick_aperiodic_pid(k_s, t_u, t_g):

    # constant factor for k_r of different controller types
    factor = t_g / (k_s * t_u)

    # p-controller
    chr_ap_p_k_r = 0.3 * factor

    # pi-controller
    chr_ap_pi_k_r = 0.35 * factor
    chr_ap_pi_t_n = 1.2 * t_u

    # pid-controller
    chr_ap_pid_k_r = 0.6 * factor
    chr_ap_pid_t_n = 1 * t_u
    chr_ap_pid_t_v = 0.5 * t_u


    return chr_ap_p_k_r, chr_ap_pi_k_r, chr_ap_pi_t_n, chr_ap_pid_k_r, chr_ap_pid_t_n, chr_ap_pid_t_v
