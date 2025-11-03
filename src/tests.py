from utils.counter import reset, get_count
from time import time
from utils.backtracking import backtracking, iniciateBaseMatrix
from utils.byb import branch_and_bound
from utils.utils import makeDifficulty 
import copy
import pandas as pd
from datetime import datetime


difficulty_levels = ["easy", "medium", "hard"]
implementaciones = {
    "backtracking": ("backtracking", backtracking),
    "branch_and_bound": ("default", branch_and_bound)
}

base_matrix = iniciateBaseMatrix()

# Generar 100 matrices por dificultad
matrices_por_dificultad = {}
for difficulty in difficulty_levels:
    matrices_por_dificultad[difficulty] = []
    for i in range(100):
        matriz = makeDifficulty(copy.deepcopy(base_matrix), difficulty)
        matrices_por_dificultad[difficulty].append(copy.deepcopy(matriz))

# Lista para almacenar todos los resultados
todos_resultados = []
resultados_promedios = []

# Ejecutar tests
for difficulty in difficulty_levels:
    print("\n" + "="*70)
    print(f"DIFICULTAD: {difficulty.upper()}")
    print("="*70)
    
    for impl_name, (counter_id, impl_func) in implementaciones.items():
        print("\n" + "-"*70)
        print(f"IMPLEMENTACIÓN: {impl_name.upper()}")
        print("-"*70)
        
        total_time = 0
        total_nodes = 0
        
        for i, matriz in enumerate(matrices_por_dificultad[difficulty]):
            reset(counter_id)
            matrix_copy = copy.deepcopy(matriz)
            
            start_time = time()
            impl_func(matrix_copy)
            end_time = time()
            
            execution_time = end_time - start_time
            nodes = get_count(counter_id)
            
            total_time += execution_time
            total_nodes += nodes
            
            # Guardar resultado individual
            todos_resultados.append({
                'Dificultad': difficulty,
                'Implementación': impl_name,
                'Test': i + 1,
                'Tiempo (s)': execution_time,
                'Nodos': nodes
            })
            
            print(f"Test {i+1:3d} | Tiempo: {execution_time:.6f}s | Nodos: {nodes:,}")
        
        # Guardar promedios
        resultados_promedios.append({
            'Dificultad': difficulty,
            'Implementación': impl_name,
            'Tiempo Promedio (s)': total_time/100,
            'Nodos Promedio': total_nodes/100,
            'Tiempo Total (s)': total_time,
            'Nodos Totales': total_nodes
        })
        
        print("-"*70)
        print(f"PROMEDIOS ({impl_name.upper()}):")
        print(f"Tiempo promedio: {total_time/100:.6f}s")
        print(f"Nodos promedio: {total_nodes/100:,.0f}")
        print(f"Tiempo total: {total_time:.2f}s")
        print(f"Nodos totales: {total_nodes:,}")
        print("-"*70)
    
    print("\n" + "="*70)

# Crear DataFrames
df_detallado = pd.DataFrame(todos_resultados)
df_promedios = pd.DataFrame(resultados_promedios)

# Exportar a Excel con múltiples hojas
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"resultados_sudoku_{timestamp}.xlsx"

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    df_detallado.to_excel(writer, sheet_name='Resultados Detallados', index=False)
    df_promedios.to_excel(writer, sheet_name='Promedios', index=False)

print(f"\n✅ Resultados exportados a: {filename}")