""""
################## Sudoku Solver ##################
    @author : Harry Dalal

    Note: Simply run the file for testing and 
            use the commented code at the bottom to solve your own sudoku puzzle.
"""
import copy

"""Sudoku grid and it's solution for example"""
sudoku_grid = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
               [6, 8, 0, 0, 7, 0, 0, 9, 0],
               [1, 9, 0, 0, 0, 4, 5, 0, 0],
               [8, 2, 0, 1, 0, 0, 0, 4, 0],
               [0, 0, 4, 6, 0, 2, 9, 0, 0],
               [0, 5, 0, 0, 0, 3, 0, 2, 8],
               [0, 0, 9, 3, 0, 0, 0, 7, 4],
               [0, 4, 0, 0, 5, 0, 0, 3, 6],
               [7, 0, 3, 0, 1, 8, 0, 0, 0]]

# sudoku_grid = [[0, 0, 0, 2, 6, 0, 7, 0, 1], [6, 8, 0, 0, 7, 0, 0, 9, 0], [1, 9, 0, 0, 0, 4, 5, 0, 0], [8, 2, 0, 1, 0, 0, 0, 4, 0], [0, 0, 4, 6, 0, 2, 9, 0, 0], [0, 5, 0, 0, 0, 3, 0, 2, 8], [0, 0, 9, 3, 0, 0, 0, 7, 4], [0, 4, 0, 0, 5, 0, 0, 3, 6], [7, 0, 3, 0, 1, 8, 0, 0, 0]]

sudoku_grid_solution = [[4, 3, 5, 2, 6, 9, 7, 8, 1],
                        [6, 8, 2, 5, 7, 1, 4, 9, 3],
                        [1, 9, 7, 8, 3, 4, 5, 6, 2],
                        [8, 2, 6, 1, 9, 5, 3, 4, 7],
                        [3, 7, 4, 6, 8, 2, 9, 1, 5],
                        [9, 5, 1, 7, 4, 3, 6, 2, 8],
                        [5, 1, 9, 3, 2, 6, 8, 7, 4],
                        [2, 4, 8, 9, 5, 7, 1, 3, 6],
                        [7, 6, 3, 4, 1, 8, 2, 5, 9]]


def solve(sudoku):
    """Main function to solve given Sudoku."""
    if sudoku_is_complete(sudoku):
        return sudoku
    else:
        # Create 3 lists which will have respective details of same item at same indices.
        possibilities_list = []  # list with all possibilities at the position
        possibilities_length = []  # list with number of total possibilities at the position
        possibilities_position = []  # list with coordinates of the position
        for row in range(9):
            for col in range(9):
                if sudoku_grid[row][col] == 0:
                    lst = find_possibilities(sudoku, row, col)
                    possibilities_list.append(lst)
                    possibilities_length.append(len(lst))
                    possibilities_position.append([row, col])
        # Fill all the valuse that are only possibilities (sure values) and then recurse to the function agian.
        if 1 in possibilities_length:
            for i in range(len(possibilities_list)):
                if possibilities_length[i] == 1:
                    add(sudoku, possibilities_position[i][0], possibilities_position[i][1], possibilities_list[i][0])
            solve(sudoku)
        # Try filling in one value at places where there are 2 possibilities.
        #     If it works, well and good. Otherwise, we try the other possibility.
        elif 2 in possibilities_length:
            for i in range(len(possibilities_list)):
                if possibilities_length[i] == 2:
                    add(sudoku, possibilities_position[i][0], possibilities_position[i][1], possibilities_list[i][0])
                    solve(sudoku)
                    add(sudoku, possibilities_position[i][0], possibilities_position[i][1], possibilities_list[i][1])
                    solve(sudoku)
        # If we still have more than 2 possibilities, we simply try putting the random number and back tracking if it does not work.
        else:
            for row in range(9):
                for col in range(9):
                    if sudoku_grid[row][col] == 0:
                        for number in range(1, 10):
                            if number_is_valid(sudoku, number, row, col):
                                add(sudoku, row, col, number)
                                solve(sudoku)
                                remove(sudoku, row, col)
        # Finally check the solved Sudoku's and return it if its true.
        if check(sudoku):
            return sudoku


