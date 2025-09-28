'''
    Purpose: The program takes a given solved Sudoku Rubik's Cube and applies random moves to it while calculating the heuristic
                 of how far the cube is from being solved. The user can choose to apply more random moves as they see fit
                 until they decide to stop.
    Last Updated: 9/21/2025
'''

# Initializes our objects that are needed for the functions to run properly
def initializefunction():
    
    cube1 = Cube(cubecounter = 0, cubename = "Pacman") # creates the first cube object "Pacman"

    FC00 = Movement(cube1, face="Front", colrow="C", position=0, direction=0, name="FC00") # creates all 12 movements for Pacman
    # Attributes includes name of face, if its a column or row, position of the column/row, direction of the movement, and a shorthand codename
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


    cube2 = copy.deepcopy(cube1) # creates deep copies of Pacman, each with different cubes counters and 
    # names (Blinky, Pinky, Inky, Clyde)
    cube2.cubecounter = 1
    cube2.cubename = "Blinky"

    cube3 = copy.deepcopy(cube1)
    cube3.cubecounter = 2
    cube3.cubename = "Pinky"


    cube4 = copy.deepcopy(cube1)
    cube4.cubecounter = 3
    cube4.cubename = "Inky"


    cube5 = copy.deepcopy(cube1)
    cube5.cubecounter = 4
    cube5.cubename = "Clyde"

    movelist = [FC00, FC01, FC10, FC11, # Throws all of the moves into an array to return
                FR00, FR01, FR10, FR11,
                LC00, LC01, LC10, LC11]

    cubeArray = [cube1, cube2, cube3, cube4, cube5] # Throws all of the cubes into an array to return

    return movelist, cubeArray # returns the array of moves and cubes to be used in other functions

# import funtions and Class definitions from other files,
# imports random, numpy, math, copy, and time libraries for various functions
from AStarAlgorithm import *
from ClassDef import *
import random
import numpy as np
import math
import copy
import time

movelist,cubeArray = initializefunction() # calls the initialize function to create the cubes and moves
newmove = 1 # variable to control while loop for user input
previous_var = 12 # variable to store the previous move applied to avoid repeating the same move (12 initially as thers no 12th move (only 0-11))
repeatrandomization = 0 # variable to check if user has applied random moves yet


while newmove == 1: # while loop to keep asking user if they want to apply more random moves
    if repeatrandomization == 0:
        user_input = input("Would you like to complete a move? Y/N:\n")
    else:
        user_input = input("Would you like to randomize even more? Y/N:\n")
    match user_input:
        case "Y" | "y":
            repeatrandomization = 1
            while True:
                try:
                    nummoves = int(input("How many moves would you like to apply (3-20 recommended):\n"))
                    if 1 <= nummoves <= 20: # checks if user input is between 3 and 20
                        for item in cubeArray:
                            previous_var = randomizer(movelist, nummoves, previous_var, item) # calls the randomizer function to apply random moves to each cube
                            print("\n\n\n\n\n")
                            
                        break
                    else:
                        print("Please enter a number between 3 and 20.")
                except ValueError: # catches error if user input is not a number
                    print("Invalid input, please enter a number.")
        case "N" | "n":
            newmove = 0
        case _:
            print("Invalid input, please re-enter.")
elapsed_time = np.zeros(len(cubeArray)) # array to store the elapsed time for each cube
goal_path = np.empty(len(cubeArray), dtype=Cube) # array to store the goal path for each cube
length_of_queue = np.zeros(len(cubeArray)) # array to store the length of the priority queue for each cube (for graph creation)

if repeatrandomization == 1:
    for item in cubeArray:

        start_time = time.perf_counter() # starts the timer for each cube
        goal_path[item.cubecounter],length_of_queue[item.cubecounter] = a_star_search(item, movelist, nummoves) # calls the A* search function to solve the cube and returns the goal path and length of the priority queue

        end_time = time.perf_counter() # ends the timer for each cube

        
        elapsed_time[item.cubecounter] = end_time - start_time 
    for item in cubeArray: # prints the results for each cube
        print("Number of nodes in the queue: %d" % length_of_queue[item.cubecounter])
        print("Time to solve cube %s was: %.4f seconds. Number of moves applied: %d" % (item.cubename, elapsed_time[item.cubecounter], (len(goal_path[item.cubecounter]) - 1)))
        for cube in goal_path[item.cubecounter]:
            printCube(cube)
    index = 0
    for nodenum in length_of_queue: # prints the number of nodes in the priority queue for each cube
        print("Cube %s has %d nodes in the priority queue" % (cubeArray[index].cubename, nodenum))
        index += 1
    averagenodes = np.mean(length_of_queue)
    print("The average number of nodes in the priorty queue is: %.2f" % averagenodes)
else:
    print("No moves were applied, exiting program.") # case if no moves were applied