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
    Fills cells that have only one possible value (determined by 'all_possibles').

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


    def unique_val(numlist, possibles):
        """Scans a Sudoku row, column, or box for missing values, \
        identifies if there is only one place missing values can appear, \
        and returns their index in numlist.

        Args:
            numlist: List of ints and 'None's as produced by the get_row, etc. \
                functions
            possibles: Nested list of possible values for blank cells, based on \
                list comprehension with 'get_possibles' function

        Returns:
            Tuple of unique value index, its value.
        """
        missing = get_missing(numlist)
        for m in missing:
            present_counter = 0
            for ind, val in enumerate(possibles):
                if m in val:
                    present_counter += 1
                    return_ind = ind
                if present_counter == 1:
                    return return_ind, m
                else:
                    return None

    fill_counter = 0
    while fill_counter == 0:
        for row_num, row in enumerate(grid):
            missing = get_missing(row)
            blanks = find_blanks(row)
            possibles_in_row = [get_possibles(grid, row_num, col_num) for col_num in blanks]
            for m in missing:
                present_counter = 0
                for ind, val in enumerate(possibles_in_row):
                    if m in val:
                        present_counter += 1
                        col_num = ind
                if present_counter == 1:
                    grid[row_num][col_num] = m
                    fill_counter += 1

        for col_num in range(9):
            column = get_column(grid, col_num)
            missing = get_missing(column)
            blanks = find_blanks(column)
            possibles_in_column = [get_possibles(grid, row_num, col_num) for row_num in blanks]
            for m in missing:
                present_counter = 0
                for ind, val in enumerate(possibles_in_column):
                    if m in val:
                        present_counter += 1
                        row_num = ind
                if present_counter == 1:
                    grid[row_num][col_num] = m
                    fill_counter += 1

        for box_row in range(0, 9, 3):
            for box_column in range(0, 9, 3):
                box = get_box(grid, box_row, box_column)
                missing = get_missing(box)
                blanks = find_blanks(box)
                blanks_index = [box_ref(ind, box_row, box_column) for ind in blanks]
                possibles_in_box = [get_possibles(grid, row_num, col_num)
                                    for (row_num, col_num) in blanks_index]
                for m in missing:
                    present_counter = 0
                    for ind, val in enumerate(possibles_in_box):
                        if m in val:
                            present_counter += 1
                            box_num = ind
                        if present_counter == 1:
                            row_num, col_num = box_ref(box_num, box_row, box_column)
                            fill_counter += 1



