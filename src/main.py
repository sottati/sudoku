import copy
from utils.utils import print_matrix, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branch_and_bound
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

    base_matrix = iniciateBaseMatrix()
    matrix = makeDifficulty(base_matrix, "hard")
    
    print("\n" + "="*70)
    print("SUDOKU A RESOLVER")
    print("="*70)
    print_matrix(matrix)
    
    # Contador de celdas vacías
    empty_cells = sum(1 for i in range(9) for j in range(9) if matrix[i][j] == 0)
    print(f"\n📊 Celdas vacías: {empty_cells}/81")
    print(f"📊 Dificultad: ALTA")

    # ============================================================
    # MÉTODO 1: BACKTRACKING
    # ============================================================
    print("\n" + "="*70)
    print("RESOLVIENDO CON BACKTRACKING")
    print("="*70)
    
    matrix_bt = [row[:] for row in matrix]
    reset()
    copy_matriz = copy.deepcopy(matrix_bt)
    time_start = time.time()
    matrix_solved_bt = backtracking(copy_matriz)
    time_end = time.time()
    
    if matrix_solved_bt:
        print("\n✅ Matriz resuelta con Backtracking:")
        print_matrix(matrix_solved_bt)


        print(f"\n⏱️  Tiempo de ejecución: {time_end - time_start:.6f} segundos")
        print(f"🔢 Intentos realizados: {get_count('backtracking'):,}")
    else:
        print("\n❌ No se encontró solución con Backtracking")

    # ============================================================
    # MÉTODO 2: BRANCH AND BOUND
    # ============================================================

    
    matrix_bnb = [row[:] for row in matrix]
    reset()
    time_start = time.time()
    matrix_solved_bnb = branch_and_bound(matrix_bnb)
    time_end = time.time()
    
    if matrix_solved_bnb:
        print("\n✅ Matriz resuelta con Branch and Bound:")
        print_matrix(matrix_solved_bnb)
        print(f"\n⏱️  Tiempo de ejecución: {time_end - time_start:.6f} segundos")
        print(f"🔢 Intentos realizados: {get_count():,}")
    else:
        print("\n❌ No se encontró solución con Branch and Bound")


if __name__ == "__main__":
    main()