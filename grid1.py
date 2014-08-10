"""
Python Sudoku Solver.
"""

from pprint import pprint as pp

def simple_test_grid():
    """Creates simple test grid that looks like:
    1234...
    1234...
    1234...
    ...
    1234"""
    grid = 9*"123456789\n"
    return grid

def real_grid():
    """Creates real unsolved Sudoku grid."""
    grid = "015240000\n" + "000009021\n" + "002065049\n" + \
            "106000250\n" + "020000030\n" + "084000107\n" + \
            "850930600\n" + "240700000\n" + "000054370"
    return grid


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
        grid: Integer nested list reprenting Sudoku grid.
        row: Row number of cell.
        col: Column number of cell.
        
    Returns:
        Integer list of values in box (top row [:3], middle [3:6], bottom [6:9]).
        """

    brow = row // 3
    bcol = col // 3
    row_start, row_end = brow * 3, (brow + 1) * 3
    col_start, col_end = bcol * 3, (bcol + 1) * 3
    box = [i for boxrow in grid[row_start:row_end] for i in boxrow[col_start:col_end] ]
    return box

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

    allvals = set(range(1,10))
    cellrow = set(get_row(grid, row_num))
    cellcol = set(get_column(grid, col_num))
    cellbox = set(get_box(grid, row_num, col_num))
    possibles = allvals - cellrow - cellcol - cellbox
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
# Count blank cells
# Identify blank cells by index
# While loop blank_cells > 0
# ----- STRATEGIES ------
# One Possibility
#   Initiate onepos_counter
#   Each cell has 9 possibilities - list (str?) 1-9
#   Eliminate possibilities as they are found in row, column, box
#   Fill in cells with 1 possibility (add to onepos_counter)
#   Break loop if onepos_counter = 0
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

def main():
    g = int_to_grid(real_grid())
    pp(all_possibles(g))


