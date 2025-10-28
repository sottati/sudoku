from utils.utils import print_matrix, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.counter import reset, get_count

import time

from typing import Set

def main():
    print("""
    ███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
    ██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
    ███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
    ╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
    ███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
    ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
    """)

    print("Matriz inicial:")
    base_matrix = iniciateBaseMatrix()
    # print_matrix(base_matrix)
    matrix = makeDifficulty(base_matrix, "medium")
    print_matrix(matrix)

    col = 0
    row = 0

    v_fila: Set[int] = {matrix[row][col] for col in range(9) if matrix[row][col] != 0}
    v_col: Set[int] = {matrix[row][col] for row in range(9) if matrix[row][col] != 0}
    v_posibles: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col

    print(v_fila)
    print(v_col)
    print(v_posibles)

    print("Matriz resuelta:")
    reset()
    time_start = time.time()
    matrix_solved = backtracking(matrix)
    time_end = time.time()
    print_matrix(matrix_solved)
    print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
    print("Intentos: " + str(get_count()))

if __name__ == "__main__":
    main()