def sudoku_is_complete(sudoku):
    """Checks if the given Sudoku is completely filled."""
    for row in range(9):
        for col in range(9):
            if sudoku_grid[row][col] == 0:
                return False
    return True


def number_is_valid(sudoku, number, row, col):
    """Checks if the given number can be filled at the given position."""
    for i in range(9):
        if sudoku[row][i] == number or sudoku[i][col] == number:
            return False
    block_row = row // 3
    block_col = col // 3
    for i in range(3):
        for j in range(3):
            if sudoku[block_row * 3 + i][block_col * 3 + j] == number:
                return False
    return True


def add(sudoku, row, col, number):
    """Adds given number at given position."""
    sudoku[row][col] = number


def remove(sudoku, row, col):
    """Removes given number at given position."""
    sudoku[row][col] = 0


def find_possibilities(sudoku, row, col):
    """Returns a list of all possibile values for the give position."""
    possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """Check for row and column values."""
    for i in range(9):
        if sudoku[row][i] in possibilities:
            possibilities.remove(sudoku[row][i])
    for i in range(9):
        if sudoku[i][col] in possibilities:
            possibilities.remove(sudoku[i][col])
    """Check for box values."""
    block_row = row // 3
    block_col = col // 3
    for i in range(3):
        for j in range(3):
            if sudoku[block_row * 3 + i][block_col * 3 + j] in possibilities:
                possibilities.remove(sudoku[block_row * 3 + i][block_col * 3 + j])
    """Return remaining possibilities."""
    return possibilities


def check(sudoku):
    """Checks the solved Sudoku's for correctness."""
    for row in range(9):
        for col in range(9):
            """Check for 0's."""
            if sudoku_grid[row][col] == 0:
                return False
            temp = sudoku[row][col]
            """Check for row and column values."""
            for i in range(9):
                if i == col:
                    continue
                elif sudoku[row][i] == temp:
                    return False
            for i in range(9):
                if i == row:
                    continue
                elif sudoku[i][col] == temp:
                    return False
            """Check for box values."""
            block_row = row // 3
            block_col = col // 3
            for i in range(3):
                for j in range(3):
                    if block_row * 3 + i == row and block_col * 3 + j == col:
                        continue
                    elif sudoku[block_row * 3 + i][block_col * 3 + j] == temp:
                        return False
    return True


def print_sudoku(sudoku):
    """Prints Sudoku in square design."""
    for row in range(9):
        if row in [3, 6]:
                print("+ - - - + - - - + - - - +")
        for col in range(9):
            if row == 0 and col == 0:
                print("+ - - - + - - - + - - - +")
            if col == 0:
                print("|", end=" ")
            print(sudoku[row][col], end=" ")
            if col in [2, 5, 8]:
                print("|", end=" ")
        print()
    print("+ - - - + - - - + - - - +")

sudoku_grid_copy = copy.deepcopy(sudoku_grid)
solved_sudoku = solve(sudoku_grid)
print()
if solved_sudoku == sudoku_grid_solution:
    print("**********PASSED**********")
else:
    print("**********FAILED**********")
print()
print("QUESTION GRID:")
print_sudoku(sudoku_grid_copy)
print()
print("SOLVED GRID:")
print_sudoku(solved_sudoku)

"""Code if you want to input your own Sudoku puzzle."""
# sudoku_grid = input("Give sudoku to solve: ")
# sudoku_grid_copy = copy.deepcopy(sudoku_grid)
# solved_sudoku = solve(sudoku_grid)

# print()
# print("QUESTION GRID:")
# print_sudoku(sudoku_grid_copy)

# print()
# print("SOLVED GRID:")
# print_sudoku(solved_sudoku)
