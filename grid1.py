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
    grid_medium = 
    grid_hard = 
    grid_expert = 
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
    possibles = all_possibles(grid)
    blank_counter = len(possibles)
    
    while blank_counter > 0:
        try:
            grid = fill_onepos(grid)

        except FailedFirstPass:
            break

        finally:
            blank_counter = len(possibles)

    while blank_counter > 0:
        try:
            grid = fill_onlyplace(grid)
            grid = fill_onepos(grid)

        except FailedSecondPass:
            break

        except FailedFirstPass:
            pass

        finally:
            blank_counter = len(possibles)

    while blank_counter > 0:
        try:
            grid = fill_clearpairs(grid)
            grid = fill_onlyplace(grid)
            grid = fill_onepos(grid)

        except FailedThirdPass:
            break

        except (FailedFirstPass, FailedSecondPass):
            pass

        finally:
            blank_counter = len(possibles)

    print("Grid solved!")
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


