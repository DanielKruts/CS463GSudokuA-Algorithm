'''
    Desc: Implementation of A* Search Algorithm, to be imported to SudokuMain.py, where it will be used to calculate the optimal path
          for solving Sudoku Cube Puzzles.
    Last Changed: 9/15/2025
'''
import numpy as np
import math
import heapq
import copy
import CubeClass
from CubeClass import Cube, CubeSide, Movement

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

class Node:
    # Initialization takes a cube object, heuristic value, cost to reach node, and parent node(Another cube object)
    def __init__(self, cube, g=0, h=0, parent=None):
        self.cube = copy.deepcopy(cube) # State of Cube
        self.g = g # Cost to reach node
        self.h = h  # Heuristic(cube)
        self.parent = parent # Parent Node
        self.f = g + h # Total Cost

    def __eq__(self, other): # Defines equality function for comparing Node objects
        return self.cube == other.cube

    def __lt__(self, other): # Defines less than function for Node objects (Makes priority queue work)
        return self.f < other.f


# This will take the starting cube input into the function and try to solve using A* Search Algorithm

def a_star_search(start_cube):
    open_dict = {} # Dictionary to hold nodes for quick lookup
    closed_dict = {} # Dictionary to hold visited nodes to easily know if we've been there
    
    open_list = [] # Our priority queue for nodes to explore
    start_node = Node(start_cube, g=0, h=heuristic(start_cube))

    heapq.heappush(open_list, start_node)