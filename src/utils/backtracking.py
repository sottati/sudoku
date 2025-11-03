from typing import Optional
from utils.utils import generateValues, initialize_matrix, isFactible, populate_matrix
from utils.counter import increment

# Algoritmo Backtracking: resuelve el sudoku llenando celdas válidas y retrocediendo cuando es necesario
def backtracking(board: list[list[int]], cell_index: int = 0) -> Optional[list[list[int]]]:
    # Caso base: recorrimos todas las celdas
    if cell_index == 81:
        return board

    row, col = divmod(cell_index, 9)

    # Saltar celdas ya completadas (diagonal inicial y pistas del puzzle)
    if board[row][col] != 0:
        return backtracking(board, cell_index + 1)

    candidates = generateValues()
    for value in candidates:
        board[row][col] = value
        increment('backtracking')
        if isFactible(board, value, row, col):
            result = backtracking(board, cell_index + 1)
            if result is not None:  # Se encontró una solución válida aguas abajo
                return result
        # Retroceder si no funcionó
        board[row][col] = 0
    return None  # Ningún candidato funcionó en esta celda

# Genera un sudoku resuelto a partir de la diagonal aleatoria
def iniciateBaseMatrix() -> list[list[int]]:
    base_matrix = initialize_matrix()
    base_matrix = populate_matrix(base_matrix)
    base_matrix = backtracking(base_matrix)
    return base_matrix 