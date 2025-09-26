'''
    Desc: Implementation of A* Search Algorithm, to be imported to SudokuMain.py, where it will be used to calculate the optimal path
          for solving Sudoku Cube Puzzles.
    Last Changed: 9/15/2025
'''
from sysconfig import get_path
import numpy as np
import math
import heapq
import copy
import random
from ClassDef import *



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
    #print(f"Heuristic evaluation of cube is {heuristicevaluation}")
    return heuristicevaluation


# Determines whether to apply a column or row moved based on the Movement object passed to it
def applyMovement(newCube, movement, path):
    if movement.colRow == "C":  # column move
        applyColumnMove(newCube, movement, path)
    elif movement.colRow == "R":  # row move
        applyRowMove(newCube, movement, path)
    else:
        print("Invalid Movement type")
        exit()

# Takes a given Cube, Movement, and path to rotate the appropriate face and apply the correct column move
def applyColumnMove(cube, movement, path):
    print("Cube name:", cube.cubename, "| Move code:", movement.name, "| face:", movement.face, "| col/row:", movement.colRow, "| pos:", movement.position, "| dir:", movement.direction)
    if movement.face == "Front":
        if movement.position == 0:  # Left column
            if movement.direction == 0:  # Down
                cube.Left.facevalue = rotate_face_clockwise(cube.Left.facevalue)
            else:  # Up
                cube.Left.facevalue = rotate_face_counterclockwise(cube.Left.facevalue)
        elif movement.position == 2:  # Right column
            if movement.direction == 0:  # Down
                cube.Right.facevalue = rotate_face_counterclockwise(cube.Right.facevalue)
            else:  # Up
                cube.Right.facevalue = rotate_face_clockwise(cube.Right.facevalue)
        else:
            print("Invalid column for Front move")
            exit()
        move(movement, path)
    elif movement.face == "Left":
        if movement.position == 0:  # Left column
            if movement.direction == 0:  # Down
                cube.Back.facevalue = rotate_face_clockwise(cube.Back.facevalue)
            else:  # Up
                cube.Back.facevalue = rotate_face_counterclockwise(cube.Back.facevalue)
        elif movement.position == 2:  # Right column
            if movement.direction == 0:  # Down
                cube.Front.facevalue = rotate_face_counterclockwise(cube.Front.facevalue)
            else:  # Up
                cube.Front.facevalue = rotate_face_clockwise(cube.Front.facevalue)
        else:
            print("Invalid column for Left move")
            exit()
        move(movement, path)
    else:
        print("Invalid face for column move")
        exit()

# Takes the given Cube, Movement, and path to correctly rotate the appropriate face and apply the correct row move
def applyRowMove(cube, movement, path):
    print("Cube name:", cube.cubename, "| Move code:", movement.name, "| face:", movement.face, "| col/row:", movement.colRow, "| pos:", movement.position, "| dir:", movement.direction)
    if movement.face == "Front":
        if movement.position == 0:  # Top row
            if movement.direction == 0:  # Left
                cube.Up.facevalue = rotate_face_clockwise(cube.Up.facevalue)
            else:  # Right
                cube.Up.facevalue = rotate_face_counterclockwise(cube.Up.facevalue)
        elif movement.position == 2:  # Bottom row
            if movement.direction == 0:  # Left
                cube.Down.facevalue = rotate_face_counterclockwise(cube.Down.facevalue)
            else:  # Right
                cube.Down.facevalue = rotate_face_clockwise(cube.Down.facevalue)
        else:
            print("Invalid row for Front move")
            exit()
        move(movement, path)
    else:
        print("Invalid face for row move")
        exit()

# Returns the path of face given a movement object
def get_path_from_movement(cube, movement):
    """
    Returns the faces and strip orientation for a move.
    face: "Front", "Left", etc.
    colRow: "C" for column, "R" for row
    position: 0 (left/top) or 2 (right/bottom)
    Returns: path_faces [4 CubeSides], path_orientations ["row2", "col0", ...]
    """
    face = movement.face
    colRow = movement.colRow
    if colRow == "C":  # Column moves
        if face == "Front":
            return [cube.Front, cube.Up, cube.Back, cube.Down]
        elif face == "Left":
            return [cube.Left, cube.Up, cube.Right, cube.Down]
    elif colRow == "R":  # Row moves
        return [cube.Front, cube.Right, cube.Back, cube.Left]
    else:
        print("Invalid Parameters")
        exit()
# Rotates a given facevalue clockwise
def rotate_face_clockwise(face):
    return [list(row) for row in zip(*face[::-1])]
# Rotates a given facevalue counterclockwise
def rotate_face_counterclockwise(face):
    return [list(row) for row in zip(*face)][::-1]
