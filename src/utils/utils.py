"""
Utilidades comunes para el proyecto de Sudoku.

Resumen de responsabilidades de este módulo:
- Representación de tableros (matrices 9x9 de enteros) y operaciones básicas.
- Impresión de la matriz con bordes "bonitos" (Unicode) o ASCII como respaldo.
- Generación de la diagonal principal aleatoria para construir una solución base.
- Creación de puzzles a partir de una solución completa (distintas dificultades).
- Comprobaciones de factibilidad (fila, columna, cuadrante) usadas por los solvers.
- Control opcional de aleatoriedad vía set_seed para reproducibilidad.

Convenciones:
- La matriz es lista de 9 listas, cada una con 9 ints (0..9). El 0 representa celda vacía.
- Índices: row y col van de 0..8. Cuadrantes: 0..8 (3x3), calculados por división entera.

Mapa de cuadrantes (índices 0..8):

    +-----+-----+-----+
    |  0  |  1  |  2  |
    +-----+-----+-----+
    |  3  |  4  |  5  |
    +-----+-----+-----+
    |  6  |  7  |  8  |
    +-----+-----+-----+

Cada cuadrante es una submatriz 3x3; p.ej., (row=4, col=7) -> cuadrante 5.
"""

from random import randint, sample
import random
from typing import Literal
import sys

# print fachero de la matriz
def print_matrix(matrix: list[list[int]]):
    """Imprime la matriz con bordes Unicode si la consola lo soporta; si no, usa ASCII.

    Notas sobre Windows: muchas consolas usan cp1252 por defecto y no soportan box-drawing
    characters. En ese caso se cae a un trazado ASCII para evitar UnicodeEncodeError.
    """

    def supports_unicode_box() -> bool:
        enc = sys.stdout.encoding or "utf-8"
        try:
            "┏".encode(enc)
            return True
        except Exception:
            return False

    if supports_unicode_box():
        TL, TR, BL, BR = "┏", "┓", "┗", "┛"
        V, v = "┃", "│"
        H3, H1 = "━━━", "───"
        TJ3, TJ1, CJ, BJ3 = "┳", "┯", "╂", "┻"
        X3, X1, MX = "╋", "┿", "┠"
        # Líneas
        top = TL + (H3 + TJ1 + H3 + TJ1 + H3 + TJ3 + H3 + TJ1 + H3 + TJ1 + H3 + TJ3 + H3 + TJ1 + H3 + TJ1 + H3) + TR
        mid_thin = "┠" + (H1 + "┼" + H1 + "┼" + H1 + CJ + H1 + "┼" + H1 + "┼" + H1 + CJ + H1 + "┼" + H1 + "┼" + H1) + "┨"
        mid_thick = "┣" + (H3 + X1 + H3 + X1 + H3 + X3 + H3 + X1 + H3 + X1 + H3 + X3 + H3 + X1 + H3 + X1 + H3) + "┫"
        bottom = BL + ("━━━" + "┷" + "━━━" + "┷" + "━━━" + BJ3 + "━━━" + "┷" + "━━━" + "┷" + "━━━" + BJ3 + "━━━" + "┷" + "━━━" + "┷" + "━━━") + BR

        print(top)
        for i in range(9):
            row_str = V
            for j in range(9):
                row_str += f"{matrix[i][j]:2d} "
                if j < 8:
                    row_str += (V if (j + 1) % 3 == 0 else v)
                else:
                    row_str += V
            print(row_str)
            if i < 8:
                print(mid_thick if (i + 1) % 3 == 0 else mid_thin)
        print(bottom)
    else:
        # ASCII fallback
        def ascii_sep():
            print("+---+---+---+---+---+---+---+---+---+")

        ascii_sep()
        for i in range(9):
            row_str = "|"
            for j in range(9):
                row_str += f"{matrix[i][j]:2d} |"
            print(row_str)
            ascii_sep()

# Retorna una matriz con diagonal principal aleatoria para iniciar un sudoku completo.
# Idea: si llenamos las 3 subcuadrículas de la diagonal (3x3) con permutaciones válidas,
# el backtracking posterior encuentra más rápido una solución completa.
def populate_matrix(matrix: list[list[int]]):
    list = [[],[],[]]
    for i in range(3):
        for j in range(3):
            num = randint(1, 9)
            while num in list[i]:
                num = randint(1, 9)
            list[i].append(num)
    
    fil_col = 0
    for i in range(3):
        for j in range(3):
            matrix[fil_col][fil_col] = list[i][j]
            fil_col += 1

    return matrix

