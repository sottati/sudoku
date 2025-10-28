# Branch and Bound
# Hay que definir las cotas, definir estrategias etc etc etc
# dejo escrito el pseudocodigo igual q en backtracking

# Algoritmo Backtracking como en la diapo
from typing import Set


def branchAndBound(S: list[list[int]], E = 0) -> list[list[int]]:
    if E == 81:
        return S
    row, col = E // 9, E % 9

    # Saltar los numeros ya llenados (diagonal al crear y numeros ya dados en el q hay q resolver)
    if S[row][col] != 0:
        return branchAndBound(S, E + 1)

    valores: Set[int] = {x for x in range(1, 10)}

    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0}
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0}
    v_cuadrante: Set[int] = set[int]()

    values = generateValuesBy()
    for v in values:
        S[row][col] = v
        if isFactible(S, v, row, col):
            resultado = branchAndBound(S, E + 1)
            if resultado is not None:  # verifica q el resultado no sea None, si es None, no se devuelve nada
                return resultado
        S[row][col] = 0
    return None  # Ningún valor funcionó

def generateValuesBy(matrix: list[list[int]], row: int, col: int) -> Set[int]:
    return True

def checkCuadrante(matrix: list[list[int]], v: int, row: int, col: int) -> bool:
    cuadrante_row = (row // 3) * 3
    cuadrante_col = (col // 3) * 3

    cuadrante: Set[int]

    for i in range(3):
        for j in range(3):
            cuadrante.add(matrix[cuadrante_row + i][cuadrante_col + j])

    
            
    return cuadrante

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

# def branchAndBound():
#     env = inicializarEstructura()
#     nodoRaiz = crearNodoRaiz()
#     agregar(env, nodoRaiz)
#     cota = actualizarCota(cota, nodoRaiz)
#     mejorSolucion = null
#     while env !== vacio: # este vacio tenemos q definir q seria, si long = 0 o un conjunto vacio, ni idea
#         nodo = primero(env)
#         if !podar(nodo, cota):
#             hijos = generarHijos(nodo)
#             for hijo in hijos:
#                 if !podar(hijo, cota):
#                     if esSolucion(hijo):
#                         if esMejor(mejorSolucion, hijo):
#                             mejorSolucion = hijo
#                             cota = actualizarCota(cota, hijo)
#                         else:
#                             agregar(env, hijo)
#                             cota = actualizarCota(cota, hijo)

    
                        