from utils.byb import branchAndBound
from utils.utils import print_matrix, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.counter import reset, get_count

import time
import copy

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
    matrix = makeDifficulty(base_matrix, "hard")
    print_matrix(matrix)

    # col = 0
    # row = 0

    # v_fila: Set[int] = {matrix[row][col] for col in range(9) if matrix[row][col] != 0}
    # v_col: Set[int] = {matrix[row][col] for row in range(9) if matrix[row][col] != 0}
    # v_cuadrante: Set[int] = {matrix[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if matrix[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}
    # v_posibles: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante

    # print(v_fila)
    # print(v_col)
    # print(v_cuadrante)
    # print(v_posibles)

    print("Matriz resuelta con backtracking:")
    reset()  # Resetea todos los contadores al inicio
    # copy es un modulo de python que se usa para copiar objetos, deepcopy es una funcion que copia el objeto y todos sus atributos
    matrix_copy_bt = copy.deepcopy(matrix)  # Copia para no modificar la original
    time_start = time.time()
    matrix_solved_bt = backtracking(matrix_copy_bt)
    time_end = time.time()
    print_matrix(matrix_solved_bt)
    print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
    print("Intentos Backtracking: " + str(get_count('backtracking')))

    print("\nMatriz resuelta con branch and bound:")
    reset('byb')  # Solo resetea el contador de byb, mantiene backtracking
    matrix_copy_byb = copy.deepcopy(matrix)  # Copia fresca de la matriz original
    time_start = time.time()
    matrix_solved_byb = branchAndBound(matrix_copy_byb)
    time_end = time.time()
    print_matrix(matrix_solved_byb)
    print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
    print("Intentos Branch and Bound: " + str(get_count('byb')))
    
    print("\n=== COMPARACION ===")
    print(f"Backtracking: {get_count('backtracking')} nodos explorados")
    print(f"Branch and Bound: {get_count('byb')} nodos explorados")

if __name__ == "__main__":
    main()