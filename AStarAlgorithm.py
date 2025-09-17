'''
    Desc: Implementation of A* Search Algorithm, to be imported to SudokuMain.py, where it will be used to calculate the optimal path
          for solving Sudoku Cube Puzzles.
    Last Changed: 9/15/2025
'''

# This is where our Heuristic for how close the cube is to be solved will go
def heuristic(cube: Cube):
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

def randomizer(movelist, movevalue, previous_var):
    print("Applying random move")
    for i in range(0, previous_var):
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
