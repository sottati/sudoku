from utils.byb import branchAndBound
from utils.utils import print_matrix, makeDifficulty, isFactible
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.counter import reset, get_count

import time
import copy
import argparse
import sys

from typing import Literal

def _is_complete_and_valid(board: list[list[int]]) -> bool:
    # No ceros
    if any(board[i][j] == 0 for i in range(9) for j in range(9)):
        return False
    # Cada celda respeta fila/columna/cuadrante
    for i in range(9):
        for j in range(9):
            v = board[i][j]
            if v < 1 or v > 9:
                return False
            if not isFactible(board, v, i, j):
                return False
    return True


def run(solver: Literal['bt','bb','both'] = 'both', difficulty: Literal['easy','medium','hard'] = 'hard', verbose: bool = False, beam: bool = False):
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

    matrix_solved_bt = None
    matrix_solved_byb = None

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
        print("Valida (BT): ", _is_complete_and_valid(matrix_solved_bt))

    if solver in ('bb', 'both'):
        print("\nMatriz resuelta con branch and bound:")
        reset('byb')  # Solo resetea el contador de byb, mantiene backtracking
        matrix_copy_byb = copy.deepcopy(matrix)
        time_start = time.time()
        matrix_solved_byb = branchAndBound(matrix_copy_byb, verbose=verbose, beam=beam)
        time_end = time.time()
        print_matrix(matrix_solved_byb)
        print("Tiempo de ejecucion: " + str(time_end - time_start) + " segundos")
        print("Intentos Branch and Bound: " + str(get_count('byb')))
        print("Valida (B&B): ", _is_complete_and_valid(matrix_solved_byb) if matrix_solved_byb else False)

    if solver == 'both':
        print("\n=== COMPARACION ===")
        print(f"Backtracking: {get_count('backtracking')} nodos explorados")
        print(f"Branch and Bound: {get_count('byb')} nodos explorados")
        iguales = (matrix_solved_bt is not None and matrix_solved_byb is not None and matrix_solved_bt == matrix_solved_byb)
        print(f"¿Soluciones iguales?: {iguales}")


def main():
    parser = argparse.ArgumentParser(description='Sudoku solver demo')
    parser.add_argument('--solver', choices=['bt','bb','both'], default='both', help='Qué solver ejecutar')
    parser.add_argument('--difficulty', choices=['easy','medium','hard'], default='hard', help='Dificultad del Sudoku generado')
    parser.add_argument('--verbose', action='store_true', help='Logs verbosos para Branch & Bound')
    parser.add_argument('--beam', action='store_true', help='Aplicar UB como corte duro (beam search, no completo)')
    args = parser.parse_args()

    run(args.solver, args.difficulty, args.verbose, args.beam)


if __name__ == "__main__":
    main()