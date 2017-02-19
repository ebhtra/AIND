

## Start with the constants and computed variables used in
##     the AIND classroom solutions, plus diagonal units:
    
rows = 'ABCDEFGHI'
cols = '123456789'
rev_cols = '987654321'

def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diag_unit_1 = [[rows[i] + cols[i] for i in range(len(rows))]]
diag_unit_2 = [[rows[i] + rev_cols[i] for i in range(len(rows))]]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI')
                              for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units + diag_unit_1 + diag_unit_2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


assignments = []

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

    # Find all instances of naked twins, triplets, etc.,
    ##  and remove their digits from unit peers
    for u in unitlist:
        vals = [values[box] for box in u if len(values[box]) > 1]
        twins = set([val for val in vals if len(val) == vals.count(val)])
        claimed = set([digit for digit in ''.join(twins)])
        for box in u:
            if len(values[box]) > 1 and values[box] not in twins:
                for c in claimed:
                    assign_value(values, box, values[box].replace(c,''))
    return values
            



def grid_values(grid):
    """ 
    Citation:  Copied from uitls.py in AIND classroom videos.
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Citation: Copied from utils.py in AIND classroom videos.
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Citation:  This is modified from AIND classroom video solution.
    
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

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
    Output: The resulting sudoku in dictionary form.
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
    """Using depth-first search and propagation, 
       create a search tree and solve the sudoku.
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
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    result = search(grid_values(grid))
    if not result:
        print('Cannot solve puzzle')
        return False
    else:
        return result
    
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