#Moves the front face clockwise or counterclockwise, considering the parameter wise, (0 is clockwise, 1 is counterclockwise)
def move(movement, path):
    """
    Rotates the edge strips around a given face.
    - cube: full Cube object
    - face: the CubeSide being rotated
    - direction: 0 = clockwise, 1 = counterclockwise
    - path: list of 4 CubeSides in the order they wrap around the face
    """
    if movement.face == "Front":
        if movement.colRow == "R": # Row move
            if movement.position == 0: # Top row
                temp = path[0].facevalue[0][:]
                if movement.direction == 0: # Clockwise
                    path[0].facevalue[0][:] = path[1].facevalue[0][:]
                    path[1].facevalue[0][:] = path[2].facevalue[0][:]
                    path[2].facevalue[0][:] = path[3].facevalue[0][:]
                    path[3].facevalue[0][:] = temp
                elif movement.direction == 1: # Counterclockwise
                    path[0].facevalue[0][:] = path[3].facevalue[0][:]
                    path[3].facevalue[0][:] = path[2].facevalue[0][:]
                    path[2].facevalue[0][:] = path[1].facevalue[0][:]
                    path[1].facevalue[0][:] = temp
            elif movement.position == 2: # Bottom row
                temp = path[0].facevalue[2][:]
                if movement.direction == 0: # Counterclockwise
                    path[0].facevalue[2][:] = path[1].facevalue[2][:]
                    path[1].facevalue[2][:] = path[2].facevalue[2][:]
                    path[2].facevalue[2][:] = path[3].facevalue[2][:]
                    path[3].facevalue[2][:] = temp
                elif movement.direction == 1: # Clockwise
                    path[0].facevalue[2][:] = path[3].facevalue[2][:]
                    path[3].facevalue[2][:] = path[2].facevalue[2][:]
                    path[2].facevalue[2][:] = path[1].facevalue[2][:]
                    path[1].facevalue[2][:] = temp
        elif movement.colRow == "C": # Column move
            if movement.position == 0: # Left column
                temp = [row[0] for row in path[0].facevalue]
                if movement.direction == 0: # Up
                    for i in range(3):
                        path[0].facevalue[i][0] = path[1].facevalue[i][0]
                    for i in range(3):
                        path[1].facevalue[i][0] = path[2].facevalue[2-i][2]
                    for i in range(3):
                        path[2].facevalue[i][2] = path[3].facevalue[2-i][0]
                    for i in range(3):
                        path[3].facevalue[i][0] = temp[i]
                elif movement.direction == 1: # Down
                        for i in range(3):    
                            path[0].facevalue[i][0] = path[3].facevalue[i][0]
                        for i in range(3):    
                            path[3].facevalue[i][0] = path[2].facevalue[2-i][2]
                        for i in range(3):
                            path[2].facevalue[i][2] = path[1].facevalue[2-i][0]
                        for i in range(3):
                            path[1].facevalue[i][0] = temp[i]
            elif movement.position == 2: # Right column
                temp = [row[2] for row in path[0].facevalue]
                if movement.direction == 0: # Down  
                    for i in range(3):
                        path[0].facevalue[i][2] = path[1].facevalue[i][2]
                    for i in range(3):
                        path[1].facevalue[i][2] = path[2].facevalue[2-i][0]
                    for i in range(3):
                        path[2].facevalue[i][0] = path[3].facevalue[2-i][2]
                    for i in range(3):
                        path[3].facevalue[i][2] = temp[i]
                elif movement.direction == 1: #Up
                    for i in range(3):
                        path[0].facevalue[i][2] = path[3].facevalue[i][2]
                    for i in range(3):
                        path[3].facevalue[i][2] = path[2].facevalue[2-i][0]
                    for i in range(3):
                        path[2].facevalue[i][0] = path[1].facevalue[2-i][2]
                    for i in range(3):
                        path[1].facevalue[i][2] = temp[i]
    elif movement.face == "Left":
        if movement.position == 0: #Left column
            temp = [row[0] for row in path[0].facevalue]
            if movement.direction == 0: # Up
                for i in range(3):
                    path[0].facevalue[2-i][0] = path[1].facevalue[0][i]
                for i in range(3):
                    path[1].facevalue[0][i] = path[2].facevalue[i][2]
                for i in range(3):
                    path[2].facevalue[i][2] = path[3].facevalue[2][2-i]
                for i in range(3):
                    path[3].facevalue[2][i] = temp[i]
            elif movement.direction == 1: # Down
                for i in range(3):
                    path[0].facevalue[i][0] = path[3].facevalue[2][i]
                for i in range(3):
                    path[3].facevalue[2][2-i] = path[2].facevalue[i][2]
                for i in range(3):
                    path[2].facevalue[i][2] = path[1].facevalue[0][i]
                for i in range(3):
                    path[1].facevalue[0][i] = temp[2-i]
        elif movement.position == 2: # Right column
            temp = [row[2] for row in path[0].facevalue]
            if movement.direction == 0: # Down
                for i in range(3):
                    path[0].facevalue[i][2] = path[1].facevalue[2][2-i]
                for i in range(3):
                    path[1].facevalue[2][i] = path[2].facevalue[i][0]
                for i in range(3):
                    path[2].facevalue[i][0] = path[3].facevalue[0][2-i]
                for i in range(3):
                    path[3].facevalue[0][i] = temp[i]
            elif movement.direction == 1: # Up
                for i in range(3):
                    path[0].facevalue[i][2] = path[3].facevalue[0][i]
                for i in range(3):
                    path[3].facevalue[0][i] = path[2].facevalue[2-i][0]
                for i in range(3):
                    path[2].facevalue[i][0] = path[1].facevalue[2][i]
                for i in range(3):
                    path[1].facevalue[2][i] = temp[2-i]
