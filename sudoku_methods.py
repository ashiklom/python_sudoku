"""
Methods for solving Sudoku grids.
"""

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
        ?? possibles: Dictionary of cell possibilities (from 'all_possibles')

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
    if fill_counter == 0 and len(possibles) > 0:
        raise FailedFirstPass("No single-possibility cells remaining. Try another method.")
    return grid



