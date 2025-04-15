from numpy import pi

def samal_pid(k_s, t_u, t_g):

    # p-controller
    sam_p_k_r = pi / 4 * t_g / (k_s * t_u)

    # pi-controller
    sam_pi_k_r = sam_p_k_r
    sam_pi_t_n = 3.33 * t_u

    # pid-controller
    sam_pid_k_r = sam_p_k_r
    sam_pid_t_n = 2 * t_u
    sam_pid_t_v = 0.5 * t_u


    return sam_p_k_r, sam_pi_k_r, sam_pi_t_n, sam_pid_k_r, sam_pid_t_n, sam_pid_t_v
