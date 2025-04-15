def strejc_20_80(t_20, t_80):
    
    str_20_80_t_u = 1.161 * t_20 - 0.161 * t_80
    str_20_80_t_g = 0.721 * (t_80  - t_20)

    return str_20_80_t_u, str_20_80_t_g
