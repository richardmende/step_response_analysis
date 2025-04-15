def latzel_pid(k_s, t_u, t_g):

    # there's no p-controller !!!
    lat_p_k_r = None

    # pi-controller
    lat_pi_k_r = 0.28 * t_g / (k_s * (t_u + 0.1 * t_g))
    lat_pi_t_n = 0.53 * t_g

    # pid-controller
    lat_pid_k_r = 0.39 * t_g / (k_s * (t_u - 0.08 * t_g))   # warning if its <= 6.5 !!!
    lat_pid_t_n = 0.74 * t_g
    lat_pid_t_v = 0.14 * t_u


    return lat_p_k_r, lat_pi_k_r, lat_pi_t_n, lat_pid_k_r, lat_pid_t_n, lat_pid_t_v
