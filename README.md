# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We iteratively shrink the size of the possible solution space by using
   logical constraints to eliminate possibilities while solving the puzzle.
   Just like all other constraints we use during the solution process, such 
   as removing an assigned box's digit from all the possible remaining values
   of the box's peers, the Naked Twins constraint allows us to use the fact
   that certain numbers MUST go in certain places to reason that they CAN'T go
   in other places. If 4 boxes in a unit all have had their possible assignments
   reduced to the same 4 digits, we know that none of those 4 digits can be 
   assigned to the other 5 boxes in the unit.  Thus the other boxes have a 
   reduced set of possibilities for their assignments.  This reduction then 
   can propogate further reductions within all the peers of the reduced squares
   by imposing tighter constraints on their possibilities, and so on.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We add constraints to the problem definition so that the solution space is
   more restricted at the start of the puzzle. By increasing the number of
   units from 27 to 29 and by increasing the number of peers from 20 to 26 for
   the 17 diagonal squares, we are able to reduce possible assignment values
   for many squares right from the start.  This in turn propogates further
   reductions for peers of the reduced squares, and so on.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.