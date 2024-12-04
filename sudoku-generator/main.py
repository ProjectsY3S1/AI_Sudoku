from generator.mace4_interface import run_mace4

def main():
    output = run_mace4("/mnt/c/Personal stuff/Year 3 Sem 1/AI/proj2_sudoku/sudoku-generator/constraints/sudoku_rules.in")
    print("Generated Sudoku Puzzle:")
    print(output)

if __name__ == "__main__":
    main()
