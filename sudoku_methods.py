"""
Methods for solving Sudoku grids.
"""

from sudoku_basic import *


def get_possibles(grid, row_num, col_num):
    """
    For cell in specified row and column, test if occupied. If unoccupied, \
            return list of possible values.

        Args:
            row_num: Row number (0-8) of cell.
            col_num: Column number (0-8) of cell.

        Returns:
            List of possible values for cell.
    """

    allvals = set(range(1, 10))
    cellrow = set(get_row(grid, row_num))
    cellcol = set(get_column(grid, col_num))
    cellbox = set(get_box(grid, row_num, col_num))
    possibles = list(allvals - cellrow - cellcol - cellbox)
    possibles.sort()
    return possibles


def all_possibles(grid):
    """
    Returns dictionary containing indices tuple (key) and possibility list (value) \
            of all blank cells in a Sudoku grid.

    Args:
        grid: Integer nested list representing Sudoku grid.

    Returns:
        Dictionary with keys as indices and possibility list as values for all blank \
                cells.
    """

    def pairwise_remove(possibles):
        """
        Scans a dictionary of possibles for pair-possibles within the same row/column/box \
            and removes the possibilities from other cells within the same row/column/box, \
            returning an updated, shorter dictionary.

        Args:
            possibles: Dictionary of possible values keyed by grid cell index.

        Returns:
            Updated dictionary of possibles with pairs removed.
        """

        def identify_removal_pairs(possibles_subset):
            """
            Sets up values to remove and their respective indices.
            """

            set_for_removal = []
            ind_for_removal = [key for key in possibles_subset]
            for ind, item in possibles_subset.items():
                if len(item) == 2 and list(possibles_subset.values()).count(item) == 2:
                    set_for_removal.append(item)
                    ind_for_removal.remove(ind)
            set_for_removal = set([val for pair in set_for_removal for val in pair])
            return ind_for_removal, set_for_removal

        for row_num in range(9):
            row_possibles = {}
            for (row_ind, col_ind), val in possibles.items():
                if row_ind == row_num:
                    row_possibles[col_ind] = val
            if len(row_possibles) > 2:
                ind_for_removal, set_for_removal = identify_removal_pairs(row_possibles)
                for ind in ind_for_removal:
                    for val in set_for_removal:
                        if val in possibles[(row_num, ind)]:
                            possibles[(row_num, ind)].remove(val)

        for col_num in range(9):
            col_possibles = {}
            for (row_ind, col_ind), val in possibles.items():
                if col_ind == col_num:
                    col_possibles[row_ind] = val
            if len(col_possibles) > 2:
                ind_for_removal, set_for_removal = identify_removal_pairs(col_possibles)
                for ind in ind_for_removal:
                    for val in set_for_removal:
                        if val in possibles[(ind, col_num)]:
                            possibles[(ind, col_num)].remove(val)

        for box_row in range(3):
            for box_column in range(3):
                box_possibles = {}
                for (row_ind, col_ind), val in possibles.items():
                    if row_ind // 3 == box_row and col_ind // 3 == box_column:
                        box_possibles[(row_ind, col_ind)] = val
                if len(box_possibles) > 2:
                    ind_for_removal, set_for_removal = identify_removal_pairs(box_possibles)
                    for ind in ind_for_removal:
                        for val in set_for_removal:
                            if val in possibles[ind]:
                                possibles[ind].remove(val)

        return possibles

    all_possibles = {}

    for row_num, row in enumerate(grid):
        for col_num, cell in enumerate(row):
            if not cell:
                all_possibles[row_num, col_num] = get_possibles(grid, row_num, col_num)


    all_possibles = pairwise_remove(all_possibles)
    return all_possibles


def fill_onepos(grid):
    """
    Fills cells that have only one possible value (determined by 'all_possibles').

    Args:
        grid: Integer nested list representing Sudoku grid.

    Returns:
        Tuple of updated grid (nested list of integers and 'None' values) and \
            integer value of cells filled.

    Raises:
        FailedFirstPass: If no cells can be filled via the obvious method.
    """

    possibles = all_possibles(grid)
    length_counter = len(possibles)
    if length_counter == 0:
        return grid, 0
    fill_counter = 0
    for ind, val in possibles.items():
        if len(val) == 1:
            grid[ind[0]][ind[1]] = val[0]
            fill_counter += 1

    return grid, fill_counter


def fill_onlyplace(grid):
    """Fills cells that are the only possible place for \
            a particular value.

    Args:
        grid: Integer nested list representing Sudoku grid.

    Returns:
        Updated grid (nested list of integers and 'None' values) and \
            integer value of cells filled.

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
            List of tuples of unique value index (relative!! Use blanks[ind] for \
                actual reference), its value; or 'None' if no unique values found.
        """
        missing = get_missing(numlist)
        unique_vals = []
        for m in missing:
            present_counter = 0
            for ind, val in enumerate(possibles):
                if m in val:
                    present_counter += 1
                    return_ind = ind
            if present_counter == 1:
                unique_vals.append((return_ind, m))
        if len(unique_vals) > 0:
            return unique_vals
        else:
            return None

    fill_counter = 0
    for row_num, row in enumerate(grid):
        blanks = find_blanks(row)
        possibles_in_row = [get_possibles(grid, row_num, col_num) for col_num in blanks]
        unique = unique_val(row, possibles_in_row)
        if unique is not None:
            for blanks_num, value in unique:
                grid[row_num][blanks[blanks_num]] = value
                fill_counter += 1

    for col_num in range(9):
        column = get_column(grid, col_num)
        blanks = find_blanks(column)
        possibles_in_column = [get_possibles(grid, row_num, col_num) for row_num in blanks]
        unique = unique_val(column, possibles_in_column)
        if unique is not None:
            for blanks_num, value in unique:
                grid[blanks[blanks_num]][col_num] = value
                fill_counter += 1

    for box_row in range(0, 9, 3):
        for box_column in range(0, 9, 3):
            box = get_box(grid, box_row, box_column)
            blanks = find_blanks(box)
            blanks_index = [box_ref(ind, box_row, box_column) for ind in blanks]
            possibles_in_box = [get_possibles(grid, row_num, col_num)
                                for (row_num, col_num) in blanks_index]
            unique = unique_val(box, possibles_in_box)
            if unique is not None:
                for blanks_num, value in unique:
                    row_num, col_num = box_ref(blanks[blanks_num], box_row, box_column)
                    grid[row_num][col_num] = value
                    fill_counter += 1

    return grid, fill_counter





