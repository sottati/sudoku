import sys
import time
import statistics as stats
from typing import Literal

# Ensure unicode output looks nice on Windows if possible
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, 'c:/Users/hok/Documents/GitHub/sudoku/src')  # safe when run from repo root too

from utils.utils import set_seed, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branchAndBound

Difficulty = Literal['easy', 'medium', 'hard']


def time_solver(solver: str, difficulty: Difficulty, runs: int, seed: int | None) -> tuple[list[float], list[int]]:
    """Devuelve listas (tiempos_en_segundos, nodos_explorados) por corrida para el solver elegido.
    Sólo medimos el paso de resolución (la generación del puzzle se hace fuera del cronómetro).
    """
    if seed is not None:
        # Make each run deterministic but still vary puzzles: add offset per run
        set_seed(seed)

    times: list[float] = []
    nodes_list: list[int] = []
    for r in range(runs):
        if seed is not None:
            # Advance seed per run for different puzzles reproducibly
            set_seed(seed + r)

        base = iniciateBaseMatrix()  # full valid grid
        puzzle = makeDifficulty([row[:] for row in base], difficulty)

        metrics: dict = {}
        start = time.perf_counter()
        if solver == 'bt':
            _ = backtracking([row[:] for row in puzzle], metrics=metrics)
        elif solver == 'bb':
            _ = branchAndBound([row[:] for row in puzzle], metrics=metrics)
        else:
            raise ValueError("solver must be 'bt' or 'bb'")
        end = time.perf_counter()
        times.append(end - start)
        nodes_list.append(int(metrics.get('nodes', 0)))
    return times, nodes_list


def summarize(label: str, values: list[float]):
    if not values:
        print(f"{label}: no data")
        return
    mean = stats.mean(values)
    p50 = stats.median(values)
    p90 = stats.quantiles(values, n=10)[8] if len(values) >= 10 else max(values)
    print(f"{label}: runs={len(values)}, mean={mean:.4f}s, p50={p50:.4f}s, p90~={p90:.4f}s")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Benchmark Sudoku solvers')
    parser.add_argument('--solver', choices=['bt', 'bb', 'both'], default='both', help='Which solver to benchmark')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium')
    parser.add_argument('--runs', type=int, default=5)
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    print(f"Benchmark: solver={args.solver}, difficulty={args.difficulty}, runs={args.runs}, seed={args.seed}")

    if args.solver in ('bt', 'both'):
        t_bt, n_bt = time_solver('bt', args.difficulty, args.runs, args.seed)
        summarize('Backtracking (tiempo)', t_bt)
        print(f"Backtracking (nodos): runs={len(n_bt)}, mean={stats.mean(n_bt):.0f}, p50={stats.median(n_bt):.0f}, max={max(n_bt):.0f}")
    if args.solver in ('bb', 'both'):
        t_bb, n_bb = time_solver('bb', args.difficulty, args.runs, args.seed)
        summarize('Branch-and-Bound (tiempo)', t_bb)
        print(f"Branch-and-Bound (nodos): runs={len(n_bb)}, mean={stats.mean(n_bb):.0f}, p50={stats.median(n_bb):.0f}, max={max(n_bb):.0f}")
