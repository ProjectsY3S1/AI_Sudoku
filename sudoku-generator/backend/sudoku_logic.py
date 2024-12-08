import random
import json
from generator.mace4_interface import run_mace4
import re
import random

# Difficulty levels (number of cells to remove)
DIFFICULTY_LEVELS = {
    'easy': 30,
    'medium': 40,
    'hard': 50
}
def get_sudoku_from_mace4():
    input_file = "/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/constraints/sudoku_rules.in"
    output_file = "/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/mace4-results/result.txt"

    # Call the previously defined run_mace4 function
    edit_constraint_file(input_file)
    return_code = run_mace4(input_file, output_file)
    
    if return_code == 0:
        print(f"mace4 ran successfully. Output saved to: {output_file}")
    else:
        print("mace4 encountered an error.")

def edit_constraint_file(file_path):
    """
    Edits row 48 of the given constraint file, replacing every number with a random number between 0 and 8.
    
    Args:
        file_path (str): The path to the constraint file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Generate a new random line
    random_numbers = [random.randint(0, 8) for _ in range(2)]
    new_line = f"   f({random_numbers[0]},{random_numbers[1]}) = {random.randint(0, 8)}.\n"

    # Replace row 48 with the new random line
    if len(lines) >= 48:  # Ensure there are at least 48 lines
        lines[47] = new_line  # Row 48 corresponds to index 47
    else:
        raise IndexError("The file does not have enough lines to edit row 48.")

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"Successfully updated row 48 with: {new_line.strip()}")

def extract_and_save_sudoku_grid():
    """
    Extracts the Sudoku grid from the Mace4 output file, replaces '0' with '9',
    and saves it as a 2D array in a JSON file.
    """
    output_file = "/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/mace4-results/result.txt"
    with open(output_file, 'r') as file:
        content = file.read()

    # Extract the function(f(_, _), [...]) part using regex
    match = re.search(r'function\(f\(_,_\), \[(.*?)\]\)', content, re.DOTALL)
    if match:
        # Extract the numbers and convert them to a list of integers
        numbers = list(map(int, match.group(1).split(',')))
        
        # Transform the 1D list into a 2D list (9x9 Sudoku grid)
        sudoku_grid = [numbers[i:i + 9] for i in range(0, len(numbers), 9)]
        
        # Replace all '0' values with '9'
        for row in range(len(sudoku_grid)):
            for col in range(len(sudoku_grid[row])):
                if sudoku_grid[row][col] == 0:
                    sudoku_grid[row][col] = 9
        
        # Save the modified Sudoku grid to a JSON file
        save_sudoku_to_json(sudoku_grid, "/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/sudoku_boards/full_board.json")
        
        print("Success: Sudoku grid extracted, modified, and saved successfully.")
        return
    else:
        print("Error: Sudoku grid not found in the output.")
        return

def generate_sudoku_puzzle(difficulty='hard'):
    """
    Generate a Sudoku puzzle based on the specified difficulty.
    """
    # Load the complete Sudoku grid
    grid = load_sudoku_from_json('/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/sudoku_boards/full_board.json')
    
    # Determine the number of cells to remove based on the difficulty level
    num_cells_to_remove = DIFFICULTY_LEVELS.get(difficulty, 30)
    
    # Remove random cells from the grid
    modified_grid = delete_random_cells(grid, num_cells_to_remove)
    
    save_sudoku_to_json(modified_grid, "/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/sudoku_boards/modified_board.json")
        
    return

def load_sudoku_from_json(file_path):
    """
    Loads a Sudoku grid from a JSON file and returns it as a 2D list.
    """
    with open(file_path, 'r') as file:
        sudoku_grid = json.load(file)
    
    # Ensure the grid is a 9x9 structure (for Sudoku)
    if len(sudoku_grid) != 9 or any(len(row) != 9 for row in sudoku_grid):
        raise ValueError("Invalid Sudoku grid. Must be a 9x9 grid.")
    
    return sudoku_grid



def delete_random_cells(grid, num_cells_to_remove):
    """
    Randomly removes `num_cells_to_remove` cells from the given Sudoku grid.
    The cells will be set to 0 (empty).
    """
    # Validate input
    if num_cells_to_remove < 1 or num_cells_to_remove > 81:
        raise ValueError("Number of cells to remove must be between 1 and 81.")
    
    # Get all possible cell positions (0-indexed)
    positions = [(row, col) for row in range(9) for col in range(9)]
    
    # Randomly select positions to remove
    random.shuffle(positions)  # Shuffle positions to get random cells
    cells_to_remove = positions[:num_cells_to_remove]
    
    # Remove cells by setting them to 0 (empty)
    for row, col in cells_to_remove:
        grid[row][col] = 0
    
    return grid


def save_sudoku_to_json(grid, file_path):
    """
    Saves the modified Sudoku grid back to a JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(grid, file)


# Example usage:
if __name__ == "__main__":
    # Load a complete Sudoku grid from JSON
    grid = load_sudoku_from_json('examples/example_sudoku.json')
    
    # Specify the number of cells to remove (e.g., difficulty level)
    num_cells_to_remove = 30
    
    # Delete random cells from the grid
    modified_grid = delete_random_cells(grid, num_cells_to_remove)
    
    # Save the modified grid back to a new JSON file
    save_sudoku_to_json(modified_grid, 'examples/modified_sudoku.json')
