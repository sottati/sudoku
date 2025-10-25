"""
Archivo de utilidades para el solver de Sudoku
Aca deberia estar toda la logica de las funciones que se van a usar en la implementacion
"""

from random import randint, sample
from typing import Literal

# print fachero de la matriz
def print_matrix(matrix: list[list[int]]):
    # Línea superior
    print("┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓")
    
    for i in range(9):
        # Imprimir fila con valores
        row_str = "┃"
        for j in range(9):
            row_str += f"{matrix[i][j]:2d} "
            if j < 8:  # No es la última columna
                if (j + 1) % 3 == 0:
                    row_str += "┃"
                else:
                    row_str += "│"
            else:  # Última columna
                row_str += "┃"
        print(row_str)
        
        # Imprimir línea divisoria
        if i < 8:
            if (i + 1) % 3 == 0:
                # Línea gruesa entre submatrices 3x3
                print("┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫")
            else:
                # Línea delgada entre filas normales
                print("┠───┼───┼───╂───┼───┼───╂───┼───┼───┨")
    
    # Línea inferior
    print("┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛")

# retorna una matriz con diagonal aleatoria para generar un sudoku completo
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
    # 35-50
    if difficulty == 'easy':
        remove = randint(20, 35)
        return chooseCells(matrix, remove)
    # 22-34
    elif difficulty == 'medium':
        return chooseCells(matrix, randint(36, 46))
    # 10-21
    elif difficulty == 'hard':
        return chooseCells(matrix, randint(47, 57))

# inicializa la matriz con todos los valores en 0
# podriamos aca directamente ya popular la matriz? 
def initialize_matrix():
    return [[0 for _ in range(9)] for _ in range(9)]

def generateValues() -> list[int]:
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]

# los cuadrantes van de 0 a 8, el 0 es el cuadrante superior izquierdo, el 8 es el cuadrante inferior derecho
def returnCuadrante(row: int, col: int) -> int:
    cuadrante_row = row // 3
    cuadrante_col = col // 3
    
    return cuadrante_row * 3 + cuadrante_col

# podas implicitas
# chequeo por cuadrante
def checkCuadrante(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
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
    for i in range(9):
        if i == row:
            continue
        if matrix[i][col] == v:
            return False
    return True

# chequeo por fila
def checkRow(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    for i in range(9):
        if i == col:
            continue
        if matrix[row][i] == v:
            return False
    return True

def isFactible(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    return checkCuadrante(matrix, v, row, col) and checkCol(matrix, v, row, col) and checkRow(matrix, v, row, col)