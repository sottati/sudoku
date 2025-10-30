from utils.utils import print_matrix, makeDifficulty, initialize_matrix, populate_matrix
from utils.backtracking import backtracking
from utils.byb import branch_and_bound
import time

def main():
    # Generar sudoku base COMPLETO
    print("Generando sudoku base...")
    base_matrix = initialize_matrix()
    base_matrix = populate_matrix(base_matrix)
    base_matrix_solved = backtracking(base_matrix)
    
    print("Sudoku completo generado:")
    print_matrix(base_matrix_solved)
    
    # Crear sudoku con dificultad (eliminar celdas)
    matrix = makeDifficulty(base_matrix_solved, "hard")
    print("\nSudoku a resolver (dificultad: hard):")
    print_matrix(matrix)
    
    # Resolver con Backtracking
    print("\n" + "="*50)
    print("RESOLVIENDO CON BACKTRACKING")
    print("="*50)
    matrix_bt = [row[:] for row in matrix]  # Copia del sudoku INCOMPLETO
    start = time.time()
    matrix_solved_bt = backtracking(matrix_bt)
    time_bt = time.time() - start
    print(f"Tiempo: {time_bt:.6f} segundos")
    if matrix_solved_bt:
        print_matrix(matrix_solved_bt)
    else:
        print("No se encontró solución")
    
    # Resolver con Branch and Bound
    print("\n" + "="*50)
    print("RESOLVIENDO CON BRANCH AND BOUND")
    print("="*50)
    matrix_byb = [row[:] for row in matrix]  # Copia del sudoku INCOMPLETO
    start = time.time()
    matrix_solved_byb = branch_and_bound(matrix_byb)
    time_byb = time.time() - start
    print(f"Tiempo: {time_byb:.6f} segundos")
    if matrix_solved_byb:
        print_matrix(matrix_solved_byb)
    else:
        print("No se encontró solución")
    
    # Comparación (solo si ambos encontraron solución)
    if matrix_solved_bt and matrix_solved_byb:
        print("\n" + "="*50)
        print("COMPARACIÓN DE TIEMPOS")
        print("="*50)
        print(f"Backtracking:       {time_bt:.6f} segundos")
        print(f"Branch & Bound:     {time_byb:.6f} segundos")
        if time_byb > 0:
            speedup = time_bt / time_byb
            print(f"Speedup:            {speedup:.2f}x")
        
        # Verificar que ambas soluciones son iguales
        if matrix_solved_bt == matrix_solved_byb:
            print("\n✓ Ambas soluciones son idénticas")
        else:
            print("\n⚠ Las soluciones son diferentes")

if __name__ == "__main__":
    main()