"""
Archivo de utilidades para el solver de Sudoku
Aca deberia estar toda la logica de las funciones que se van a usar en la implementacion
"""

from random import randint
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

# Habria que definir cual es la mejor forma de popular la matriz de entrada, si con todos 1 si con nums
# del 1 al 9 con alguna heuristica o con numeros aleatorios
def populate_matrix(matrix: list[list[int]]):
    for i in range(9):
        for j in range(9):
            matrix[i][j] = randint(1, 9)
    return matrix

def populate_with_dificulty(matrix: list[list[int]], difficulty: Literal['easy', 'medium', 'hard']):
    # 35-50
    if difficulty == 'easy':
        return matrix
    # 22-34
    elif difficulty == 'medium':
        return matrix
    # 10-21
    elif difficulty == 'hard':
        return matrix

# inicializa la matriz con todos los valores en 0
# podriamos aca directamente ya popular la matriz? 
def initialize_matrix():
    return [[0 for _ in range(9)] for _ in range(9)]
