"""
Branch and Bound implementation for Sudoku solver
Usa cola de prioridad y heurística MRV (Minimum Remaining Values)
"""

from utils.utils import generateValues, isFactible
from typing import Optional
import heapq

class Node:
    """Representa un nodo en el árbol de búsqueda"""
    def __init__(self, matrix: list[list[int]], empty_cells: int):
        self.matrix = [row[:] for row in matrix]  # Copia profunda
        self.empty_cells = empty_cells  # Número de celdas vacías restantes
        self.cost = self.calculate_cost()
    
    def calculate_cost(self) -> int:
        """
        Calcula el costo del nodo basado en el número de celdas vacías
        (menor es mejor)
        """
        return self.empty_cells
    
    def __lt__(self, other):
        """Comparador para la cola de prioridad"""
        return self.cost < other.cost

def count_empty_cells(matrix: list[list[int]]) -> int:
    """Cuenta el número de celdas vacías en la matriz"""
    count = 0
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                count += 1
    return count

def get_min_remaining_values_cell(matrix: list[list[int]]) -> tuple[int, int, list[int]]:
    """
    Encuentra la celda vacía con menor número de valores posibles (MRV heuristic)
    Retorna: (row, col, possible_values)
    """
    min_options = 10
    best_cell = None
    best_values = []
    
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                possible_values = []
                for value in generateValues():
                    # Crear copia temporal para verificar
                    temp_matrix = [row[:] for row in matrix]
                    temp_matrix[i][j] = value
                    if isFactible(temp_matrix, value, i, j):
                        possible_values.append(value)
                
                if len(possible_values) < min_options:
                    min_options = len(possible_values)
                    best_cell = (i, j)
                    best_values = possible_values
                    
                    # Si no hay valores posibles, retornar inmediatamente
                    if min_options == 0:
                        return i, j, []
    
    if best_cell:
        return best_cell[0], best_cell[1], best_values
    return -1, -1, []

def is_complete(matrix: list[list[int]]) -> bool:
    """Verifica si el sudoku está completamente resuelto"""
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True

def branch_and_bound(matrix: list[list[int]]) -> Optional[list[list[int]]]:
    """
    Resuelve el Sudoku usando Branch and Bound con cola de prioridad
    
    Estrategia:
    - Usa una cola de prioridad (min-heap) para explorar nodos más prometedores primero
    - Aplica MRV (Minimum Remaining Values) para elegir la mejor celda a llenar
    - Poda nodos que no tienen solución posible
    """
    
    # Inicializar estructura (cola de prioridad)
    priority_queue = []
    
    # Crear nodo raíz
    empty_count = count_empty_cells(matrix)
    root_node = Node(matrix, empty_count)
    
    # Agregar nodo raíz a la cola
    heapq.heappush(priority_queue, root_node)
    
    # Contador de nodos explorados
    nodes_explored = 0
    
    while priority_queue:
        # Obtener el nodo más prometedor
        current_node = heapq.heappop(priority_queue)
        nodes_explored += 1
        
        # Verificar si es solución completa
        if is_complete(current_node.matrix):
            print(f"Solución encontrada! Nodos explorados: {nodes_explored}")
            return current_node.matrix
        
        # Encontrar la mejor celda para expandir (MRV heuristic)
        row, col, possible_values = get_min_remaining_values_cell(current_node.matrix)
        
        # Poda: si no hay celda vacía o no hay valores posibles
        if row == -1 or len(possible_values) == 0:
            continue
        
        # Generar hijos (branches)
        for value in possible_values:
            # Crear nueva matriz con el valor asignado
            new_matrix = [row[:] for row in current_node.matrix]
            new_matrix[row][col] = value
            
            # Verificar factibilidad (redundante pero por seguridad)
            if isFactible(new_matrix, value, row, col):
                # Calcular celdas vacías
                new_empty_count = current_node.empty_cells - 1
                
                # Crear nuevo nodo hijo
                child_node = Node(new_matrix, new_empty_count)
                
                # Agregar a la cola de prioridad
                heapq.heappush(priority_queue, child_node)
    
    print(f"No se encontró solución. Nodos explorados: {nodes_explored}")
    return None