"""
Implementación de Branch and Bound para resolver Sudoku
Autor: santiago-garbini
Fecha: 2025-11-01

Branch and Bound con cola de prioridad INTERNA de celdas vacías.

Heurística: Most Constrained Variable (MCV) implementada con heap
Cota Inferior: Mínimo de opciones disponibles en cualquier celda vacía
Cota Superior: Máximo de opciones disponibles en cualquier celda vacía
"""

from typing import Set, Tuple, Optional, List
from utils.counter import increment
import heapq


class SudokuNode:
    """
    Representa un nodo en el árbol de búsqueda de Branch and Bound
    
    Attributes:
        matrix: Estado actual del tablero (9x9)
        depth: Profundidad del nodo en el árbol
        cells_heap: Cola de prioridad de celdas vacías (ordenadas por MCV)
        lower_bound: Mínimo de opciones en alguna celda vacía
        upper_bound: Máximo de opciones en alguna celda vacía
    """
    
    def __init__(self, matrix: list[list[int]], depth: int = 0):
        self.matrix = [row[:] for row in matrix]
        self.depth = depth
        self.cells_heap: List[Tuple[int, int, int, Set[int]]] = []
        self.lower_bound = float('inf')
        self.upper_bound = 0
        self._build_cells_heap()
        
    def _build_cells_heap(self):
        """
        Construye la cola de prioridad de celdas vacías.
        
        REEMPLAZA a find_most_constrained_cell():
        - En lugar de buscar la celda más restringida cada vez,
          construimos un heap UNA VEZ con todas las celdas vacías
        - El heap mantiene automáticamente las celdas ordenadas por MCV
        
        Heap contiene tuplas: (num_opciones, row, col, opciones_disponibles)
        Ordenado automáticamente por num_opciones (menor primero)
        
        También calcula las cotas mientras construye el heap.
        """
        counter = 0
        min_options = float('inf')
        max_options = 0
        
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    options = self._get_available_values(i, j)
                    num_options = len(options)
                    
                    if num_options == 0:
                        # Estado inválido
                        self.lower_bound = float('inf')
                        self.upper_bound = float('inf')
                        self.cells_heap = []
                        return
                    
                    # Actualizar cotas
                    min_options = min(min_options, num_options)
                    max_options = max(max_options, num_options)
                    
                    # Agregar celda al heap
                    # (num_opciones, row, col, counter, opciones)
                    heapq.heappush(self.cells_heap, (num_options, i, j, counter, options))
                    counter += 1
        
        # Establecer cotas
        if not self.cells_heap:
            # No hay celdas vacías (sudoku resuelto)
            self.lower_bound = 0
            self.upper_bound = 0
        else:
            self.lower_bound = min_options
            self.upper_bound = max_options
    
    def _get_available_values(self, row: int, col: int) -> Set[int]:
        """Calcula los valores disponibles para una celda específica."""
        if self.matrix[row][col] != 0:
            return set()
        
        all_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        used_in_row = {self.matrix[row][c] for c in range(9) if self.matrix[row][c] != 0}
        used_in_col = {self.matrix[r][col] for r in range(9) if self.matrix[r][col] != 0}
        
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        used_in_box = set()
        
        for i in range(3):
            for j in range(3):
                val = self.matrix[box_row + i][box_col + j]
                if val != 0:
                    used_in_box.add(val)
        
        return all_values - used_in_row - used_in_col - used_in_box
    
    def get_most_constrained_cell(self) -> Optional[Tuple[int, int, Set[int]]]:
        """
        Extrae la celda más restringida del heap.
        
        ANTES: Recorría todo el tablero O(81)
        AHORA: Extrae del heap O(log n)
        
        Returns:
            Optional[Tuple[int, int, Set[int]]]: (fila, columna, opciones) o None
        """
        if not self.cells_heap:
            return None  # No hay celdas vacías
        
        # Extraer la celda con MENOS opciones (cabeza del heap)
        num_options, row, col, _, options = heapq.heappop(self.cells_heap)
        
        return (row, col, options)
    
    def is_solved(self) -> bool:
        """Verifica si el sudoku está resuelto (no hay celdas en el heap)."""
        return len(self.cells_heap) == 0
    
    def __lt__(self, other):
        """Comparador para la cola de prioridad de nodos."""
        if self.lower_bound != other.lower_bound:
            return self.lower_bound < other.lower_bound
        if self.upper_bound != other.upper_bound:
            return self.upper_bound < other.upper_bound
        return self.depth > other.depth


def branch_and_bound(matrix: list[list[int]]) -> Optional[list[list[int]]]:
    """
    Resuelve el Sudoku usando Branch and Bound con poda por cotas.
    
    MEJORA: Usa heap interno en cada nodo para MCV eficiente.
    
    Args:
        matrix: Matriz 9x9 del sudoku con 0 en celdas vacías
    
    Returns:
        Optional[list[list[int]]]: Matriz resuelta o None si no hay solución
    """
    priority_queue = []
    counter = 0
    
    initial_node = SudokuNode(matrix, depth=0)
    
    if initial_node.lower_bound == float('inf'):
        return None
    
    heapq.heappush(priority_queue, (initial_node.lower_bound, initial_node.upper_bound, counter, initial_node))
    counter += 1
    
    upper_bound_global = float('inf')
    best_solution = None
    
    while priority_queue:
        current_lb, current_ub, _, current_node = heapq.heappop(priority_queue)
        
        # Poda explícita
        if current_node.lower_bound >= upper_bound_global:
            continue
        
        # ¿Solución encontrada?
        if current_node.is_solved():
            solution_ub = current_node.upper_bound
            
            if solution_ub < upper_bound_global:
                upper_bound_global = solution_ub
                best_solution = current_node.matrix
            
            continue
        
        # MEJORA: Extraer celda más restringida del heap O(log n)
        result = current_node.get_most_constrained_cell()
        
        if result is None:
            continue
        
        row, col, available_values = result
        
        # Generar hijos
        for value in sorted(available_values):
            increment()
            
            new_matrix = [r[:] for r in current_node.matrix]
            new_matrix[row][col] = value
            
            child_node = SudokuNode(new_matrix, depth=current_node.depth + 1)
            
            # Poda implícita
            if child_node.lower_bound < upper_bound_global:
                heapq.heappush(priority_queue, 
                             (child_node.lower_bound, child_node.upper_bound, counter, child_node))
                counter += 1
    
    return best_solution