from utils.byb import branchAndBound
from utils.utils import print_matrix, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.counter import reset, get_count

import time
import copy
import argparse
import sys

from typing import Literal

def run(solver: Literal['bt','bb','both'] = 'both', difficulty: Literal['easy','medium','hard'] = 'hard', verbose: bool = False):
    # Mejorar salida en Windows
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    print("""
    ███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
    ██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
    ███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
    ╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
    ███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
    ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
    """)

    print(f"Matriz inicial (dificultad={difficulty}):")
    base_matrix = iniciateBaseMatrix()
    matrix = makeDifficulty(copy.deepcopy(base_matrix), difficulty)
    print_matrix(matrix)

    if solver in ('bt', 'both'):
        print("\nMatriz resuelta con backtracking:")
        reset()  # Resetea todos los contadores al inicio
        matrix_copy_bt = copy.deepcopy(matrix)
        time_start = time.time()
        matrix_solved_bt = backtracking(matrix_copy_bt)
        time_end = time.time()
        print_matrix(matrix_solved_bt)
        print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
        print("Intentos Backtracking: " + str(get_count('backtracking')))

    if solver in ('bb', 'both'):
        print("\nMatriz resuelta con branch and bound:")
        reset('byb')  # Solo resetea el contador de byb, mantiene backtracking
        matrix_copy_byb = copy.deepcopy(matrix)
        time_start = time.time()
        matrix_solved_byb = branchAndBound(matrix_copy_byb, verbose=verbose)
        time_end = time.time()
        print_matrix(matrix_solved_byb)
        print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
        print("Intentos Branch and Bound: " + str(get_count('byb')))

    if solver == 'both':
        print("\n=== COMPARACION ===")
        print(f"Backtracking: {get_count('backtracking')} nodos explorados")
        print(f"Branch and Bound: {get_count('byb')} nodos explorados")


def main():
    parser = argparse.ArgumentParser(description='Sudoku solver demo')
    parser.add_argument('--solver', choices=['bt','bb','both'], default='both', help='Qué solver ejecutar')
    parser.add_argument('--difficulty', choices=['easy','medium','hard'], default='hard', help='Dificultad del Sudoku generado')
    parser.add_argument('--verbose', action='store_true', help='Logs verbosos para Branch & Bound')
    args = parser.parse_args()

    run(args.solver, args.difficulty, args.verbose)


if __name__ == "__main__":
    main()