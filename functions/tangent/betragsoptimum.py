from math import pow

def betragsoptimum_pid(k_s, t_u, t_g):

    # constant factor for k_r of different controller types
    factor = 1 / k_s

    # p-controller
    bet_p_k_r = factor * pow((t_g / t_u),2) / (1 + 2 * t_g / t_u)

    # pi-controller
    bet_pi_k_r = factor * (0.5 * t_g / t_u + 0.5 * t_u / t_g)
    bet_pi_t_n = t_g + pow(t_u,2) / (6 * t_g)

    # pid-controller
    bet_pid_k_r = factor * (0.25 + 0.75 * t_g / t_u + t_u / (80 * t_g))
    bet_pid_t_n = t_g + t_u / 3
    bet_pid_t_v = 0.25 * t_g + pow(t_u,2) / (80 * t_g)


    return bet_p_k_r, bet_pi_k_r, bet_pi_t_n, bet_pid_k_r, bet_pid_t_n, bet_pid_t_v
