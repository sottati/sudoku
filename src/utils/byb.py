# Branch and Bound
# Hay que definir las cotas, definir estrategias etc etc etc
# dejo escrito el pseudocodigo igual q en backtracking

# Algoritmo Backtracking como en la diapo
from queue import PriorityQueue
from typing import Set
from utils.utils import isFactible
from utils.counter import increment

# Quiero implementar una solucion de sudoku utilizando branch and bound y tomando de heuristica para podar que siempre busque 
# el nodo con menor cantidad de opciones disponibles. Quiero que la cota inferior sea el minimo de opciones disponibles y la
#  cota superior sea el minimo entre: mayor cantidad de valores disponibles por nodo o por maxima cantidad de veces que aparece 
# un valor en el tablero de los disponibles para ese nodo

# Cota inferior: minimo de opciones disponibles
# Cota superior: min(minOpcionesDisponibles, maxVecesQueApareceUnValor)

# dado fila, columna y cuadrante para una celda, genera los valores posibles utilizando conjuntos
def generatePosibleValues(S: list[list[int]], row: int, col: int) -> Set[int]:
    # conjunto con los valores que hay en esa fila
    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en esa columna
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en ese cuadrante
    v_cuadrante: Set[int] = {S[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if S[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}

    # conjunto con los valores posibles para esa celda
    return {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante

# no se si usar este PriorityQueue o una lista de nodos, por ahora lo dejo como PriorityQueue
# se almacena la cota, la celda y los valores posibles en el nodo
def iniciarColaDePrioridad(S: list[list[int]]) -> PriorityQueue[tuple[int, tuple[int, int, set[int]]]]:
    cola: PriorityQueue[tuple[int, tuple[int, int, set[int]]]] = PriorityQueue()
    for i in range(9):
        for j in range(9):
            if S[i][j] != 0:
                cota = calcularCotaInferior(S, i, j)
                # cota, celda y valores posibles
                cola.put((cota, (i, j, generatePosibleValues(S, i, j))))

    return cola

# cota inferior: cantidad de opciones disponibles por nodo a poner
def calcularCotaInferior(S: list[list[int]], row: int, col: int) -> int:
    # conjunto con los valores que hay en esa fila
    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en esa columna
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en ese cuadrante
    v_cuadrante: Set[int] = {S[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if S[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}

    candidatos: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante
    return len(candidatos) # size() es el numero de elementos en el conjunto

# Faltan podas por heuristica

def podar(nodo: tuple[int, tuple[int, int, set[int]]]) -> bool:
    return False

def branchAndBound(S: list[list[int]]) -> list[list[int]]:
    E = 0
    lim = 0
    ENV = iniciarColaDePrioridad(S)
    # ENV.put(0, 0) # agregar nodo raiz ???
    

    # Saltar los numeros ya llenados (diagonal al crear y numeros ya dados en el q hay q resolver)
    # if S[row][col] != 0:
    #     return branchAndBound(S, E + 1)

    while not ENV.empty():
        nodo = ENV.get() # saca un nodo de la cola de prioridad, el primero de la cola
        print(f"Nodo: {nodo}")
        if podar(nodo) == False:
            print("Poda exitosa")
        else:
            print("Poda fallida")

        
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

    
                        