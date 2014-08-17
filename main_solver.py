"""
Python Sudoku Solver
Main file containing solution process.
"""

from pprint import pprint as pp
from sudoku_methods import *
from sudoku_basic import *

def real_grid(difficulty):
    """Creates real unsolved Sudoku grid."""
    grid_easy = "015240000\n" + "000009021\n" + "002065049\n" + \
            "106000250\n" + "020000030\n" + "084000107\n" + \
            "850930600\n" + "240700000\n" + "000054370"
    grid_medium = "000400700\n" +"000010090\n" + "936070400\n" + \
            "802009030\n" + "500742009\n" + "090800204\n" + \
            "007080925\n" + "080020000\n" + "009001000\n"
    grid_hard = "700400030\n" + "015003000\n" + "006807000\n" + \
            "200300080\n" + "009000700\n" + "070002006\n" + \
            "000608200\n" + "000200390\n" + "030009001"
    grid_expert = "400700091\n" + "503900000\n" + "002680700\n" + \
            "002680700\n" + "010040080\n" + "004037200\n" + \
            "000000000\n" + "000002506\n" + "670008003"
    all_grids = {'easy': grid_easy, 'medium': grid_medium,
            'hard': grid_hard, 'expert': grid_expert}
    return all_grids[difficulty]


def solve(grid):
    """
    Solves the input Sudoku grid using several increasingly demanding strategies.
    
    Args:
        grid: Integer nested list representing Sudoku grid.

    Returns:
        Solved grid as nested list of integers.
    """
    pp(grid)
    possibles = all_possibles(grid)
    blank_counter = len(possibles)

    while blank_counter > 0:
        print("Blank cells remaining: ", blank_counter)
        grid, filled = fill_onepos(grid)

        print("Filled cells: ", filled)
        if filled == 0:
            print('Easy options depleted. Moving on to \'only place\' method')
            break
        blank_counter -= filled
        filled = 0

    while blank_counter > 0:
        print("Blank cells remaining: ", blank_counter)
        grid, filled_onlyplace = fill_onlyplace(grid)
        grid, filled_onepos = fill_onepos(grid)
        filled = filled_onlyplace + filled_onepos

        print("Filled cells: ", filled)
        if filled == 0:
            print('Only place method failed. Moving on to guessing.')
            break
        blank_counter -= filled
        filled = 0

    # while blank_counter > 0:
    #     try:
    #         grid = fill_clearpairs(grid)
    #         grid = fill_onlyplace(grid)
    #         grid = fill_onepos(grid)
    #
    #     except FailedThirdPass:
    #         break
    #
    #     except (FailedFirstPass, FailedSecondPass):
    #         pass
    #
    #     finally:
    #         blank_counter = len(possibles)

    if blank_counter > 0:
        print("Can't solve!")
    else:
        print("Grid solved!")
    pp(grid)
    return grid

# Only place
#   for 1-9
#       Get possible indices
#       Fill if only one possible index for row, column, box
# Guesser <-- DO FIRST
#   Set up grid rules
#   Annotate blank cells with possibilities
#   Loop through cells:
#       Start with cells with only 2 possibilities
#       Update blank cell possibilities after each guess

def quicksetup():
    a = int_to_grid(real_grid('easy'))
    b = int_to_grid(real_grid('medium'))
    c = int_to_grid(real_grid('hard'))
    d = int_to_grid(real_grid('expert'))
    return a,b,c,d

def main():
    a,b,c,d = quicksetup()
    solve(a)
    solve(b)
    solve(c)
    solve(d)

main()


