#!/usr/bin/env python3
import sys
import tty
import termios

def get_key():
    """Lee una tecla sin Enter"""
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

def print_board(board, row, col):
    """Imprime tablero con indicador de posición"""
    print("="*25 + "\033[K")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("  " + "-"*21 + "\033[K")

        line = " "
        for j in range(9):
            if j % 3 == 0:
                line += " | " if j > 0 else " "

            val = str(board[i][j]) if board[i][j] != 0 else "·"

            # Marcar posición actual
            if i == row and j == col:
                line += f"[{val}]"
            else:
                line += f" {val} "

        print(line + "\033[K")

    print("="*25 + "\033[K")
    print(f"  Pos: ({row+1},{col+1}) | 1-9: num | 0: borrar | q: salir" + "\033[K")

def menu(options):
    """Menú interactivo que retorna índice seleccionado"""
    current = 0
    num_lines = len(options) + 3  # Opciones + título + separador + info

    print("\n=== MENÚ ===\n")

    first = True
    while True:
        if not first:
            # Subir para redibujar
            print(f"\033[{num_lines}A\r", end="")
        first = False

        print("=== MENÚ ===" + "\033[K")
        print("\033[K")  # Línea vacía

        for idx, opt in enumerate(options):
            if idx == current:
                print(f"  > {opt} <" + "\033[K")
            else:
                print(f"    {opt}" + "\033[K")

        print("\033[K")
        print("↑/↓: navegar | Enter: seleccionar" + "\033[K", end="")

        key = get_key()

        if key == 'UP' and current > 0:
            current -= 1
        elif key == 'DOWN' and current < len(options) - 1:
            current += 1
        elif key in ['\r', '\n']:  # Enter
            print(f"\n\nSeleccionaste: {options[current]}\n")
            return current

def main():
    board = [[0 for _ in range(9)] for _ in range(9)]
    row, col = 0, 0

    # options = ["Jugar Sudoku", "Ver instrucciones", "Configuración", "Salir"]
    # selected = menu(options)
    # print(f"Opción {selected}: {options[selected]}")

    # first_draw = True
    # while True:
    #     if not first_draw:
    #         # Mover cursor arriba 14 líneas para redibujar
    #         print("\033[14A\r", end="")
    #     first_draw = False

    #     print_board(board, row, col)

    #     key = get_key()

    #     # Navegación
    #     if key == 'UP' and row > 0:
    #         row -= 1
    #     elif key == 'DOWN' and row < 8:
    #         row += 1
    #     elif key == 'LEFT' and col > 0:
    #         col -= 1
    #     elif key == 'RIGHT' and col < 8:
    #         col += 1

    #     # Números 1-9
    #     elif key in '123456789':
    #         board[row][col] = int(key)

    #     # Borrar
    #     elif key == '0':
    #         board[row][col] = 0

    #     # Salir
    #     elif key in 'qQ':
    #         break

    # print("\n\nMatriz final:")
    # for row_data in board:
    #     print(row_data)
    # print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrumpido\n")