def chooseCells(matrix: list[list[int]], cells: int):
    """Elimina 'cells' celdas (si existen) seleccionadas al azar.

    - Sólo se eliminan celdas que actualmente no son 0 (para mantener la cantidad pedida).
    - Se modifica la matriz IN-PLACE y se retorna la misma referencia por conveniencia.
    """
    # Crear lista de todas las posiciones con números
    filled_cells = []
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                filled_cells.append((i, j))
    
    # sample elige elementos aleatorios sin repeticion de una lista, set o conjunto
    # min es para que no se elijan mas celdas que las que hay
    cells_to_remove = sample(filled_cells, min(cells, len(filled_cells)))
    
    # vaciar las celdas elegidas
    for row, col in cells_to_remove:
        matrix[row][col] = 0
    
    return matrix

def makeDifficulty(matrix: list[list[int]], difficulty: Literal['easy', 'medium', 'hard']):
    """Vacía celdas para crear un puzzle con una dificultad aproximada.

    Advertencia: los rangos están calibrados empíricamente y no garantizan unicidad de solución.
    - easy: deja más pistas (quita menos celdas)
    - medium / hard: quita más celdas
    """
    # Comentarios originales indicaban 35-50 pistas, pero aquí usamos cantidades a remover.
    if difficulty == 'easy':
        remove = randint(20, 35)
        return chooseCells(matrix, remove)
    # medium: remueve más celdas
    elif difficulty == 'medium':
        return chooseCells(matrix, randint(36, 46))
    # hard: remueve todavía más
    elif difficulty == 'hard':
        return chooseCells(matrix, randint(47, 57))

# inicializa la matriz con todos los valores en 0
# podriamos aca directamente ya popular la matriz? 
def initialize_matrix():
    """Crea una matriz 9x9 llena de ceros (tablero vacío)."""
    return [[0 for _ in range(9)] for _ in range(9)]

def generateValues() -> list[int]:
    """Devuelve los candidatos básicos 1..9 en orden fijo.

    Podríamos barajarlos para mayor aleatoriedad, pero mantener orden estable
    hace más fácil reproducir ejecuciones (y B&B ya decide el orden de expansión).
    """
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]

# los cuadrantes van de 0 a 8, el 0 es el cuadrante superior izquierdo, el 8 es el cuadrante inferior derecho
def returnCuadrante(row: int, col: int) -> int:
    """Devuelve el id de cuadrante 0..8 para la celda (row, col).

    Fórmula: (row // 3) * 3 + (col // 3)

    Ejemplo visual:
        row // 3 => {0,1,2} para filas 0..2, 3..5, 6..8
        col // 3 => {0,1,2} para columnas 0..2, 3..5, 6..8
        cuadrante_id = 3*(row//3) + (col//3)
    """
    cuadrante_row = row // 3
    cuadrante_col = col // 3
    
    return cuadrante_row * 3 + cuadrante_col

# podas implicitas
# chequeo por cuadrante
def checkCuadrante(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    """Verifica que 'v' no se repita en el cuadrante 3x3 correspondiente a (row, col)."""
    cuadrante_id = (row // 3) * 3 + (col // 3)
    cuadrante_row = (row // 3) * 3
    cuadrante_col = (col // 3) * 3

    for i in range(3):
        for j in range(3):
            actual_row = cuadrante_row + i
            actual_col = cuadrante_col + j
            if actual_row == row and actual_col == col:
                continue
            if matrix[actual_row][actual_col] == v:
                return False
    return True

# chequeo por columna
def checkCol(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    """Verifica que 'v' no se repita en la columna 'col' (ignorando la celda actual)."""
    for i in range(9):
        if i == row:
            continue
        if matrix[i][col] == v:
            return False
    return True

# chequeo por fila
def checkRow(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    """Verifica que 'v' no se repita en la fila 'row' (ignorando la celda actual)."""
    for i in range(9):
        if i == col:
            continue
        if matrix[row][i] == v:
            return False
    return True

def isFactible(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    """Regresa True si 'v' puede colocarse en (row, col) sin violar reglas de Sudoku."""
    return checkCuadrante(matrix, v, row, col) and checkCol(matrix, v, row, col) and checkRow(matrix, v, row, col)


def set_seed(seed: int | None):
    """Fija la semilla del generador aleatorio para reproducibilidad (None para aleatorio).

    Afecta tanto a randint() como a sample() ya que ambas usan el RNG global de random.
    """
    random.seed(seed)