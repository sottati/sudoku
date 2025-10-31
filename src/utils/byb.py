# Branch and Bound para Sudoku
# Implementación con heurística MRV y cotas solicitadas:
# - Heurística de selección (expandir primero): celda con MENOR cantidad de opciones (MRV)
# - Cota inferior (LB): mínimo de opciones disponibles en TODO el tablero (equivale al tamaño de MRV)
# - Cota superior (UB): min(minOpcionesDisponibles, maxVecesQueApareceUnValor) donde
#       maxVecesQueApareceUnValor = máximo, entre los candidatos de la celda MRV,
#       de cuántas veces aparece ese valor como candidato en el tablero actual.
#   Se usa UB para limitar cuántos hijos generar (poda del factor de ramificación).

from typing import Set, Tuple, Optional
from copy import deepcopy
import heapq
from collections import Counter
from utils.utils import isFactible
from utils.counter import increment

# Nota: esta implementación es best-first con cola de prioridad usando LB como prioridad.
# Se poda además cuando alguna celda queda con 0 candidatos.

# dado fila, columna y cuadrante para una celda, genera los valores posibles utilizando conjuntos
def generatePosibleValues(S: list[list[int]], row: int, col: int) -> Set[int]:
    # conjunto con los valores que hay en esa fila
    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en esa columna
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en ese cuadrante
    v_cuadrante: Set[int] = {S[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if S[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}

    # conjunto con los valores posibles para esa celda
    return {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante

def _all_empty_cells(S: list[list[int]]):
    for i in range(9):
        for j in range(9):
            if S[i][j] == 0:
                yield (i, j)

def _select_mrv_cell(S: list[list[int]]) -> Optional[Tuple[int, int, Set[int]]]:
    """Devuelve (row, col, candidatos) para la celda con MENOS candidatos.
    Si no hay celdas vacías, devuelve None.
    Si alguna celda tiene 0 candidatos, devuelve (row, col, set()) para indicar poda.
    """
    best: Optional[Tuple[int, int, Set[int]]] = None
    best_len = 10
    for (r, c) in _all_empty_cells(S):
        cands = generatePosibleValues(S, r, c)
        lc = len(cands)
        if lc == 0:
            return (r, c, set())  # poda inmediata
        if lc < best_len:
            best = (r, c, cands)
            best_len = lc
            if best_len == 1:
                # No puede haber menos de 1; ya es el mejor posible
                break
    return best

def _global_candidate_stats(S: list[list[int]]) -> tuple[Counter, int]:
    """Devuelve (frecuenciaGlobalDeValores, maximoTamañoDeDominioPorCelda).
    - frecuenciaGlobalDeValores: Counter con cuántas veces aparece cada valor 1..9 como candidato.
    - maximoTamañoDeDominioPorCelda: máximo número de candidatos entre todas las celdas vacías.
    """
    cnt = Counter()
    max_dom = 0
    for (r, c) in _all_empty_cells(S):
        cands = generatePosibleValues(S, r, c)
        l = len(cands)
        if l > max_dom:
            max_dom = l
        for v in cands:
            cnt[v] += 1
    return cnt, max_dom

def _compute_bounds(S: list[list[int]]):
    """Calcula cota inferior (LB) y cota superior (UB) según lo solicitado.
    - LB = tamaño de candidatos de la celda MRV = mínimo de opciones disponibles.
    - UB = min( mayorCantidadDeValoresDisponiblesPorNodo,
                max_{v en cand(MRV)} frecuenciaGlobal(v) ),
      donde mayorCantidadDeValoresDisponiblesPorNodo es el máximo tamaño de dominio
      entre todas las celdas vacías del tablero actual.
    Devuelve (LB, UB, (row,col,cands), freq_map)
    """
    mrv = _select_mrv_cell(S)
    if mrv is None:
        # tablero completo -> LB = UB = 0 por conveniencia
        return 0, 0, None, Counter()
    row, col, cands = mrv
    if len(cands) == 0:
        # ya se detectó inconsistencia -> poda
        return 0, 0, mrv, Counter()
    lb = len(cands)
    freq, max_domain = _global_candidate_stats(S)
    max_freq = max((freq[v] for v in cands), default=0)
    ub = min(max_domain, max_freq)
    return lb, ub, mrv, freq

def branchAndBound(S: list[list[int]], verbose: bool = False, debug_limit: Optional[int] = None, beam: bool = False) -> Optional[list[list[int]]]:
    """Resuelve el Sudoku usando Branch & Bound con MRV y cotas LB/UB solicitadas.
    - Prioridad de expansión: menor LB primero (best-first)
    - Poda: si alguna celda tiene 0 candidatos, se descarta el estado
    - Uso de UB: limita el número de hijos a generar (poda del branching)
    Devuelve la matriz solución o None si no hay solución.
    """

    # Si ya está completo, devolver tal cual
    if all(S[i][j] != 0 for i in range(9) for j in range(9)):
        return S

    # Min-heap de estados: (LB, tie, board)
    heap: list[tuple[int, int, list[list[int]]]] = []
    tie = 0
    iter_no = 0

    def _log(msg: str):
        if verbose:
            print(msg)

    lb0, ub0, mrv0, _ = _compute_bounds(S)
    if mrv0 is not None and len(mrv0[2]) == 0:
        return None  # inconsistente de entrada
    heapq.heappush(heap, (lb0, tie, deepcopy(S)))
    tie += 1

    while heap:
        lb, _, board = heapq.heappop(heap)
        iter_no += 1
        _log(f"[B&B] pop iter={iter_no} lb={lb} heap_size={len(heap)}")
        if debug_limit is not None and iter_no > debug_limit:
            _log("[B&B] debug_limit alcanzado; deteniendo logs (sigue resolviendo en silencio)...")
            verbose = False

        # ¿Resuelto?
        if all(board[i][j] != 0 for i in range(9) for j in range(9)):
            return board

        # Selección MRV y cotas
        cur_lb, cur_ub, mrv, freq = _compute_bounds(board)
        if mrv is None:
            # Tablero completo (ya se habría capturado arriba, pero por seguridad)
            return board
        r, c, cands = mrv
        _log(f"[B&B] MRV=({r},{c}) cands={sorted(cands)} cur_lb={cur_lb} cur_ub={cur_ub}")

        # Poda por inconsistencia
        if len(cands) == 0:
            _log("[B&B] prune: celda con 0 candidatos")
            continue

        # Ordenar candidatos por frecuencia global DESC (los más comunes primero)
        ordered = sorted(cands, key=lambda v: freq.get(v, 0), reverse=True)
        limit = min(len(cands), max(1, cur_ub))
        mode = 'beam' if beam else 'soft'
        _log(f"[B&B] ordered={ordered} limit={limit} mode={mode}")
        seq = ordered[:limit] if beam else ordered
        for idx, v in enumerate(seq):
            # Generar hijo
            child = deepcopy(board)
            child[r][c] = v
            increment('byb')
            if isFactible(child, v, r, c):
                # Calcular la prioridad del hijo
                child_lb, _, _, _ = _compute_bounds(child)
                # Empujar hijo
                heapq.heappush(heap, (child_lb, tie, child))
                rank = 'prio' if idx < limit else 'defer'
                _log(f"[B&B]  -> push v={v} child_lb={child_lb} rank={rank} new_heap_size={len(heap)}")
                tie += 1

    return None  # No se encontró solución          