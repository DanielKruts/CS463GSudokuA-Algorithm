'''
    Desc: Implementation of A* Search Algorithm, to be imported to SudokuMain.py, where it will be used to calculate the optimal path
          for solving Sudoku Cube Puzzles.
    Last Changed: 9/15/2025
'''
import numpy as np
import math
import heapq
import copy
import ClassDef
from ClassDef import *

def hashmapadd(cube, cubecounter, movecounter):
    keyinitialize = str(cubecounter) + "&" + str(movecounter)
    Hashmap.MovementHashmap[keyinitialize] = cube
    movecounter += movecounter;
    return cubecounter, movecounter

def hashmapaccess(cubecounter, movecounter):
    return Hashmap.MovementHashmapp[str(cubecounter) + "&" + str(movecounter)]

def hashmapprint():
    for key in Hashmap.MovementHashmapp.items():
        print(f"{key}")



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


# This will take the starting cube input into the function and try to solve using A* Search Algorithm

def a_star_search(start_cube):
    open_dict = {} # Dictionary to hold nodes for quick lookup
    closed_dict = {} # Dictionary to hold visited nodes to easily know if we've been there
    
    open_list = [] # Our priority queue for nodes to explore
    start_node = Node(start_cube, g=0, h=heuristic(start_cube))

    heapq.heappush(open_list, start_node)