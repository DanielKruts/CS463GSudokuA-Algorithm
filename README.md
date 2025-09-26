# CS463GSudokuA-Algorithm

Python implementation of the A* Algorithm on a Sudoku Cube

Note: This project requires an installation of Python to run the script, as well as installing the numpy library.
Installing Python and the numpy library:

	1. Install Python from https://www.python.org/downloads/ if you haven't already(Ensure that Python is added to your path on installation)
		(Python 3.11 was used for testing and 3.13 had previously caused errors)
	2. Open your terminal/command prompt
	3. Install numpy using pip with the command 'pip install numpy'
	4. Verify the installation by running 'python -c "import numpy; print(numpy.__version__)"' in your terminal/command prompt
	5. If the version number prints without errors, numpy is successfully installed
	6. If you encounter issues, refer to the numpy installation guide at https://numpy.org/install/ for troubleshooting

How to Run: 

	1. Open your terminal/command prompt, or your preferred IDE
	2. Navigate to the directory where SudokuMain.py, ClassDef.py, and AStarAlgorithm.py is located, or open the file in your IDE
	3. Run the script using the command 'python SudokuMain.py' in the terminal/command prompt, or run the file in your IDE
	4. Follow the prompts on the screen to randomly generate the moves on a completed Sudoku Cube (range is 3-20).
	5. After generating the moves, you will be prompted to choose if you want even more moves applied to the cube (y/n).
	6. After confirming the moves, the A* algorithm will attempt to solve the cube and print the solution steps to the console.
	7. This will print out the solutions to all five cubes.
	8. If you wish to run the program again (under a different number of moves), simply rerun the script and follow the prompts.
