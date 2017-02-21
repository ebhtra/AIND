
from sudokutils import *


assignments = []  # List used to keep track of the board as it's solved

def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    This also works for triplets and quadruplets, etc.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from unit peers.
    """
   
    for u in unitlist:
        # Find all instances of naked twins, triplets, etc.
        twins = find_twins(u, values)
        
        if twins:   # If naked twins were found
            # Trim all twin values from non-twin unit boxes
            values = trim_boxes(u, twins, values)
        
    return values
            
def find_twins(unit, values):
    """
    Within a unit of squares, find and return box values that exist within
    the unit exactly as many times as there are values in the box. 
    E.g., if there are 3 boxes with the value '789', or 4 with '1358', return
    that value. This method doesn't look for singletons (boxes that are already
    assigned), since that is taken care of by the eliminate() method.
    Args:
        unit(list): The squares in the unit, which must be keys in "values"
        values(dict): sudoku squares for keys and poss digit strings for values
    Returns:
        A set of the found twins (triplets, quadruplets, etc.)
    """
    # Only work on unassigned boxes
    vals = [values[box] for box in unit if len(values[box]) > 1]
    # Find and return box values that exist within the unit exactly 
    #   as many times as there are values in the box. 
    return set([val for val in vals if len(val) == vals.count(val)])
        
def trim_boxes(unit, twins, values):
    """
    Trim digits off possible assignments for sudoku squares
    Args:
        unit(list): The squares in the unit, which must be keys in @values
        twins(set): Strings of digits possible for assignment to a square
        values(dict): sudoku squares for keys and poss digit strings for values
    Returns:
        The values dict with, hopefully, reduced values
    """
    # Reduce the set of twins values to whichever digits they comprise.
    claimed = set([digit for digit in ''.join(twins)])
    for box in unit:
    # Use the sets of twins and claimed digits to reduce the remaining
    #   possibilities for the other boxes within the same unit.
    # Only look at unassigned boxes not in the twins set
        if len(values[box]) > 1 and values[box] not in twins:
            for c in claimed:
                # Remove any claimed digits from these boxes
                assign_value(values, box, values[box].replace(c,'')) 
    return values


def eliminate(values):
    """Citation:  This is modified from AIND classroom video solution.
    
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
            
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    unsolved = [box for box in values if len(values[box]) > 1]
    for box in unsolved:
        links = units[box]
        for unit in links:
            left = ''.join([values[b] for b in unit])
            for digit in values[box]:
                if left.count(digit) == 1:
                    assign_value(values, box, digit)
                    break
    
    return values


def reduce_puzzle(values):
    """ As provided by AIND class solution, with adjustments:
    Iterate through eliminate(), only_choice(), and naked_twins().
    If at some point, there is a box with no available values, the
      puzzle is unsolvable, so return False.
    If after an iteration of the three functions, the sudoku remains the same, 
      return the sudoku, in its (possibly solved) stalled state.
    
    Input: A sudoku in dictionary form.
    Output: The same sudoku dict with hopefully shorter values
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys()
                                      if len(values[box]) == 1])
        ## Use the 3 constraint functions
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        ## Check if anything has changed during this iteration
        solved_values_after = len([box for box in values.keys()
                                     if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        ## Halt puzzle-solving if unsolvable under current assignments
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Use depth-first search to propogate a search tree: Try assigning a digit
    in a box with the fewest remaining options. If that doesn't return an 
    unsolveable puzzle, then recursively search its offspring until a legal 
    solution is returned.  Anytime an assignment leads to a dead end, return 
    False to backtrack up to the last part of the tree with remaining options.
    """
    ## Reduce the problem size
    vals = reduce_puzzle(values)
    ## Backtrack if unsolvable with current assignments
    if not vals:  
        return False
    ## Return solution if all squares are assigned
    if len(''.join(vals.values())) == len(rows)*len(cols):
        return vals
    
    ## Else choose one of the unfilled squares with the fewest possibilities
    best = min([box for box in vals if len(vals[box]) > 1],
                key=lambda x: len(vals[x]))
    
    ## Now use recursion to solve each one of the resulting sudokus,
    ##  and if one returns a value (not False), return it
    for digit in vals[best]:
        newVals = vals.copy()
        newVals[best] = digit
        assign_value(values, best, digit)
        result = search(newVals)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid: a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4\
                      ....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. 
        False if no solution exists.
    """
    result = search(grid_values(grid))
    if not result:
        # No more backtracking possible, so puzzle is unsolveable
        print('Cannot solve puzzle')
        return False
    else:
        return result
    
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4..\
                          .4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a \
               problem! It is not a requirement.')
