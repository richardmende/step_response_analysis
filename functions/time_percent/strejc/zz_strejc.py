def strejc_10_90(t_10, t_90):
    
    str_10_90_t_u = 1.048 * t_10 - 0.048 * t_90
    str_10_90_t_g = 0.455 * (t_90  - t_10)

    return str_10_90_t_u, str_10_90_t_g



def strejc_20_80(t_20, t_80):
    
    str_20_80_t_u = 1.161 * t_20 - 0.161 * t_80
    str_20_80_t_g = 0.721 * (t_80  - t_20)

    return str_20_80_t_u, str_20_80_t_g
