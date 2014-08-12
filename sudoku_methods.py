"""
Methods for solving Sudoku grids.
"""

from sudoku_basic import *


class FailedFirstPass(Exception):
    pass


class FailedSecondPass(Exception):
    pass


class FailedThirdPass(Exception):
    pass


def fill_onepos(grid):
    """
    Fills cells that have only one possibile value (determined by 'all_possibles').

    Args:
        grid: Integer nested list representing Sudoku grid.

    Returns:
        Updated grid (nested list of integers and 'None' values) 

    Raises:
        FailedFirstPass: If no cells can be filled via the obvious method.
    """

    possibles = all_possibles(grid)
    length_counter = len(possibles)
    fill_counter = 0
    for ind, val in possibles.items():
        if len(val) == 1:
            grid[ind[0]][ind[1]] = val[0]
            fill_counter += 1
            length_counter = len(possibles)
#    pp(all_possibles(grid))
    if fill_counter == 0 and length_counter > 0:
        raise FailedFirstPass("No single-possibility cells remaining. Try another method.")
    return grid


def fill_onlyplace(grid):
    """Fills cells that are the only possible place for \
            a particular value.

    Args:

        grid: Integer nested list representing Sudoku grid.
    Returns:
        Updated grid (nested list of integers and 'None' values)

    Raises:
        FailedSecondPass: If no cells can be filled via this method.
    """

    fill_counter = 0
    while fill_counter == 0:
        for rownum, row in enumerate(grid):
            missing = get_missing(row)
            blanks = find_blanks(row)
            possibles_in_row = [get_possibles(grid, rownum, col_num) for col_num in blanks]
            #TODO: Find unique occurence of a value in 'missing' in above and fill by index



