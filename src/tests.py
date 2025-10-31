from utils import print_matrix, initialize_matrix, populate_matrix 

def printCuadrante(cuadrante: list[list[int]]):
    for i in range(3):
        for j in range(3):
            print(cuadrante[i][j], end=" ")
        print()
    

cuadrante_test = [[0 for _ in range(3)] for _ in range(3)]

cuadrante_test[0][0] = 1
cuadrante_test[1][1] = 3
cuadrante_test[2][2] = 2


def tests():
    printCuadrante(cuadrante_test)

tests()