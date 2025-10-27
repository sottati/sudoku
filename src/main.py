"""Entrypoint/CLI del proyecto.

Permite elegir solver y dificultad desde la línea de comandos. También acepta una
semilla de aleatoriedad para reproducir tanto la solución base como el puzzle
generado por makeDifficulty.
"""

from utils.utils import print_matrix, makeDifficulty, set_seed
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branchAndBound


def run(solver: str = "bb", difficulty: str = "hard", seed: int | None = None, show_metrics: bool = False):
    """
    Ejecuta el demo del solver con parámetros:
    - solver: "bt" (backtracking) | "bb" (branch-and-bound)
    - difficulty: "easy" | "medium" | "hard"
    """
    try:
        # Mejor salida en Windows con caracteres Unicode
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # Semilla para reproducibilidad (opcional). Afecta a la solución base y al puzzle.
    set_seed(seed)

    base_matrix = iniciateBaseMatrix()
    print("Base completa:")
    print_matrix(base_matrix)

    # Crear el puzzle a partir de la base. Usamos una copia para no mutar la base.
    matrix = makeDifficulty([row[:] for row in base_matrix], difficulty)
    print(f"Puzzle ({difficulty}):")
    print_matrix(matrix)

    print("Matriz resuelta (" + ("backtracking" if solver == "bt" else "branch-and-bound") + "):")
    # Métricas opcionales de rendimiento
    metrics: dict = {}
    import time
    t0 = time.perf_counter()
    if solver == "bb":
        # B&B opera sobre copias para no alterar el puzzle original.
        matrix_solved = branchAndBound([row[:] for row in matrix], metrics=metrics)
    else:
        matrix_solved = backtracking([row[:] for row in matrix], metrics=metrics)
    t1 = time.perf_counter()
    print_matrix(matrix_solved)
    if show_metrics:
        print(f"Tiempo de resolución: {t1 - t0:.4f} s | Nodos explorados: {int(metrics.get('nodes', 0))}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sudoku solver demo")
    # Alineamos los defaults con la función run(solver="bb", difficulty="hard")
    parser.add_argument("--solver", choices=["bt", "bb"], default="bb", help="bt=backtracking, bb=branch-and-bound")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="hard")
    parser.add_argument("--seed", type=int, default=None, help="Semilla aleatoria para reproducibilidad")
    parser.add_argument("--metrics", action="store_true", help="Muestra tiempo y nodos explorados al resolver")
    args = parser.parse_args()

    run(solver=args.solver, difficulty=args.difficulty, seed=args.seed, show_metrics=args.metrics)
