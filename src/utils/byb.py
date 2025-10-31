"""
Implementación de Branch and Bound para resolver Sudoku
Autor: santiago-garbini
Fecha: 2025-10-31

Heurística: Most Constrained Variable (MCV) - Siempre buscar la celda con menor cantidad de opciones disponibles
Cota inferior: Mínimo de opciones disponibles en cualquier celda vacía
Cota superior: Mínimo entre:
    1. Mayor cantidad de valores disponibles por celda (restricción local)
    2. Menor cantidad de lugares restantes para colocar un valor (restricción global)
"""

from typing import Set, Tuple, Optional
from utils.counter import increment
import heapq


class SudokuNode:
    """
    Representa un nodo en el árbol de búsqueda de Branch and Bound
    
    Attributes:
        matrix: Estado actual del tablero (9x9)
        depth: Profundidad del nodo en el árbol
        lower_bound: Cota inferior (mejor caso optimista)
        upper_bound: Cota superior (peor caso razonable)
    """
    
    def __init__(self, matrix: list[list[int]], depth: int = 0):
        self.matrix = [row[:] for row in matrix]  # Copia profunda de la matriz
        self.depth = depth
        self.lower_bound = self._calculate_lower_bound()
        self.upper_bound = self._calculate_upper_bound()
        
    def _calculate_lower_bound(self) -> int:
        """
        Calcula la cota inferior del nodo.
        
        Cota Inferior = Mínimo número de opciones disponibles en cualquier celda vacía
        
        Representa el "mejor caso optimista": la celda más fácil de llenar.
        Si alguna celda no tiene opciones disponibles, retorna infinito (estado inválido).
        Si no hay celdas vacías, retorna 0 (sudoku resuelto).
        
        Returns:
            int: Mínimo de opciones disponibles, infinito si es inválido, 0 si está resuelto
        """
        min_options = float('inf')
        
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:  # Solo evaluar celdas vacías
                    options = self._get_available_values(i, j)
                    
                    if len(options) == 0:
                        # Estado inválido: celda vacía sin opciones disponibles
                        return float('inf')
                    
                    min_options = min(min_options, len(options))
        
        # Si no encontró celdas vacías, el sudoku está completo
        return min_options if min_options != float('inf') else 0
    
    def _calculate_upper_bound(self) -> int:
        """
        Calcula la cota superior del nodo usando DOS criterios complementarios.
        
        Criterio 1 (Restricción LOCAL): 
            Mayor cantidad de opciones disponibles en alguna celda vacía.
            Mide la complejidad desde la perspectiva de celdas individuales.
            Ejemplo: Si una celda tiene 7 opciones, es muy "libre" y difícil de resolver.
        
        Criterio 2 (Restricción GLOBAL):
            Menor cantidad de lugares restantes para colocar algún valor.
            Mide la complejidad desde la perspectiva del tablero completo.
            Ejemplo: Si el número 6 ya aparece 8 veces, solo queda 1 lugar para él.
        
        Cota Superior = min(Criterio 1, Criterio 2)
        
        Se toma el MÍNIMO porque representa el factor MÁS LIMITANTE:
        - Si una celda tiene 8 opciones (Criterio 1) pero un valor solo puede ir en 2 lugares (Criterio 2),
          el cuello de botella real es el Criterio 2 (más restrictivo).
        
        Returns:
            int: El valor del factor más limitante
        """
        # CRITERIO 1: Mayor cantidad de opciones en una celda (restricción local)
        max_options_per_cell = 0
        
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    options = self._get_available_values(i, j)
                    max_options_per_cell = max(max_options_per_cell, len(options))
        
        # CRITERIO 2: Menor cantidad de lugares restantes para un valor (restricción global)
        
        # Paso 1: Contar cuántas veces aparece cada valor en el tablero
        value_counts = {}
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] != 0:
                    value = self.matrix[i][j]
                    value_counts[value] = value_counts.get(value, 0) + 1
        
        # Paso 2: Calcular cuántos lugares QUEDAN para cada valor
        # En un sudoku completo, cada número debe aparecer exactamente 9 veces
        min_remaining_places = 9  # Máximo posible
        
        for value in range(1, 10):  # Valores del 1 al 9
            count = value_counts.get(value, 0)  # Cuántas veces ya aparece
            remaining = 9 - count  # Cuántas veces más debe aparecer
            
            if remaining > 0:  # Solo considerar valores aún no completos
                min_remaining_places = min(min_remaining_places, remaining)
        
        # COMBINACIÓN: Tomar el factor MÁS LIMITANTE
        if max_options_per_cell > 0:
            return min(max_options_per_cell, min_remaining_places)
        else:
            # No hay celdas vacías, usar solo el criterio global
            return min_remaining_places
    
    def _get_available_values(self, row: int, col: int) -> Set[int]:
        """
        Calcula los valores disponibles para una celda específica.
        
        Considera las tres restricciones del Sudoku:
        1. No puede repetir valores en la misma fila
        2. No puede repetir valores en la misma columna
        3. No puede repetir valores en el mismo cuadrante 3x3
        
        Args:
            row: Fila de la celda (0-8)
            col: Columna de la celda (0-8)
        
        Returns:
            Set[int]: Conjunto de valores disponibles (1-9)
        """
        if self.matrix[row][col] != 0:
            return set()  # Celda ya ocupada
        
        all_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        # Restricción 1: Valores ya usados en la fila
        v_fila = {self.matrix[row][c] for c in range(9) if self.matrix[row][c] != 0}
        
        # Restricción 2: Valores ya usados en la columna
        v_col = {self.matrix[r][col] for r in range(9) if self.matrix[r][col] != 0}
        
        # Restricción 3: Valores ya usados en el cuadrante 3x3
        cuadrante_row = (row // 3) * 3  # Fila inicial del cuadrante
        cuadrante_col = (col // 3) * 3  # Columna inicial del cuadrante
        v_cuadrante = set()
        
        for i in range(3):
            for j in range(3):
                val = self.matrix[cuadrante_row + i][cuadrante_col + j]
                if val != 0:
                    v_cuadrante.add(val)
        
        # Valores disponibles = Todos - (usados en fila + columna + cuadrante)
        return all_values - v_fila - v_col - v_cuadrante
    
    def find_most_constrained_cell(self) -> Optional[Tuple[int, int, Set[int]]]:
        """
        Implementa la heurística MCV (Most Constrained Variable).
        
        Encuentra la celda vacía con MENOR cantidad de opciones disponibles.
        Esta heurística es clave para reducir el espacio de búsqueda:
        - Elegir primero las celdas más restringidas reduce el factor de ramificación
        - Detecta inconsistencias más temprano (fail-fast)
        - Guía la búsqueda hacia soluciones prometedoras
        
        Returns:
            Optional[Tuple[int, int, Set[int]]]: 
                (fila, columna, valores_disponibles) de la celda más restringida,
                o None si no hay celdas vacías o si hay un estado inválido
        """
        min_options = float('inf')
        best_cell = None
        best_values = None
        
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    available = self._get_available_values(i, j)
                    
                    if len(available) == 0:
                        # Estado inválido: celda vacía sin opciones
                        return None
                    
                    if len(available) < min_options:
                        min_options = len(available)
                        best_cell = (i, j)
                        best_values = available
        
        if best_cell:
            return (best_cell[0], best_cell[1], best_values)
        
        return None  # No hay celdas vacías (sudoku resuelto)
    
    def is_solved(self) -> bool:
        """
        Verifica si el sudoku está completamente resuelto.
        
        Returns:
            bool: True si todas las celdas están llenas, False en caso contrario
        """
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    return False
        return True
    
    def __lt__(self, other):
        """
        Comparador para la cola de prioridad (heap).
        
        Prioriza nodos con MENOR lower_bound (más restringidos = más prometedores).
        En caso de empate, prioriza mayor profundidad (más cercano a solución).
        
        Args:
            other: Otro SudokuNode para comparar
        
        Returns:
            bool: True si este nodo tiene prioridad sobre el otro
        """
        if self.lower_bound != other.lower_bound:
            return self.lower_bound < other.lower_bound
        return self.depth > other.depth


def branch_and_bound(matrix: list[list[int]]) -> Optional[list[list[int]]]:
    """
    Resuelve el Sudoku usando el algoritmo Branch and Bound con cola de prioridad.
    
    Algoritmo:
    1. Crear nodo raíz con el estado inicial
    2. Agregar a la cola de prioridad (ordenada por lower_bound)
    3. Mientras la cola no esté vacía:
       a. Extraer nodo con menor lower_bound
       b. Si está resuelto, retornar solución ✓
       c. Si se puede podar (lower_bound > cota_global), descartar ✗
       d. Actualizar cota_global con upper_bound del nodo
       e. Encontrar celda más restringida (heurística MCV)
       f. Generar nodos hijos (uno por cada valor disponible)
       g. Para cada hijo:
          - Si lower_bound <= cota_global: agregar a cola
          - Si no: podar (no agregar)
    4. Si la cola se vacía sin solución, no hay solución
    
    Poda Explícita:
    - Se descarta un nodo cuando su lower_bound supera la cota_global
    - Esto significa que incluso en el mejor caso, este nodo no puede mejorar
      la mejor solución encontrada hasta ahora
    
    Args:
        matrix: Matriz 9x9 del sudoku con 0 en celdas vacías
    
    Returns:
        Optional[list[list[int]]]: Matriz resuelta o None si no hay solución
    """
    # Cola de prioridad: elementos son tuplas (lower_bound, contador, nodo)
    # - lower_bound: criterio de prioridad (menor = más prioritario)
    # - contador: desempate para nodos con mismo lower_bound (evita comparar nodos)
    # - nodo: el SudokuNode actual
    priority_queue = []
    counter = 0  # Contador global para desempate
    
    # Crear nodo raíz (estado inicial)
    initial_node = SudokuNode(matrix, depth=0)
    heapq.heappush(priority_queue, (initial_node.lower_bound, counter, initial_node))
    counter += 1
    
    # Cota superior global: mejor upper_bound encontrado hasta ahora
    # Inicialmente infinito (no hemos encontrado ningún nodo)
    cota_global = float('inf')
    
    # Actualizar cota global con el nodo inicial
    if initial_node.upper_bound < cota_global:
        cota_global = initial_node.upper_bound
    
    # Estadísticas para análisis
    
    
    # Bucle principal de Branch and Bound
    while priority_queue:
        # Extraer nodo con menor lower_bound (más prometedor)
        current_lower_bound, _, current_node = heapq.heappop(priority_queue)
        nodes_explored += 1
        
        # ¿Encontramos la solución?
        if current_node.is_solved():
            print(f"\n[Branch & Bound] ✓ Solución encontrada")
            return current_node.matrix
        
        # PODA EXPLÍCITA: Si la cota inferior supera la cota global, descartar
        if current_node.lower_bound > cota_global:
            nodes_pruned += 1
            continue  # No explorar este nodo
        
        # Actualizar cota global si este nodo tiene mejor upper_bound
        if current_node.upper_bound < cota_global:
            cota_global = current_node.upper_bound
        
        # HEURÍSTICA MCV: Encontrar la celda con menos opciones disponibles
        result = current_node.find_most_constrained_cell()
        
        if result is None:
            # Estado inválido (alguna celda sin opciones disponibles)
            nodes_pruned += 1
            continue
        
        row, col, available_values = result
        
        # GENERAR NODOS HIJOS: uno por cada valor disponible para la celda seleccionada
        for value in sorted(available_values):  # Ordenar para consistencia
            increment()  # Contar este intento en las estadísticas
            
            # Crear nueva matriz con el valor asignado
            new_matrix = [r[:] for r in current_node.matrix]
            new_matrix[row][col] = value
            
            # Crear nuevo nodo hijo
            child_node = SudokuNode(new_matrix, depth=current_node.depth + 1)
            
            # PODA EXPLÍCITA: Solo agregar el hijo si su lower_bound no supera la cota global
            if child_node.lower_bound <= cota_global:
                heapq.heappush(priority_queue, (child_node.lower_bound, counter, child_node))
                counter += 1
                
                # Actualizar cota global si este hijo tiene mejor upper_bound
                if child_node.upper_bound < cota_global:
                    cota_global = child_node.upper_bound
            else:
                # Este hijo no puede mejorar la mejor solución conocida
                nodes_pruned += 1
    
    # La cola se vació sin encontrar solución
    print(f"\n[Branch & Bound] ✗ No se encontró solución")
    return None