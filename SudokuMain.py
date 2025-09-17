'''
    Purpose: The program takes a given solved Sudoku Rubik's Cube and applies random moves to it while calculating the heuristic
                 of how far the cube is from being solved. The user can choose to apply more random moves as they see fit
                 until they decide to stop.
    Last Updated: 9/12/2025
'''
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

# Initializes our objects that are needed for the functions to run properly
def initializefunction():
    cubeObject = Cube()

    FC00 = Movement(cubeObject, face="Front", colrow="C", position=0, direction=0, name="FC00")
    FC01 = Movement(cubeObject, face="Front", colrow="C", position=0, direction=1, name="FC01")
    FC10 = Movement(cubeObject, face="Front", colrow="C", position=2, direction=0, name="FC10")
    FC11 = Movement(cubeObject, face="Front", colrow="C", position=2, direction=1, name="FC11")

    FR00 = Movement(cubeObject, face="Front", colrow="R", position=0, direction=0, name="FR00")
    FR01 = Movement(cubeObject, face="Front", colrow="R", position=0, direction=1, name="FR01")
    FR10 = Movement(cubeObject, face="Front", colrow="R", position=2, direction=0, name="FR10")
    FR11 = Movement(cubeObject, face="Front", colrow="R", position=2, direction=1, name="FR11")

    LC00 = Movement(cubeObject, face="Left", colrow="C", position=0, direction=0, name="LC00")
    LC01 = Movement(cubeObject, face="Left", colrow="C", position=0, direction=1, name="LC01")
    LC10 = Movement(cubeObject, face="Left", colrow="C", position=2, direction=0, name="LC10")
    LC11 = Movement(cubeObject, face="Left", colrow="C", position=2, direction=1, name="LC11")

    printCube(cubeObject)

    movelist = [FC00, FC01, FC10, FC11,
                FR00, FR01, FR10, FR11,
                LC00, LC01, LC10, LC11]

    return movelist, cubeObject

# Determines whether to apply a column or row moved based on the Movement object passed to it
def applyMovement(movement, path):
    cube = movement.cube

    if movement.colRow == "C":  # column move
        applyColumnMove(cube, movement, path)
    elif movement.colRow == "R":  # row move
        applyRowMove(cube, movement, path)
    else:
        print("Invalid Movement type")
        exit()

# Takes a given Cube, Movement, and path to rotate the appropriate face and apply the correct column move
def applyColumnMove(cube, movement, path):
    print("Movement Code:", movement.name, "| face:", movement.face, "| col/row:", movement.colRow, "| position:", movement.position, "| direction:", movement.direction)
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
    print("Movement Code:", movement.name, "| face:", movement.face, "| col/row:", movement.colRow, "| position:", movement.position, "| direction:", movement.direction)
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
def get_path_from_movement(movement):
    """
    Returns the faces and strip orientation for a move.
    face: "Front", "Left", etc.
    colRow: "C" for column, "R" for row
    position: 0 (left/top) or 2 (right/bottom)
    Returns: path_faces [4 CubeSides], path_orientations ["row2", "col0", ...]
    """
    cube = movement.cube
    face = movement.face
    colRow = movement.colRow
    position = movement.position
    direction = movement.direction
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
                    path[0].facevalue[0][:] = path[3].facevalue[0][:]
                    path[3].facevalue[0][:] = path[2].facevalue[0][:]
                    path[2].facevalue[0][:] = path[1].facevalue[0][:]
                    path[1].facevalue[0][:] = temp
                elif movement.direction == 1: # Counterclockwise
                    path[0].facevalue[0][:] = path[3].facevalue[0][:]
                    path[3].facevalue[0][:] = path[2].facevalue[0][:]
                    path[2].facevalue[0][:] = path[1].facevalue[0][:]
                    path[1].facevalue[0][:] = temp
            elif movement.position == 2: # Bottom row
                temp = path[0].facevalue[2][:]
                if movement.direction == 0: # Counterclockwise
                    path[0].facevalue[2][:] = path[3].facevalue[2][:]
                    path[3].facevalue[2][:] = path[2].facevalue[2][:]
                    path[2].facevalue[2][:] = path[1].facevalue[2][:]
                    path[1].facevalue[2][:] = temp
                elif movement.direction == 1: # Clockwise
                    path[0].facevalue[2][:] = path[1].facevalue[2][:]
                    path[1].facevalue[2][:] = path[2].facevalue[2][:]
                    path[2].facevalue[2][:] = path[3].facevalue[2][:]
                    path[3].facevalue[2][:] = temp
        elif movement.colRow == "C": # Column move
            if movement.position == 0: # Left column
                temp = [row[0] for row in path[0].facevalue]
                if movement.direction == 0: # Down
                    for i in range(3):
                        path[0].facevalue[i][0] = path[1].facevalue[i][0]
                    for i in range(3):
                        path[1].facevalue[i][0] = path[2].facevalue[2-i][2]
                    for i in range(3):
                        path[2].facevalue[i][2] = path[3].facevalue[2-i][0]
                    for i in range(3):
                        path[3].facevalue[i][0] = temp[i]
                elif movement.direction == 1: #Up
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
            if movement.direction == 0: # Down
                for i in range(3):
                    path[0].facevalue[2-i][0] = path[1].facevalue[0][i]
                for i in range(3):
                    path[1].facevalue[0][i] = path[2].facevalue[i][2]
                for i in range(3):
                    path[2].facevalue[i][2] = path[3].facevalue[2][2-i]
                for i in range(3):
                    path[3].facevalue[2][i] = temp[i]
            elif movement.direction == 1: # Up
                for i in range(3):
                    path[0].facevalue[i][0] = path[3].facevalue[2][i]
                for i in range(3):
                    path[3].facevalue[2][2-i] = path[2].facevalue[i][2]
                for i in range(3):
                    path[2].facevalue[i][2] = path[1].facevalue[0][2-i]
                for i in range(3):
                    path[1].facevalue[0][i] = temp[i]
        elif movement.position == 2: #Right column
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
                    path[1].facevalue[0][i] = temp[2-i]
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
    print("Applying random move")
    print("Move value is", movevalue)
    for i in range(0, movevalue):
        print("Test")
        random_var = random.randint(0, 11)
        while random_var == previous_var:
            print("Same move as last time, rerolling")
            random_var = random.randint(0, 11)
        movechosen = movelist[random_var]
        pathprint = get_path_from_movement(movechosen)
        #print("Path is", [side.centercolor for side in pathprint[0]], "with orientations", pathprint[1])
        applyMovement(movechosen, pathprint)

        printCube(cubeObject)
        heuristic(cubeObject)
        previous_var = random_var
    return previous_var

import random
import numpy as np
import math
import AStarAlgorithm
import CubeClass 
from CubeClass import Cube, Movement, CubeSide

movelist,cubeObject = initializefunction()
heuristic(cubeObject)

newmove = 1
previous_var = -1

while(newmove == 1):
    user_input = input("Would you like to complete a move? Y/N:\n")

    match user_input:
        case "Y" | "y":
            while True:
                try:
                    nummoves = int(input("How many moves woud you like to apply (3-20 recommended):\n"))
                    if 3 <= nummoves <= 20:
                        break
                    else:
                        print("Please enter a number between 3 and 20.")
                except ValueError:
                    print("Invalid input, please enter a number.")
            previous_var = randomizer(movelist, nummoves, previous_var, cubeObject)
        case "N" | "n":
            print("Exiting movements.")
            newmove = 0
        case _:
            print("Invalid input, please re-enter.")