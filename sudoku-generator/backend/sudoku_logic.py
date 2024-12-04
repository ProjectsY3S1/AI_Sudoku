import random
import json

def load_sudoku_from_json(file_path):
    """
    Loads a Sudoku grid from a JSON file and returns it as a 2D list.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the grid from the loaded data
    sudoku_grid = data.get("grid")
    
    # Ensure the grid is a 9x9 structure (for Sudoku)
    if not sudoku_grid or len(sudoku_grid) != 9 or any(len(row) != 9 for row in sudoku_grid):
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
