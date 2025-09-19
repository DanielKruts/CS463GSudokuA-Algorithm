'''
    Desc: Cube classes for SudokuMain.py
    Last Updated: 9/17/2025
'''
import numpy as np
import math
import heapq
import copy

class CubeSide:
    # self initialization created for CubeSide to fix centervalue variable issues
    def __init__(self, facevalue, centercolor):
        self.facevalue = facevalue
        self.centercolor = centercolor
        self.centervalue = str(facevalue[1][1]) + self.centercolor

#Creates a cube with 6 predetermined sides of a solved cube
class Cube:
    def __init__(self):
        self.Front = CubeSide([[9, 5, 2], [3, 8, 1], [6, 7, 4]], 'Y')
        self.Back = CubeSide([[9, 5, 2], [3, 8, 1], [6, 7, 4]], 'P')
        self.Left = CubeSide([[7, 1, 8], [2, 4, 6], [9, 3, 5]], 'B')
        self.Right = CubeSide([[4, 6, 3], [7, 5, 9], [1, 2, 8]], 'G')
        self.Up = CubeSide([[8, 1, 3], [4, 6, 7], [2, 9, 5]], 'O')
        self.Down = CubeSide([[1, 2, 8], [5, 3, 9], [7, 4, 6]], 'R')

# Class Movement
class Movement:
    '''
    Self initialization takes multiple parameters
    cube - the whole Cube object
    face - which face the move applies to ("Front", "Left", "Right", etc.)
    colRow - "C" (column) or "R" (row)
    position - 0 (left/top) or 2 (right/bottom)
    direction - 0 or 1 (clockwise/counterclockwise or down/up/left/right depending on context)
    name - shorthand label like "FC00"
    '''
    def __init__(self, cube, face, colrow, position, direction, name, path=None):
        self.cube = cube
        self.face = face
        self.colRow = colrow
        self.position = position
        self.direction = direction
        self.name = name
        self.path = path if path is not None else []

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

class Hashmap:
    def __init__(self):
        self.MovementHashmap = dict()