def printCube(cubeObject):
    # Takes a looper iterating through the desired values of the sides of the cube and prints them in a readable format
    for i in [cubeObject.Up]:
        print(f"\t {i.facevalue[0]}\n\t {i.facevalue[1]}\n\t {i.facevalue[2]}")
    
    for i in [cubeObject.Left, cubeObject.Front, cubeObject.Right, cubeObject.Back]:
         print(i.facevalue[0], end="")
    print("")
    for i in [cubeObject.Left, cubeObject.Front, cubeObject.Right, cubeObject.Back]:
         print(i.facevalue[1], end="")
    print("")
    for i in [cubeObject.Left, cubeObject.Front, cubeObject.Right, cubeObject.Back]:
         print(i.facevalue[2], end="")
    print("")
    for i in [cubeObject.Down]:
         print(f"\t {i.facevalue[0]}\n\t {i.facevalue[1]}\n\t {i.facevalue[2]}")
    print("")

def randomizer(movelist, movevalue, previous_var, cubeObject):
    printCube(cubeObject)
    print("Applying random move(s)")
    for i in range(0, movevalue):
        random_var = random.randint(0, 11)
        while random_var == previous_var:
            print("Repeat move, rerolling")
            random_var = random.randint(0, 11)
        movechosen = movelist[random_var]
        pathprint = get_path_from_movement(cubeObject, movechosen)
        #print("Path is", [side.centercolor for side in pathprint[0]], "with orientations", pathprint[1])
        applyMovement(cubeObject, movechosen, pathprint)

        printCube(cubeObject)
        heuristic(cubeObject)
        previous_var = random_var
    return previous_var

# This will take the starting cube input into the function and try to solve using A* Search Algorithm
def a_star_search(startCube, movelist, nummoves):
    open_heap = []                      # will contain tuples (f, counter, node)
    closed_set = set()                  # stores cube_key(...) of expanded nodes
    g_scores = {}                       # maps cube_key -> g
    counter = 0                         # tie-breaker for heap

    movecounter = 0

    start_h = heuristic(startCube)
    start_node = Node(startCube, g=0, h=start_h)
    start_node.f = start_node.g + start_node.h

    heapq.heappush(open_heap, start_node)
    counter += 1
    g_scores[startCube] = 0

    while open_heap:
        current = heapq.heappop(open_heap)
        current_key = current.cube
        print("Visiting Node with h:", current.h, " g:", current.g, " f:", current.f)

        # If already expanded (we may have a stale entry), skip
        if current_key in closed_set:
            # stale entry, skip
            continue

        # Goal test
        if current.h == 0:
            print("Goal found!")
            return reconstruct_path(current)

        # Mark current as expanded
        closed_set.add(current_key)

        # Expand neighbors
        for move in movelist:
            # create child cube and key
            new_cube = copy.deepcopy(current.cube)
            applyMovement(new_cube, move, get_path_from_movement(new_cube, move))
            child_key = new_cube
            tentative_g = current.g + 1
            '''
            # If child already expanded, skip it
            if child_key in closed_set:
                continue
            '''
            # If we have a better or equal g already recorded, skip
            if child_key in g_scores and tentative_g >= g_scores[child_key]:
                # Not a better path
                continue

            # Otherwise it's a better path: create neighbor node
            child_h = heuristic(new_cube)
            neighbor = Node(new_cube, g=tentative_g, h=child_h, parent=current)
            '''
            # If goal:
            if neighbor.h == 0:
                print("Goal found!\n")
                return reconstruct_path(neighbor), len(open_heap)
            '''
            # Record best g so far
            g_scores[child_key] = tentative_g

            # push to heap with tie-breaker counter
            heapq.heappush(open_heap, neighbor)
            counter += 1

            movecounter += 1
            print("Heuristic:", neighbor.h, "Depth:", neighbor.g, "Node #:", movecounter)

    print("No path found!")
    return None

# Returns the path from start to goal by tracing parent nodes
def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node.cube)
        node = node.parent
    return path[::-1]  # reverse to get start -> goal