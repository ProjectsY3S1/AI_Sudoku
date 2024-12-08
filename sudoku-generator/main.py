from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
from backend.sudoku_logic import get_sudoku_from_mace4, extract_and_save_sudoku_grid, generate_sudoku_puzzle

# Initialize the Flask app
app = Flask(__name__)

# Load the solution grid from example_sudoku.json
def load_solution():
    with open("/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/sudoku_boards/full_board.json") as f:
        return json.load(f)

# Load the modified Sudoku grid (with some cells erased)
def load_modified():
    with open("/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/sudoku_boards/modified_board.json") as f:
        return json.load(f)

# Welcome page
@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        # Get the selected difficulty from the form
        difficulty = request.form.get("difficulty")
        if not difficulty:
            return "Error: No difficulty selected", 400
        
        # Generate a Sudoku puzzle with the selected difficulty
        get_sudoku_from_mace4()
        extract_and_save_sudoku_grid()
        generate_sudoku_puzzle(difficulty=difficulty)
        
        # Redirect to the game page
        return redirect(url_for("game"))
    
    return render_template("welcome.html")

# Game page
@app.route("/game", methods=["GET"])
def game():
    # Load the solution and modified grid
    solution = load_solution()
    modified_grid = load_modified()
    
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
