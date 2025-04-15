from math import pow
from numpy import pi

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



def chien_hrones_reswick_20_percent_pid(k_s, t_u, t_g):

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



def samal_pid(k_s, t_u, t_g):

    # p-controller
    sam_p_k_r = pi/4 * t_g / (k_s + t_u)

    # pi-controller
    sam_pi_k_r = sam_p_k_r
    sam_pi_t_n = 3.33 * t_u

    # pid-controller
    sam_pid_k_r = sam_p_k_r
    sam_pid_t_n = 2 * t_u
    sam_pid_t_v = 0.5 * t_u


    return sam_p_k_r, sam_pi_k_r, sam_pi_t_n, sam_pid_k_r, sam_pid_t_n, sam_pid_t_v



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
