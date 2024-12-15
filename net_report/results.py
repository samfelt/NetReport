from tabulate import tabulate
from .colors import colors as c

def print_group_table(title, table, fmt="outline"):
    """
    Print a nicely formatted table with a single line for the title and the
    2D list as table the table below it
    """

    p_table = tabulate(table, tablefmt=fmt)
    width = len(p_table.split("\n")[0])
    top_line = "+" + ("-" * (width-2)) + "+"
    title_line = "| " + f"{c.Bold}{title: <{width-3}}{c.NoC}" + "|"
    print(top_line)
    print(title_line)
    print(p_table)
