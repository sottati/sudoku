"""
Utilidades para interfaz de terminal con termios
"""
import sys
import tty
import termios
from typing import Tuple, Set, Optional


def get_key() -> str:
    """Lee una tecla sin necesidad de presionar Enter

    Returns:
        str: Tecla presionada ('UP', 'DOWN', 'LEFT', 'RIGHT', o caracter)
    """
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        # Detectar flechas (escape sequences)
        if key == '\x1b':
            next1 = sys.stdin.read(1)
            next2 = sys.stdin.read(1)
            if next1 == '[':
                if next2 == 'A': return 'UP'
                if next2 == 'B': return 'DOWN'
                if next2 == 'C': return 'RIGHT'
                if next2 == 'D': return 'LEFT'
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def clear_screen():
    """Limpia la pantalla de la terminal"""
    print("\033[2J\033[H", end="")


def _draw_menu(title: str, options: list[str], current: int):
    """Dibuja el menú en la posición actual del cursor

    Args:
        title: Título del menú
        options: Lista de opciones
        current: Índice de la opción seleccionada
    """
    print("\033[K")  # blank line (clear + implicit newline)
    print(f"{title}\033[K")
    print("\033[K")  # blank line

    for idx, opt in enumerate(options):
        prefix = "→" if idx == current else " "
        print(f"  {prefix} {opt}\033[K")

    print("\033[K")  # blank line
    print("↑/↓: navegar | Enter: seleccionar\033[K", end="", flush=True)


def menu(title: str, options: list[str]) -> int:
    """Menú interactivo con navegación por flechas

    Args:
        title: Título del menú
        options: Lista de opciones

    Returns:
        int: Índice de la opción seleccionada
    """
    current = 0
    num_lines = len(options) + 5  # blank + title + blank + opciones + blank + instrucciones

    # Guardar posición del cursor y dibujar primera vez
    print("\033[s", end="")  # Save cursor position
    _draw_menu(title, options, current)

    while True:
        key = get_key()

        if key == 'UP' and current > 0:
            current -= 1
        elif key == 'DOWN' and current < len(options) - 1:
            current += 1
        elif key in ['\r', '\n']:  # Enter
            # Restaurar posición y limpiar menú
            print("\033[u", end="")  # Restore cursor
            for _ in range(num_lines):
                print("\033[K")
            print(f"\033[{num_lines}A", end="")  # Volver arriba
            return current
        else:
            continue

        # Restaurar posición del cursor y redibujar
        print("\033[u", end="")  # Restore cursor position
        _draw_menu(title, options, current)


def print_sudoku(matrix: list[list[int]],
                cursor: Optional[Tuple[int, int]] = None,
                original_cells: Optional[Set[Tuple[int, int]]] = None,
                show_instructions: bool = True,
                error_message: Optional[str] = None):
    """Imprime el tablero de Sudoku con formato

    Args:
        matrix: Matriz 9x9 del sudoku
        cursor: Tupla (row, col) de la posición del cursor
        original_cells: Set de tuplas (row, col) de celdas originales (no editables)
        show_instructions: Si mostrar instrucciones
        error_message: Mensaje de error opcional
    """
    if original_cells is None:
        original_cells = set()

    print("  ╔═══════╤═══════╤═══════╗")

    for i in range(9):
        if i == 3 or i == 6:
            print("  ╟───────┼───────┼───────╢")

        line = "  ║"
        for j in range(9):
            if j == 3 or j == 6:
                line += " │"

            val = matrix[i][j]
            is_original = (i, j) in original_cells
            is_cursor = cursor == (i, j)

            # Formatear celda
            if val == 0:
                char = "·"
            else:
                char = str(val)

            # Aplicar estilo según tipo de celda
            if is_cursor:
                # Cursor actual (invertido)
                line += f" \033[7m{char}\033[0m"
            elif is_original:
                # Celda original (bold)
                line += f" \033[1m{char}\033[0m"
            else:
                # Celda editable
                line += f" {char}"

        line += " ║"
        print(line)

    print("  ╚═══════╧═══════╧═══════╝")

    if cursor is not None:
        print(f"\n  Posición: ({cursor[0]+1}, {cursor[1]+1})", end="", flush=True)

    if show_instructions:
        print("\n  ⌨  Flechas: navegar | 1-9: ingresar | 0: borrar | s: submit | q: salir")

    if error_message:
        print(f"\n  ❌ {error_message}")
