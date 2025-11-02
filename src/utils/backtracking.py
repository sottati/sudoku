from utils.utils import generateValues, initialize_matrix, isFactible, populate_matrix
from utils.counter import increment

# Algoritmo Backtracking como en la diapo
def backtracking(S: list[list[int]], E = 0, visualizer = None) -> list[list[int]]:
    if E == 81:
        return S
    row, col = E // 9, E % 9

    # Saltar los numeros ya llenados (diagonal al crear y numeros ya dados en el q hay q resolver)
    if S[row][col] != 0:
        return backtracking(S, E + 1, visualizer)

    values = generateValues()
    for v in values:
        S[row][col] = v
        increment('backtracking')

        if visualizer:
            visualizer.update(S, row, col, v)

        if isFactible(S, v, row, col):
            resultado = backtracking(S, E + 1, visualizer)
            if resultado is not None:  # verifica q el resultado no sea None, si es None, no se devuelve nada
                return resultado

        S[row][col] = 0
        if visualizer:
            visualizer.backtrack(S, row, col)

    return None  # Ningún valor funcionó

# sudoku resuelto a partir de la diagonal aleatoria
def iniciateBaseMatrix():
    base_matrix = initialize_matrix()
    base_matrix = populate_matrix(base_matrix)
    base_matrix = backtracking(base_matrix)
    return base_matrix