"""
Visualizador para animación de algoritmos de resolución
"""
import time
import sys
from typing import Set, Tuple
from ui.terminal import print_sudoku


class SudokuVisualizer:
    """Visualizador para animar la resolución del Sudoku en tiempo real

    Attributes:
        current_matrix: Estado actual del tablero
        original_cells: Set de celdas originales (no editables)
        initial_delay: Delay inicial (más lento)
        min_delay: Delay mínimo (límite de aceleración)
        acceleration_factor: Factor de reducción del delay cada iteración
        current_delay: Delay actual que disminuye con cada update
        num_lines: Número de líneas que ocupa el tablero en terminal
    """

    def __init__(self, initial_matrix: list[list[int]], original_cells: Set[Tuple[int, int]],
                 initial_delay: float = 0.15, min_delay: float = 0.00001, acceleration_factor: float = 0.98,
                 enable_acceleration: bool = True, enable_animation: bool = True):
        """
        Args:
            initial_matrix: Matriz inicial del sudoku
            original_cells: Set de tuplas (row, col) de celdas originales
            initial_delay: Delay inicial en segundos (default: 0.15 = 150ms, bien lento)
            min_delay: Delay mínimo en segundos (default: 0.0001 = 0.1ms)
            acceleration_factor: Factor de multiplicación del delay (default: 0.98)
                                 Valores menores = acelera más rápido
            enable_acceleration: Si True, acelera progresivamente. Si False, delay fijo
            enable_animation: Si True, muestra animación. Si False, no renderiza (métricas reales)
        """
        self.current_matrix = [row[:] for row in initial_matrix]
        self.original_cells = original_cells
        self.initial_delay = initial_delay
        self.min_delay = min_delay
        self.acceleration_factor = acceleration_factor if enable_acceleration else 1.0
        self.current_delay = initial_delay
        self.enable_acceleration = enable_acceleration
        self.enable_animation = enable_animation
        # Líneas del tablero:
        # 1 header + 11 filas (9 + 2 separadores) + 1 footer = 13
        # + 1 blank (\n en posición) + 1 línea posición = 15
        # Subir 14 para volver a línea 1 (desde línea 15)
        self.num_lines = 14

    def update(self, matrix: list[list[int]], row: int, col: int, value: int):
        """Actualiza y renderiza el tablero con la nueva celda

        Args:
            matrix: Matriz actualizada
            row: Fila de la celda modificada
            col: Columna de la celda modificada
            value: Valor asignado a la celda
        """
        self.current_matrix = [r[:] for r in matrix]

        if not self.enable_animation:
            return

        # Subir cursor al inicio del tablero
        print(f"\033[{self.num_lines}A\r", end="", flush=True)

        # Redibujar tablero con cursor en celda actual
        print_sudoku(self.current_matrix, cursor=(row, col), original_cells=self.original_cells, show_instructions=False)

        sys.stdout.flush()
        time.sleep(self.current_delay)

        # Acelerar progresivamente
        self.current_delay = max(self.min_delay, self.current_delay * self.acceleration_factor)

    def backtrack(self, matrix: list[list[int]], row: int, col: int):
        """Animación cuando se hace backtrack (resetea celda a 0)

        Args:
            matrix: Matriz actualizada
            row: Fila de la celda reseteada
            col: Columna de la celda reseteada
        """
        self.update(matrix, row, col, 0)

    def reset_speed(self):
        """Reinicia el delay a su valor inicial"""
        self.current_delay = self.initial_delay
