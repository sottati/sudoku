from utils.utils import print_matrix, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking

def main():

    base_matrix = iniciateBaseMatrix()
    print_matrix(base_matrix)
    matrix = makeDifficulty(base_matrix, "easy")
    print_matrix(matrix)

    print("Matriz resuelta:")
    matrix_solved = backtracking(matrix)
    print_matrix(matrix_solved)

if __name__ == "__main__":
    main()