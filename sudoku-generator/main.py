from flask import Flask, render_template, jsonify, request
import json
from backend.sudoku_logic import load_sudoku_from_json, delete_random_cells

# Initialize the Flask app
app = Flask(__name__)

# Difficulty levels (number of cells to remove)
DIFFICULTY_LEVELS = {
    'easy': 30,
    'medium': 40,
    'hard': 50
}

def generate_sudoku_puzzle(difficulty='hard'):
    """
    Generate a Sudoku puzzle based on the specified difficulty.
    """
    # Load the complete Sudoku grid
    grid = load_sudoku_from_json('examples/example_sudoku.json')
    
    # Determine the number of cells to remove based on the difficulty level
    num_cells_to_remove = DIFFICULTY_LEVELS.get(difficulty, 30)
    
    # Remove random cells from the grid
    modified_grid = delete_random_cells(grid, num_cells_to_remove)
    
    return modified_grid

# Load the solution grid from example_sudoku.json
def load_solution():
    with open("examples/example_sudoku.json") as f:
        return json.load(f)["grid"]

# Load the modified Sudoku grid (with some cells erased)
def load_modified():
    with open("examples/modified_sudoku.json") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    solution = load_solution()  # Check if this returns a valid grid
    modified_grid = load_modified()  # Ensure this is correctly loaded
    
    if not solution or not modified_grid:
        return "Error loading Sudoku data", 500  # Handle error if data is missing

    return render_template('index.html', grid=modified_grid, solution=solution)



@app.route('/submit', methods=['POST'])
def submit():
    """
    Handle the submitted solution from the frontend.
    """
    # Get the user-submitted grid (from frontend)
    user_grid = request.json.get('grid')
    
    # Here you can add logic to validate the user's solution if needed
    
    return jsonify({'message': 'Solution received', 'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
