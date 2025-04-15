from functions.procedure import procedure
from functions.print_pid_table import print_possible_pid_table

type, order, values = procedure()

print_possible_pid_table(type, order, values)
