"""
Branch and Bound para resolver Sudoku (9x9)

Estrategia utilizada (enfoque práctico para este proyecto):
- Estado = matriz 9x9 actual (lista de listas de ints).
- Costo (cota inferior) = cantidad de celdas vacías (0) restantes. Cuantas menos vacías,
    más prometedor el nodo (priorizamos por menor costo en un heap).
- Poda: si alguna celda vacía no tiene valores factibles, se descarta el nodo inmediatamente.
- Expansión: elegir la celda con menos candidatos (heurística MRV = Minimum Remaining Values)
    y generar un hijo por cada candidato.

Diagrama simplificado del ciclo:
        estado -> seleccionar celda con menos candidatos (MRV)
                     -> por cada candidato v: crear hijo con v colocado
                     -> calcular costo = #0s y meter en heap (frontera)
                     -> extraer del heap el estado con menor costo y repetir

Comentarios:
- Operativamente se parece a un backtracking con MRV, pero el orden de exploración lo decide
    una cola de prioridad (frontera) basada en la cota. Esto puede explorar primero estados más "llenos".
- Es fácil de entender y suficientemente eficiente para sudokus típicos.

Complejidad y casos límite:
- La complejidad en el peor caso sigue siendo exponencial, pero MRV + poda reducen mucho el espacio.
- Si el Sudoku ya está completo, se devuelve tal cual.
- Si es insatisfactible, la frontera se vacía tras podas sucesivas y devolvemos None.
"""

from copy import deepcopy
from heapq import heappop, heappush
from typing import List, Optional, Tuple

from utils.utils import generateValues, isFactible

Matrix = List[List[int]]


def _count_zeros(S: Matrix) -> int:
    """Cuenta cuántas celdas siguen vacías (0). Se usa como cota/costo del nodo."""
    return sum(1 for i in range(9) for j in range(9) if S[i][j] == 0)


def _candidates(S: Matrix, row: int, col: int) -> list[int]:
    """Valores factibles en (row, col) según utilidades existentes (isFactible)."""
    vals = []
    for v in generateValues():
        if isFactible(S, v, row, col):
            vals.append(v)
    return vals


def _select_cell_with_fewest_candidates(S: Matrix) -> Optional[Tuple[int, int, list[int]]]:
    """Devuelve (row, col, candidatos) de la celda vacía con menos candidatos (MRV).
    Si no hay celdas vacías, devuelve None (estado objetivo).

    Poda temprana: si alguna celda vacía no tiene candidatos (lista vacía), este estado es
    inconsistente y debe descartarse.
    """
    best: Optional[Tuple[int, int, list[int]]] = None
    best_len = 10  # mayor a 9
    for i in range(9):
        for j in range(9):
            if S[i][j] == 0:
                cand = _candidates(S, i, j)
                l = len(cand)
                if l == 0:
                    # Poda inmediata
                    return (i, j, [])
                if l < best_len:
                    best = (i, j, cand)
                    best_len = l
                    if best_len == 1:
                        # no hay mejor que 1
                        return best
    return best


def branchAndBound(S: Matrix, metrics: dict | None = None) -> Optional[Matrix]:
    """Resuelve el Sudoku usando Branch&Bound. Devuelve la matriz resuelta o None si no hay solución.

    Contrato breve:
    - Entrada: matriz 9x9 con 0 para celdas vacías.
    - Salida: matriz 9x9 válida, o None si es insatisfactible.
    - Errores: no arroja excepciones; retorna None si toda la frontera fue podada.
    """

    # Inicializar heap con el estado inicial.
    # Cada item es (costo, tie_break, matriz). Usamos un contador (tie_break) para evitar
    # que Python intente comparar matrices cuando los costos empatan.
    heap: list[tuple[int, int, Matrix]] = []
    tie = 0
    if metrics is not None:
        # Inicializar contadores
        metrics.setdefault("nodes", 0)  # nodos expandidos (pops del heap)
        metrics.setdefault("generated", 0)  # hijos generados

    # Validación/poda rápida: si ya no hay vacías, devolver
    sel = _select_cell_with_fewest_candidates(S)
    if sel is None:
        return S
    row, col, cand = sel
    if len(cand) == 0:
        return None  # insatisfactible desde el inicio

    heappush(heap, (_count_zeros(S), tie, deepcopy(S)))
    tie += 1

    while heap:
        _, _, state = heappop(heap)
        if metrics is not None:
            metrics["nodes"] += 1

        choice = _select_cell_with_fewest_candidates(state)
        if choice is None:
            # No hay vacías: solución encontrada
            return state

        r, c, candidates = choice
        if len(candidates) == 0:
            # poda: estado inválido
            continue

        # Rama: por cada candidato generamos un hijo colocando el valor y evaluando nuevamente.
        for v in candidates:
            child = deepcopy(state)
            child[r][c] = v

            # Poda temprana: verificar que no generamos una contradicción inmediata.
            # (Ya generamos candidatos factibles, pero puede liberar restricciones en otra celda.)
            # Si en el nuevo estado alguna celda queda sin candidatos, se descarta al insertar.
            next_sel = _select_cell_with_fewest_candidates(child)
            if next_sel is not None and len(next_sel[2]) == 0:
                continue  # poda

            heappush(heap, (_count_zeros(child), tie, child))
            tie += 1
            if metrics is not None:
                metrics["generated"] += 1

    # Nada quedó en la frontera: no hay solución
    return None
                        