def strejc_10_90(t_10, t_90):
    
    str_10_90_t_u = 1.048 * t_10 - 0.048 * t_90
    str_10_90_t_g = 0.455 * (t_90  - t_10)

    return str_10_90_t_u, str_10_90_t_g
