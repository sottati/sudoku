# Branch and Bound
# Hay que definir las cotas, definir estrategias etc etc etc
# dejo escrito el pseudocodigo igual q en backtracking

# Algoritmo Backtracking como en la diapo
from queue import PriorityQueue
from typing import Set
from utils import isFactible
from counter import increment

sudoku_prueba: list[list[int]] = [
    [0, 0, 0, 4, 0, 0, 0, 8, 0],
    [0, 5, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 4, 0, 3, 7, 5, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 7, 8],
    [0, 6, 8, 0, 1, 2, 0, 0, 5],
    [0, 7, 9, 8, 6, 0, 0, 2, 1],
    [0, 0, 0, 3, 9, 8, 0, 6, 7],
    [0, 0, 0, 5, 0, 1, 9, 3, 0],
    [0, 0, 0, 0, 7, 4, 8, 0, 0]
]

# Quiero implementar una solucion de sudoku utilizando branch and bound y tomando de heuristica para podar que siempre busque 
# el nodo con menor cantidad de opciones disponibles. Quiero que la cota inferior sea el minimo de opciones disponibles y la
#  cota superior sea el minimo entre: mayor cantidad de valores disponibles por nodo o por maxima cantidad de veces que aparece 
# un valor en el tablero de los disponibles para ese nodo

# Cota inferior: minimo de opciones disponibles
# Cota superior: min(minOpcionesDisponibles, maxVecesQueApareceUnValor)

class NodoSudoku:
    """representa un nodo en el arbol de busqueda"""
    def __init__(self, fila: int, columna: int, valores_posibles: Set[int], 
                 cota_inferior: int, tablero: list[list[int]] = None):
        self.fila = fila
        self.columna = columna
        self.valores_posibles = valores_posibles
        self.cota_inferior = cota_inferior
        # self.cota_superior = cota_superior
        self.tablero = tablero  # Opcional: para guardar el estado completo
    
    def __lt__(self, other):
        """Para PriorityQueue: menor cota = mayor prioridad"""
        if self.cota_inferior != other.cota_inferior:
            return self.cota_inferior < other.cota_inferior
        if self.fila != other.fila:
            return self.fila < other.fila
        return self.columna < other.columna
    
    def __str__(self):
        return f"Nodo(fila={self.fila}, col={self.columna}, cota inferior={self.cota_inferior}, opciones={len(self.valores_posibles)})"

# diccionario para contar la cantidad de veces que aparece cada valor en el tablero
freq_values: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

def is_complete(matrix: list[list[int]]) -> bool:
    """verifica si el sudoku está completamente resuelto"""
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True

def generatePosibleValues(S: list[list[int]], row: int, col: int) -> Set[int]:
    """dado fila, columna y cuadrante para una celda, genera los valores posibles utilizando conjuntos"""
    # conjunto con los valores que hay en esa fila
    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en esa columna
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en ese cuadrante
    v_cuadrante: Set[int] = {S[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if S[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}

    # conjunto con los valores posibles para esa celda
    return {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante

# no se si usar este PriorityQueue o una lista de nodos, por ahora lo dejo como PriorityQueue
def iniciarColaDePrioridad(S: list[list[int]]) -> PriorityQueue[NodoSudoku]:
    """
    se almacena la cota, la celda y los valores posibles en el nodo
    """
    cola: PriorityQueue[NodoSudoku] = PriorityQueue()
    for i in range(9):
        for j in range(9):
            if S[i][j] == 0:
                cota = calcularCotaInferior(S, i, j)
                # cota, celda y valores posibles
                nodo = NodoSudoku(i, j, generatePosibleValues(S, i, j), cota, S)
                # cola.put((cota, nodo))
                cola.put(nodo)
            # si el valor no es 0, se agrega a la frecuencia de valores
            else:
                freq_values[S[i][j]] += 1

    return cola

def generarHijos(nodo: NodoSudoku) -> list[NodoSudoku]:
    """genera los hijos del nodo"""
    hijos: list[NodoSudoku] = []
    for valor in nodo.valores_posibles:
        hijos.append(NodoSudoku(nodo.fila, nodo.columna, {valor}, nodo.cota_inferior, nodo.tablero))
    return hijos

def calcularCotaInferior(S: list[list[int]], row: int, col: int) -> int:
    """cota inferior: cantidad de opciones disponibles por nodo a poner"""
    # conjunto con los valores que hay en esa fila
    v_fila: Set[int] = {S[row][col] for col in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en esa columna
    v_col: Set[int] = {S[row][col] for row in range(9) if S[row][col] != 0} 
    # conjunto con los valores que hay en ese cuadrante
    v_cuadrante: Set[int] = {S[(row // 3) * 3 + i][(col // 3) * 3 + j] for i in range(3) for j in range(3) if S[(row // 3) * 3 + i][(col // 3) * 3 + j] != 0}

    candidatos: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9} - v_fila - v_col - v_cuadrante

    return len(candidatos) # cantidad de opciones disponibles para esa celda

# Faltan podas por heuristica

def podar(nodo: tuple[int, tuple[int, int, set[int]]]) -> bool:
    """podar si no hay valores posibles para esa celda"""
    if len(nodo.valores_posibles) == 0:
        return True
    return False

def branchAndBound(S: list[list[int]]) -> list[list[int]]:
    cola = iniciarColaDePrioridad(S)
    nodo_raiz = NodoSudoku(0, 0, generatePosibleValues(S, 0, 0), calcularCotaInferior(S, 0, 0), S)
    cola.put(nodo_raiz)
    cota = calcularCotaInferior(S, 0, 0)
    lim = 0 # mejor solucion parcial
    
    while not cola.empty():
        nodo = cola.get() # saca un nodo de la cola de prioridad, el primero de la cola
        print(f"Nodo: {nodo}")
        if not podar(nodo):
            if esSolucion(nodo):
            print("Poda exitosa")
        else:
            print("Poda fallida")
  
    return None  # Ningún valor funcionó


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

# test para ejecutar el branch and bound con la matriz de prueba
branchAndBound(sudoku_prueba)
print(freq_values)