"""
Basic Sudoku grid functions.
"""


def int_to_grid(intgrid):
    """
    Creates grid (list of lists; [row][column]) from string of line-separated integers.\
            All '0' values are converted to 'None' objects, all others converted to 'int'.

        Args:
            intgrid: String of line-separated integers.

        Returns:
            Sudoku grid in the form of integer list of lists [row][column] with blank cells\
                    indicated by 'None' objects.
    """

    grid = [list(i) for i in intgrid.split()]
    grid = [[int(i) if i != '0' else None for i in row] for row in grid]
    return grid


def get_row(grid, num):
    """Extract row of index 'num' from grid as list.
    
    Args:
        grid: Integer nested list representing Sudoku grid.
        num: Row number (0-8)
        
    Returns:
        List of integers in row. 'None' values are unoccupied cells."""

    row = grid[num]
    return row


def get_column(grid, num):
    """Extract column of index 'num' from grid as list.
    
    Args:
        grid: Integer nested list representing Sudoku grid.
        num: Column number (0-8)
        
    Returns:
        List of integers in column. 'None' values are unoccupied cells."""

    column = [row[num] for row in grid]
    return column


def get_box(grid, row, col):
    """Extract box by row-column location of cell.
    
    Args:
        grid: Integer nested list representing Sudoku grid.
        row: Row number of cell.
        col: Column number of cell.
        
    Returns:
        Integer list of values in box (top row [:3], middle [3:6], bottom [6:9]).
        """

    brow = row // 3
    bcol = col // 3
    row_start, row_end = brow * 3, (brow + 1) * 3
    col_start, col_end = bcol * 3, (bcol + 1) * 3
    box = [i for boxrow in grid[row_start:row_end] for i in boxrow[col_start:col_end]]
    return box


def box_ref(ind, box_row, box_col):
    """Retrieve absolute grid index (as tuple) of a cell from its \
            box position.

    Args:
        ind: Index of cell within box list
        box_row: Starting row of box (coerced to 0, 3, or 6)
        box_col: Starting column of box (coerced to 0, 3, or 6)

    Returns:
        Tuple of row, column indices for the specified cell.

    """
    box_row = box_row // 3 * 3
    box_col = box_col // 3 * 3
    relative_row = ind // 3
    relative_col = ind % 3
    absolute_row = relative_row + box_row
    absolute_col = relative_col + box_col
    return absolute_row, absolute_col


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
    all_possibles = {}

    for row_num, row in enumerate(grid):
        for col_num, cell in enumerate(row):
            if not cell:
                all_possibles[row_num, col_num] = get_possibles(grid, row_num, col_num)

    return all_possibles


def get_missing(numlist):
    """
    Retreive list of missing values from a row, column, or box.

    Args:
        numlist: A list of ints and Nones as produced by the get_row, etc. \
                functions.

    Returns:
        List of ints missing from given section.
    """

    allvals = set(range(1, 10))
    missing = list(allvals - set(numlist))
    return missing


def find_blanks(numlist):
    """Retreive indices of all blank cells in row, column, or box.

    Args:
        numlist: A list of ints and Nones as produced by the get_row, etc. \
                functions.

    Returns:
        List of indices of blank cells from given section.
    """
    blanks = []
    for ind, val in enumerate(numlist):
        if val == None:
            blanks.append(ind)

    return blanks
