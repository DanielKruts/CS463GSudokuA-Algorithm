'''
    Desc: Implementation of A* Search Algorithm, to be imported to SudokuMain.py, where it will be used to calculate the optimal path
          for solving Sudoku Cube Puzzles.
    Last Changed: 9/15/2025
'''
import numpy as np
import math
# This is where our Heuristic for how close the cube is to be solved will go
def heuristic(cube):
    heuristicscores = []

    # loop over all 6 faces of the cube
    for side in [cube.Front, cube.Back, cube.Left, cube.Right, cube.Up, cube.Down]:
        heuristicface = np.array(side.facevalue)
        flat = heuristicface.flatten()
        missingvaluesface = 9 - len(np.unique(flat))

        heuristicscores.append(missingvaluesface)

    heuristicevaluation = math.ceil(max(heuristicscores) / 3)
    print(f"Heuristic evaluation of cube is {heuristicevaluation}")
    return heuristicevaluation
