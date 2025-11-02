"""
Visualizador dual para comparación simultánea de dos algoritmos
"""
import time
import sys
import threading
from typing import Set, Tuple, Optional


class DualVisualizer:
    """Visualiza dos algoritmos resolviendo el mismo sudoku simultáneamente

    Attributes:
        matrix_left: Estado tablero izquierdo (Backtracking)
        matrix_right: Estado tablero derecho (Branch & Bound)
        original_cells: Celdas originales del sudoku
        delay: Delay fijo entre actualizaciones
        time_left: Tiempo transcurrido algoritmo izquierdo
        time_right: Tiempo transcurrido algoritmo derecho
        attempts_left: Intentos algoritmo izquierdo
        attempts_right: Intentos algoritmo derecho
        completed_left: Si algoritmo izquierdo terminó
        completed_right: Si algoritmo derecho terminó
        lock: Lock para thread safety
    """

    def __init__(self, initial_matrix: list[list[int]], original_cells: Set[Tuple[int, int]], delay: float = 0.005):
        """
        Args:
            initial_matrix: Matriz inicial del sudoku
            original_cells: Set de celdas originales
            delay: Delay fijo en segundos (default: 0.005 = 5ms)
        """
        self.matrix_left = [row[:] for row in initial_matrix]
        self.matrix_right = [row[:] for row in initial_matrix]
        self.original_cells = original_cells
        self.delay = delay

        self.cursor_left: Optional[Tuple[int, int]] = None
        self.cursor_right: Optional[Tuple[int, int]] = None

        self.time_left = 0.0
        self.time_right = 0.0
        self.attempts_left = 0
        self.attempts_right = 0

        self.completed_left = False
        self.completed_right = False

        self.lock = threading.Lock()

        # Número de líneas totales: títulos + tablero + métricas
        # 1 títulos + 13 líneas tablero + 1 métricas = 15
        self.num_lines = 15

    def update_left(self, matrix: list[list[int]], row: int, col: int, elapsed_time: float, attempts: int):
        """Actualiza tablero izquierdo (Backtracking)"""
        with self.lock:
            self.matrix_left = [r[:] for r in matrix]
            self.cursor_left = (row, col)
            self.time_left = elapsed_time
            self.attempts_left = attempts
            self._redraw()

    def update_right(self, matrix: list[list[int]], row: int, col: int, elapsed_time: float, attempts: int):
        """Actualiza tablero derecho (Branch & Bound)"""
        with self.lock:
            self.matrix_right = [r[:] for r in matrix]
            self.cursor_right = (row, col)
            self.time_right = elapsed_time
            self.attempts_right = attempts
            self._redraw()

    def mark_completed(self, side: str):
        """Marca un algoritmo como completado

        Args:
            side: 'left' o 'right'
        """
        with self.lock:
            if side == 'left':
                self.completed_left = True
            elif side == 'right':
                self.completed_right = True
            self._redraw()

    def _redraw(self):
        """Redibuja ambos tableros lado a lado"""
        # Subir cursor al inicio
        print(f"\033[{self.num_lines}A\r", end="", flush=True)

        # Títulos
        left_title = "BACKTRACKING"
        right_title = "BRANCH & BOUND"
        print(f"  {left_title:<25}    {right_title:<25}\033[K")

        # Imprimir tableros lado a lado
        self._print_dual_boards()

        # Métricas
        left_status = "✅ Completado" if self.completed_left else "⏳ Resolviendo"
        right_status = "✅ Completado" if self.completed_right else "⏳ Resolviendo"

        metrics_left = f"⏱  {self.time_left:6.2f}s | 🔢 {self.attempts_left:,}"
        metrics_right = f"⏱  {self.time_right:6.2f}s | 🔢 {self.attempts_right:,}"

        print(f"  {metrics_left:<25}    {metrics_right:<25}\033[K", end="", flush=True)

        sys.stdout.flush()
        time.sleep(self.delay)

    def _print_dual_boards(self):
        """Imprime dos tableros sudoku lado a lado"""
        # Header
        header = "╔═══════╤═══════╤═══════╗"
        print(f"  {header}      {header}\033[K")

        for i in range(9):
            # Separadores horizontales
            if i == 3 or i == 6:
                sep = "╟───────┼───────┼───────╢"
                print(f"  {sep}      {sep}\033[K")

            # Construir ambas filas
            left_line = self._build_row(self.matrix_left, i, self.cursor_left, self.original_cells)
            right_line = self._build_row(self.matrix_right, i, self.cursor_right, self.original_cells)

            print(f"  {left_line}      {right_line}\033[K")

        # Footer
        footer = "╚═══════╧═══════╧═══════╝"
        print(f"  {footer}      {footer}\033[K")

    def _build_row(self, matrix: list[list[int]], row_idx: int, cursor: Optional[Tuple[int, int]],
                   original_cells: Set[Tuple[int, int]]) -> str:
        """Construye una fila del tablero sudoku"""
        line = "║"
        for j in range(9):
            if j == 3 or j == 6:
                line += " │"

            val = matrix[row_idx][j]
            is_original = (row_idx, j) in original_cells
            is_cursor = cursor == (row_idx, j)

            if val == 0:
                char = "·"
            else:
                char = str(val)

            # Aplicar estilo con espacios
            if is_cursor:
                line += f" \033[7m{char}\033[0m "  # Invertido
            elif is_original:
                line += f" \033[1m{char}\033[0m "  # Bold
            else:
                line += f" {char} "

        line += "║"
        return line

    def initial_draw(self):
        """Dibuja el estado inicial de ambos tableros"""
        print("\033[K")  # Blank line

        left_title = "BACKTRACKING"
        right_title = "BRANCH & BOUND"
        print(f"  {left_title:<25}    {right_title:<25}")

        self._print_dual_boards()

        metrics_left = f"⏱  {self.time_left:6.2f}s | 🔢 {self.attempts_left:,}"
        metrics_right = f"⏱  {self.time_right:6.2f}s | 🔢 {self.attempts_right:,}"

        print(f"  {metrics_left:<25}    {metrics_right:<25}", end="", flush=True)
