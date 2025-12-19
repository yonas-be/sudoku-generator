import random

#-----------------------------
# Global variables
#-----------------------------
SOLUTIONS = 0


# Main function to generate a puzzle
def generate(difficulty: str | None):
    grid = []
    for i in range(9):
        row = [0] * 9
        grid.append(row)
    fill_grid(grid)

    number_count = 0
    if difficulty is None:
        difficulty = "easy"

    if difficulty.lower() == "easy":
        number_count = 35
    elif difficulty.lower() == "medium":
        number_count = 45
    elif difficulty.lower() == "hard":
        number_count = 55
    elif difficulty.lower() == "hardcore":
        number_count = 60

    remove_numbers(grid, number_count)

    return grid

# Recursively fills a sudoku grid
def fill_grid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                #empty Cell found

                numbers = list(range(1, 10))
                random.shuffle(numbers)

                for number in numbers:
                    if check_rules(grid, row, col, number):
                        # place number
                        grid[row][col] = number

                        if fill_grid(grid):
                            return True
                        #delete last number
                        grid[row][col] = 0
                return False
    return True

# Helper function to check if a number is valid or not
def check_rules(grid, r, c, num):
    box_start_r = (r // 3) * 3
    box_start_c = (c // 3) * 3

    # Check rows / cols / box
    for i in range(9):
        if (grid[r][i] == num) or (grid[i][c] == num):
            return False
        if grid[box_start_r + i // 3][box_start_c + i % 3] == num:
            return False
    # Passed all checks
    return True

# Recursively solves the grid
def solve(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                #found empty cell
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for number in numbers:
                    if check_rules(puzzle, i, j, number):
                        #number is valid
                        puzzle[i][j] = number

                        if solve(puzzle):
                            return True

                        #number isn't valid, reset
                        puzzle[i][j] = 0
                return False
    return True

# Writes the amount of solutions to the global variable "SOLUTIONS". Stops at SOLUTIONS > 1
def check_uniqueness(grid, empty_cells: list | None = None):
    global SOLUTIONS

    if empty_cells is None:
        empty_cells =  []
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    empty_cells.append((i, j))

    if SOLUTIONS > 1:
        return True

    if len(empty_cells) == 0:
        SOLUTIONS += 1

        if SOLUTIONS > 1:
            return True
        return False

    #MRV, search cell with the fewest possibilities
    best_cell = None
    best_possibilities = 0
    min_possibilities = 9

    for row, col in empty_cells:

        possibilities = []

        for num in range(1, 10):
            if check_rules(grid, row, col, num):
                possibilities.append(num)

        if len(possibilities) < min_possibilities:
            min_possibilities = len(possibilities)
            best_possibilities = possibilities
            best_cell = (row, col)

        if min_possibilities == 1:
            break

    numbers = best_possibilities[:]

    row, col = best_cell
    for num in numbers:
        if check_rules(grid, row, col, num):
            grid[row][col] = num
            empty_cells.remove(best_cell)
            if check_uniqueness(grid, empty_cells):
                grid[row][col] = 0
                return True
            empty_cells.append(best_cell)
            grid[row][col] = 0  # backtrack

    return False

# Recursively removes the desired amount of numbers. Can take alot of time.
def remove_numbers(grid, number_count, filled_cells=None):
    global SOLUTIONS

    if number_count >= 64:
        return False

    # Base case: if no more numbers need to be removed
    if number_count == 0:
        return True

    if filled_cells is None:
        filled_cells = [(r, c) for r in range(9) for c in range(9) if grid[r][c] != 0]
        random.shuffle(filled_cells)

    for cell in filled_cells:
        r, c = cell
        number_backup = grid[r][c]
        grid[r][c] = 0

        # Still unique?
        SOLUTIONS = 0
        check_uniqueness(grid)

        if SOLUTIONS == 1:
            # Valid --> recurse
            filled_cells.remove(cell)
            if remove_numbers(grid, number_count - 1, filled_cells):
                return True

        # Load backup value
        grid[r][c] = number_backup
        filled_cells.append(cell)

    return False

# Quickly print the Sudoku in the console
def print_puzzle(p):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("------+-------+------")

        row_str = ""
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row_str += "| "

            if p[r][c] == 0:
                row_str += "."
            else:
                row_str += str(p[r][c])

            row_str += " "
        print(row_str)
