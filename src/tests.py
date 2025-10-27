"""Pruebas rápidas (ad-hoc) para verificar comportamiento de los solvers.

Este módulo no usa un framework de testing formal; sirve como smoke-test:
- Construye una solución base.
- Genera un puzzle con cierta dificultad.
- Resuelve con backtracking y con branch-and-bound.
- Verifica que ambas soluciones sean idénticas (misma grilla final).
"""

from utils import print_matrix, initialize_matrix, populate_matrix, set_seed
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branchAndBound
from utils.utils import makeDifficulty


def printCuadrante(cuadrante: list[list[int]]):
    """Imprime una submatriz 3x3 (útil para depurar cuadrantes)."""
    for i in range(3):
        for j in range(3):
            print(cuadrante[i][j], end=" ")
        print()


def _is_valid_solution(solution: list[list[int]]) -> bool:
    """Chequea que la solución sea un Sudoku válido (sin considerar las pistas originales).

    - Todas las celdas en 1..9
    - Filas/columnas contienen exactamente {1..9}
    - Cada bloque 3x3 contiene exactamente {1..9}
    """
    nums = set(range(1, 10))
    # Filas
    for r in range(9):
        row = solution[r]
        if any(v not in nums for v in row):
            return False
        if set(row) != nums:
            return False
    # Columnas
    for c in range(9):
        col = {solution[r][c] for r in range(9)}
        if col != nums:
            return False
    # Bloques 3x3
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = {solution[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)}
            if block != nums:
                return False
    return True


def _respects_clues(puzzle: list[list[int]], solution: list[list[int]]) -> bool:
    """Verifica que la solución respete las pistas del puzzle (mismas celdas fijas)."""
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0 and puzzle[r][c] != solution[r][c]:
                return False
    return True


def test_solvers_equal(difficulty: str = "medium"):
    """Genera un puzzle y verifica que ambos solvers produzcan soluciones válidas.

    Nota: Los puzzles generados no garantizan unicidad. Si ambos solvers dan soluciones diferentes
    pero válidas y respetan las pistas, se considera OK y se reporta como tal.
    """
    base = iniciateBaseMatrix()
    puzzle = makeDifficulty([row[:] for row in base], difficulty)

    sol_bt = backtracking([row[:] for row in puzzle])
    sol_bb = branchAndBound([row[:] for row in puzzle])

    # Validar soluciones
    assert _is_valid_solution(sol_bt), "Backtracking produjo una solución inválida"
    assert _is_valid_solution(sol_bb), "Branch-and-Bound produjo una solución inválida"
    assert _respects_clues(puzzle, sol_bt), "Backtracking no respeta las pistas del puzzle"
    assert _respects_clues(puzzle, sol_bb), "Branch-and-Bound no respeta las pistas del puzzle"

    if sol_bt == sol_bb:
        print(f"OK: Ambas soluciones coinciden para dificultad '{difficulty}'.")
        print_matrix(sol_bb)
    else:
        print(
            f"OK: Soluciones diferentes pero válidas para dificultad '{difficulty}' "
            "(el puzzle puede tener múltiples soluciones)."
        )
        print("Solución Backtracking:")
        print_matrix(sol_bt)
        print("Solución Branch-and-Bound:")
        print_matrix(sol_bb)


if __name__ == "__main__":
    # Ajuste de salida para que el print de la matriz se vea bien en Windows
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    import argparse
    parser = argparse.ArgumentParser(description="Tests rápidos del solver")
    parser.add_argument("--seed", type=int, default=None, help="Semilla aleatoria para reproducibilidad")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium")
    args = parser.parse_args()

    set_seed(args.seed)
    test_solvers_equal(difficulty=args.difficulty)