from generator.mace4_interface import run_mace4
from backend.sudoku_logic import get_sudoku_from_mace4, extract_and_save_sudoku_grid
def main():
    get_sudoku_from_mace4()
    extract_and_save_sudoku_grid()

if __name__ == "__main__":
    main()