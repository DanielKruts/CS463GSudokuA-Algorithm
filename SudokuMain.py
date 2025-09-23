'''
    Purpose: The program takes a given solved Sudoku Rubik's Cube and applies random moves to it while calculating the heuristic
                 of how far the cube is from being solved. The user can choose to apply more random moves as they see fit
                 until they decide to stop.
    Last Updated: 9/21/2025
'''

# Initializes our objects that are needed for the functions to run properly
def initializefunction():
    
    cube1 = Cube(cubecounter = 1, cubename = "Pacman")

    FC00 = Movement(cube1, face="Front", colrow="C", position=0, direction=0, name="FC00")
    FC01 = Movement(cube1, face="Front", colrow="C", position=0, direction=1, name="FC01")
    FC10 = Movement(cube1, face="Front", colrow="C", position=2, direction=0, name="FC10")
    FC11 = Movement(cube1, face="Front", colrow="C", position=2, direction=1, name="FC11")

    FR00 = Movement(cube1, face="Front", colrow="R", position=0, direction=0, name="FR00")
    FR01 = Movement(cube1, face="Front", colrow="R", position=0, direction=1, name="FR01")
    FR10 = Movement(cube1, face="Front", colrow="R", position=2, direction=0, name="FR10")
    FR11 = Movement(cube1, face="Front", colrow="R", position=2, direction=1, name="FR11")

    LC00 = Movement(cube1, face="Left", colrow="C", position=0, direction=0, name="LC00")
    LC01 = Movement(cube1, face="Left", colrow="C", position=0, direction=1, name="LC01")
    LC10 = Movement(cube1, face="Left", colrow="C", position=2, direction=0, name="LC10")
    LC11 = Movement(cube1, face="Left", colrow="C", position=2, direction=1, name="LC11")


    cube2 = copy.deepcopy(cube1)
    cube2.cubecounter = 2
    cube2.cubename = "Blinky"

    cube3 = copy.deepcopy(cube1)
    cube3.cubecounter = 3
    cube3.cubename = "Pinky"


    cube4 = copy.deepcopy(cube1)
    cube4.cubecounter = 4
    cube4.cubename = "Inky"


    cube5 = copy.deepcopy(cube1)
    cube5.cubecounter = 5
    cube5.cubename = "Clide"

    # For the goal cube so we have an already solved cube object to compare to
    goalCube = Cube(cubecounter = 0, cubename="GoalCube")

    movelist = [FC00, FC01, FC10, FC11,
                FR00, FR01, FR10, FR11,
                LC00, LC01, LC10, LC11]

    cubeArray = [cube1, cube2, cube3, cube4, cube5]

    return movelist, cubeArray, goalCube

from AStarAlgorithm import *
from ClassDef import *
import random
import numpy as np
import math
import copy


movelist,cubeArray,goalCube = initializefunction()
newmove = 1
previous_var = -1

while newmove == 1:
    user_input = input("Would you like to complete a move? Y/N:\n")
    match user_input:
        case "Y" | "y":
            while True:
                try:
                    nummoves = int(input("How many moves would you like to apply (3-20 recommended):\n"))
                    if 1 <= nummoves <= 20:
                        for item in cubeArray:
                            print("WERE PRINTING THE FUCKING CUBE FUCKHEADS. NEW CUBE!!!")
                            print("Cube is: " + item.cubename)
                            printCube(item)
                            previous_var = randomizer(movelist, nummoves, previous_var, item)
                            heuristic(item)
                            a_star_search(item, goalCube, movelist)
                            print("\n\n\n\n\n")
                        break
                    else:
                        print("Please enter a number between 3 and 20.")
                except ValueError:
                    print("Invalid input, please enter a number.")
        case "N" | "n":
            print("Exiting movements.")
            newmove = 0
        case _:
            print("Invalid input, please re-enter.")
