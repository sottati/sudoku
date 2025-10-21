from utils import print_matrix

# Algoritmo Backtracking como en la diapo
def backtracking(S: list[list[int]], E: int):
    values = generateValues()
    for v in values:
        add(S, E, v)
        if factible(S):
            if isSolution(S):
                print_matrix(S)
            else:
                backtracking(S, E + 1)
        pop(S, E)

