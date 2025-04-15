from .t_sum.zz_t_sum import kuhn_fast_pid, kuhn_normal_pid
from .tangent.zz_tangent_pid import betragsoptimum_pid, chien_hrones_reswick_20_percent_pid, chien_hrones_reswick_aperiodic_pid, latzel_pid, oppelt_pid, samal_pid, ziegler_nichols_pid
from .time_percent.latzel.zz_latzel import latzel_calculation, latzel_10_pid, latzel_20_pid
from .time_percent.strejc.zz_strejc import strejc_10_90, strejc_20_80


from pandas import DataFrame
from pandasgui import show



# function for rounding on 2 decimal places
def two_decimal_places(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    else:
        return "—"


def print_possible_pid_table(model_type, model_order, characteristic_values):

    if model_type == 'PT':
        K_S = characteristic_values[0]
        T_sum1 = characteristic_values[1]
        T_sum2 = characteristic_values[2]
        T_u = characteristic_values[3]
        T_g = characteristic_values[4]
        t_10 = characteristic_values[5][0]
        t_20 = characteristic_values[5][1]
        t_50 = characteristic_values[5][2]
        t_80 = characteristic_values[5][3]
        t_90 = characteristic_values[5][4]

        # collecting values for t_sum
        kuhn_fast1 = kuhn_fast_pid(K_S, T_sum1)
        kuhn_normal1 = kuhn_normal_pid(K_S, T_sum1)

        kuhn_fast2 = kuhn_fast_pid(K_S, T_sum2)
        kuhn_normal2 = kuhn_normal_pid(K_S, T_sum2)

        # collecting values for time_percent: Latzel
        t_m, n = latzel_calculation(t_10, t_50, t_90)
        lat_10 = latzel_10_pid(K_S, t_m, n)
        lat_20 = latzel_20_pid(K_S, t_m, n)

        if model_order == 1:

            # preparing table for printing with 2 decimal places
            table1 = [
                ["type of controller", "parameter", "Kuhn1 (fast)", "Kuhn1 (normal)", "Kuhn2 (fast)", "Kuhn2 (normal)", "Latzel (10)", "Latzel (20)"],
                ["P",  "K_R",  two_decimal_places(kuhn_fast1[0]), two_decimal_places(kuhn_normal1[0]), two_decimal_places(kuhn_fast2[0]), two_decimal_places(kuhn_normal2[0]), two_decimal_places(lat_10[0]), two_decimal_places(lat_20[0])],
                ["PI", "K_R",  two_decimal_places(kuhn_fast1[1]), two_decimal_places(kuhn_normal1[1]), two_decimal_places(kuhn_fast2[1]), two_decimal_places(kuhn_normal2[1]), two_decimal_places(lat_10[1]), two_decimal_places(lat_20[1])],
                ["",   "T_N",  two_decimal_places(kuhn_fast1[2]), two_decimal_places(kuhn_normal1[2]), two_decimal_places(kuhn_fast2[2]), two_decimal_places(kuhn_normal2[2]), two_decimal_places(lat_10[2]), two_decimal_places(lat_20[2])],
                ["PID","K_R",  two_decimal_places(kuhn_fast1[3]), two_decimal_places(kuhn_normal1[3]), two_decimal_places(kuhn_fast2[3]), two_decimal_places(kuhn_normal2[3]), two_decimal_places(lat_10[3]), two_decimal_places(lat_20[3])],
                ["",   "T_N",  two_decimal_places(kuhn_fast1[4]), two_decimal_places(kuhn_normal1[4]), two_decimal_places(kuhn_fast2[4]), two_decimal_places(kuhn_normal2[4]), two_decimal_places(lat_10[4]), two_decimal_places(lat_20[4])],
                ["",   "T_NV", two_decimal_places(kuhn_fast1[5]), two_decimal_places(kuhn_normal1[5]), two_decimal_places(kuhn_fast2[5]), two_decimal_places(kuhn_normal2[5]), two_decimal_places(lat_10[5]), two_decimal_places(lat_20[5])]
            ]

        if model_order >= 2:
            # collecting values for tangent
            betrag = betragsoptimum_pid(K_S, T_u, T_g)
            chr_20 = chien_hrones_reswick_20_percent_pid(K_S, T_u, T_g)
            chr_ap = chien_hrones_reswick_aperiodic_pid(K_S, T_u, T_g)
            latzel = latzel_pid(K_S, T_u, T_g)
            oppelt = oppelt_pid(K_S, T_u, T_g)
            samal = samal_pid(K_S, T_u, T_g)
            zini = ziegler_nichols_pid(K_S, T_u, T_g)

            # preparing table for printing with 2 decimal places
            table1 = [
                ["type of controller", "parameter", "Kuhn1 (fast)", "Kuhn1 (normal)", "Kuhn2 (fast)", "Kuhn2 (normal)", "Betragsoptimum", "CHR (20)", "CHR (aperiodic)", "Latzel (tangent)", "Oppelt", "Samal", "Ziegler/Nichols", "Latzel (10)", "Latzel (20)"],
                ["P",  "K_R",  two_decimal_places(kuhn_fast1[0]), two_decimal_places(kuhn_normal1[0]), two_decimal_places(kuhn_fast2[0]), two_decimal_places(kuhn_normal2[0]), two_decimal_places(betrag[0]), two_decimal_places(chr_20[0]), two_decimal_places(chr_ap[0]), two_decimal_places(latzel[0]), two_decimal_places(oppelt[0]), two_decimal_places(samal[0]), two_decimal_places(zini[0]), two_decimal_places(lat_10[0]), two_decimal_places(lat_20[0])],
                ["PI", "K_R",  two_decimal_places(kuhn_fast1[1]), two_decimal_places(kuhn_normal1[1]), two_decimal_places(kuhn_fast2[1]), two_decimal_places(kuhn_normal2[1]), two_decimal_places(betrag[1]), two_decimal_places(chr_20[1]), two_decimal_places(chr_ap[1]), two_decimal_places(latzel[1]), two_decimal_places(oppelt[1]), two_decimal_places(samal[1]), two_decimal_places(zini[1]), two_decimal_places(lat_10[1]), two_decimal_places(lat_20[1])],
                ["",   "T_N",  two_decimal_places(kuhn_fast1[2]), two_decimal_places(kuhn_normal1[2]), two_decimal_places(kuhn_fast2[2]), two_decimal_places(kuhn_normal2[2]), two_decimal_places(betrag[2]), two_decimal_places(chr_20[2]), two_decimal_places(chr_ap[2]), two_decimal_places(latzel[2]), two_decimal_places(oppelt[2]), two_decimal_places(samal[2]), two_decimal_places(zini[2]), two_decimal_places(lat_10[2]), two_decimal_places(lat_20[2])],
                ["PID","K_R",  two_decimal_places(kuhn_fast1[3]), two_decimal_places(kuhn_normal1[3]), two_decimal_places(kuhn_fast2[3]), two_decimal_places(kuhn_normal2[3]), two_decimal_places(betrag[3]), two_decimal_places(chr_20[3]), two_decimal_places(chr_ap[3]), two_decimal_places(latzel[3]), two_decimal_places(oppelt[3]), two_decimal_places(samal[3]), two_decimal_places(zini[3]), two_decimal_places(lat_10[3]), two_decimal_places(lat_20[3])],
                ["",   "T_N",  two_decimal_places(kuhn_fast1[4]), two_decimal_places(kuhn_normal1[4]), two_decimal_places(kuhn_fast2[4]), two_decimal_places(kuhn_normal2[4]), two_decimal_places(betrag[4]), two_decimal_places(chr_20[4]), two_decimal_places(chr_ap[4]), two_decimal_places(latzel[4]), two_decimal_places(oppelt[4]), two_decimal_places(samal[4]), two_decimal_places(zini[4]), two_decimal_places(lat_10[4]), two_decimal_places(lat_20[4])],
                ["",   "T_NV", two_decimal_places(kuhn_fast1[5]), two_decimal_places(kuhn_normal1[5]), two_decimal_places(kuhn_fast2[5]), two_decimal_places(kuhn_normal2[5]), two_decimal_places(betrag[5]), two_decimal_places(chr_20[5]), two_decimal_places(chr_ap[5]), two_decimal_places(latzel[5]), two_decimal_places(oppelt[5]), two_decimal_places(samal[5]), two_decimal_places(zini[5]), two_decimal_places(lat_10[5]), two_decimal_places(lat_20[5])]
            ]

    

            # collecting values for time_percent: Strejc_10_90
            str_10_t_u, str_10_t_g = strejc_10_90(t_10, t_90)

            # using the combination and calculating pid values
            betrag = betragsoptimum_pid(K_S, str_10_t_u, str_10_t_g)
            chr_20 = chien_hrones_reswick_20_percent_pid(K_S, str_10_t_u, str_10_t_g)
            chr_ap = chien_hrones_reswick_aperiodic_pid(K_S, str_10_t_u, str_10_t_g)
            latzel = latzel_pid(K_S, str_10_t_u, str_10_t_g)
            oppelt = oppelt_pid(K_S, str_10_t_u, str_10_t_g)
            samal = samal_pid(K_S, str_10_t_u, str_10_t_g)
            zini = ziegler_nichols_pid(K_S, str_10_t_u, str_10_t_g)


            # preparing table for printing with 2 decimal places
            table2 = [
                ["type of controller", "parameter", "Betragsoptimum", "CHR (20)", "CHR (aperiodic)", "Latzel (tangent)", "Oppelt", "Samal", "Ziegler/Nichols"],
                ["P",  "K_R",  two_decimal_places(betrag[0]), two_decimal_places(chr_20[0]), two_decimal_places(chr_ap[0]), two_decimal_places(latzel[0]), two_decimal_places(oppelt[0]), two_decimal_places(samal[0]), two_decimal_places(zini[0])],
                ["PI", "K_R",  two_decimal_places(betrag[1]), two_decimal_places(chr_20[1]), two_decimal_places(chr_ap[1]), two_decimal_places(latzel[1]), two_decimal_places(oppelt[1]), two_decimal_places(samal[1]), two_decimal_places(zini[1])],
                ["",   "T_N",  two_decimal_places(betrag[2]), two_decimal_places(chr_20[2]), two_decimal_places(chr_ap[2]), two_decimal_places(latzel[2]), two_decimal_places(oppelt[2]), two_decimal_places(samal[2]), two_decimal_places(zini[2])],
                ["PID","K_R",  two_decimal_places(betrag[3]), two_decimal_places(chr_20[3]), two_decimal_places(chr_ap[3]), two_decimal_places(latzel[3]), two_decimal_places(oppelt[3]), two_decimal_places(samal[3]), two_decimal_places(zini[3])],
                ["",   "T_N",  two_decimal_places(betrag[4]), two_decimal_places(chr_20[4]), two_decimal_places(chr_ap[4]), two_decimal_places(latzel[4]), two_decimal_places(oppelt[4]), two_decimal_places(samal[4]), two_decimal_places(zini[4])],
                ["",   "T_NV", two_decimal_places(betrag[5]), two_decimal_places(chr_20[5]), two_decimal_places(chr_ap[5]), two_decimal_places(latzel[5]), two_decimal_places(oppelt[5]), two_decimal_places(samal[5]), two_decimal_places(zini[5])]
            ]


            # collecting values for time_percent: Strejc_20_80
            str_20_t_u, str_20_t_g = strejc_20_80(t_20, t_80)

            # using the combination and calculating pid values
            betrag = betragsoptimum_pid(K_S, str_20_t_u, str_20_t_g)
            chr_20 = chien_hrones_reswick_20_percent_pid(K_S, str_20_t_u, str_20_t_g)
            chr_ap = chien_hrones_reswick_aperiodic_pid(K_S, str_20_t_u, str_20_t_g)
            latzel = latzel_pid(K_S, str_20_t_u, str_20_t_g)
            oppelt = oppelt_pid(K_S, str_20_t_u, str_20_t_g)
            samal = samal_pid(K_S, str_20_t_u, str_20_t_g)
            zini = ziegler_nichols_pid(K_S, str_20_t_u, str_20_t_g)


            # preparing table for printing with 2 decimal places
            table3 = [
                ["type of controller", "parameter", "Betragsoptimum", "CHR (20)", "CHR (aperiodic)", "Latzel (tangent)", "Oppelt", "Samal", "Ziegler/Nichols"],
                ["P",  "K_R",  two_decimal_places(betrag[0]), two_decimal_places(chr_20[0]), two_decimal_places(chr_ap[0]), two_decimal_places(latzel[0]), two_decimal_places(oppelt[0]), two_decimal_places(samal[0]), two_decimal_places(zini[0])],
                ["PI", "K_R",  two_decimal_places(betrag[1]), two_decimal_places(chr_20[1]), two_decimal_places(chr_ap[1]), two_decimal_places(latzel[1]), two_decimal_places(oppelt[1]), two_decimal_places(samal[1]), two_decimal_places(zini[1])],
                ["",   "T_N",  two_decimal_places(betrag[2]), two_decimal_places(chr_20[2]), two_decimal_places(chr_ap[2]), two_decimal_places(latzel[2]), two_decimal_places(oppelt[2]), two_decimal_places(samal[2]), two_decimal_places(zini[2])],
                ["PID","K_R",  two_decimal_places(betrag[3]), two_decimal_places(chr_20[3]), two_decimal_places(chr_ap[3]), two_decimal_places(latzel[3]), two_decimal_places(oppelt[3]), two_decimal_places(samal[3]), two_decimal_places(zini[3])],
                ["",   "T_N",  two_decimal_places(betrag[4]), two_decimal_places(chr_20[4]), two_decimal_places(chr_ap[4]), two_decimal_places(latzel[4]), two_decimal_places(oppelt[4]), two_decimal_places(samal[4]), two_decimal_places(zini[4])],
                ["",   "T_NV", two_decimal_places(betrag[5]), two_decimal_places(chr_20[5]), two_decimal_places(chr_ap[5]), two_decimal_places(latzel[5]), two_decimal_places(oppelt[5]), two_decimal_places(samal[5]), two_decimal_places(zini[5])]
            ]

    
    
    # print tables as dataframes in a separate window
    df1 = DataFrame(table1)
    df2 = DataFrame(table2)
    df3 = DataFrame(table3)
    show(all_pids=df1, strejc_10_90=df2, strejc_20_80=df3)
