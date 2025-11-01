"""
Lógica de juego para modos manual y automático
"""
import time
import copy
from typing import Set, Tuple, Optional
from utils.utils import isFactible, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branch_and_bound
from utils.counter import reset, get_count
from ui.terminal import get_key, clear_screen, print_sudoku


def validate_complete_solution(matrix: list[list[int]]) -> bool:
    """Valida que la solución del sudoku esté completa y sea correcta

    Args:
        matrix: Matriz 9x9 del sudoku

    Returns:
        bool: True si la solución es válida y completa
    """
    # Verificar que no haya celdas vacías
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
            # Verificar que cada celda sea válida
            if not isFactible(matrix, matrix[i][j], i, j):
                return False

    return True


def modo_manual(difficulty: str):
    """Modo de juego manual con input del usuario

    Args:
        difficulty: Nivel de dificultad ('easy', 'medium', 'hard')
    """
    # Generar sudoku
    print("\n  Generando sudoku...\n")
    base_matrix = iniciateBaseMatrix()
    matrix = makeDifficulty(base_matrix, difficulty)

    # Guardar celdas originales (no editables)
    original_cells: Set[Tuple[int, int]] = set()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                original_cells.add((i, j))

    # Copiar matriz para jugar
    game_matrix = [row[:] for row in matrix]

    # Posición del cursor
    cursor = (0, 0)
    error_message = None

    # Loop de juego
    clear_screen()
    while True:
        # Renderizar tablero
        print_sudoku(game_matrix, cursor, original_cells, error_message=error_message)

        # Leer tecla
        key = get_key()
        error_message = None  # Reset error

        # Navegación
        if key == 'UP' and cursor[0] > 0:
            cursor = (cursor[0] - 1, cursor[1])
        elif key == 'DOWN' and cursor[0] < 8:
            cursor = (cursor[0] + 1, cursor[1])
        elif key == 'LEFT' and cursor[1] > 0:
            cursor = (cursor[0], cursor[1] - 1)
        elif key == 'RIGHT' and cursor[1] < 8:
            cursor = (cursor[0], cursor[1] + 1)

        # Ingresar número 1-9
        elif key in '123456789':
            row, col = cursor
            # No permitir editar celdas originales
            if (row, col) in original_cells:
                error_message = "No puedes editar celdas originales"
            else:
                value = int(key)
                # Validar si el valor puede ir ahí
                if isFactible(game_matrix, value, row, col):
                    game_matrix[row][col] = value
                else:
                    error_message = f"El {value} no puede ir ahí (conflicto en fila/col/caja)"

        # Borrar (0)
        elif key == '0':
            row, col = cursor
            # No permitir borrar celdas originales
            if (row, col) in original_cells:
                error_message = "No puedes borrar celdas originales"
            else:
                game_matrix[row][col] = 0

        # Submit (s)
        elif key in 'sS':
            clear_screen()
            print("\n  Validando solución...\n")

            if validate_complete_solution(game_matrix):
                print("  ✅ ¡CORRECTO! Has resuelto el sudoku exitosamente.\n")
            else:
                print("  ❌ INCORRECTO. La solución tiene errores o está incompleta.\n")

            print_sudoku(game_matrix, original_cells=original_cells, show_instructions=False)
            print("\n  Presiona cualquier tecla para continuar...")
            get_key()
            return

        # Salir (q)
        elif key in 'qQ':
            return

        # Redibujar pantalla
        clear_screen()


def modo_automatico(difficulty: str, algorithm: str):
    """Modo automático - resolver sudoku con algoritmo

    Args:
        difficulty: Nivel de dificultad ('easy', 'medium', 'hard')
        algorithm: Algoritmo a usar ('backtracking', 'bnb', 'both')
    """
    # Generar sudoku
    print("\n  Generando sudoku...\n")
    base_matrix = iniciateBaseMatrix()
    matrix = makeDifficulty(base_matrix, difficulty)

    # Mostrar sudoku inicial
    clear_screen()
    print("\n  SUDOKU A RESOLVER\n")

    # Calcular celdas vacías
    empty_cells = sum(1 for i in range(9) for j in range(9) if matrix[i][j] == 0)

    # Guardar celdas originales para visualización
    original_cells: Set[Tuple[int, int]] = set()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                original_cells.add((i, j))

    print_sudoku(matrix, original_cells=original_cells, show_instructions=False)
    print(f"\n  📊 Celdas vacías: {empty_cells}/81")
    print(f"  📊 Dificultad: {difficulty.upper()}")

    print("\n  Presiona cualquier tecla para resolver...")
    get_key()

    # Resolver según algoritmo
    if algorithm == 'backtracking':
        _resolver_backtracking(matrix)
    elif algorithm == 'bnb':
        _resolver_bnb(matrix)
    elif algorithm == 'both':
        _resolver_ambos(matrix)

    print("\n  Presiona cualquier tecla para continuar...")
    get_key()


def _resolver_backtracking(matrix: list[list[int]]):
    """Resuelve con backtracking y muestra resultados"""
    clear_screen()
    print("\n  RESOLVIENDO CON BACKTRACKING\n")

    matrix_bt = copy.deepcopy(matrix)
    reset('backtracking')

    time_start = time.time()
    matrix_solved = backtracking(matrix_bt)
    time_end = time.time()

    if matrix_solved:
        print("  ✅ Matriz resuelta:\n")
        print_sudoku(matrix_solved, show_instructions=False)
        print(f"\n  ⏱️  Tiempo: {time_end - time_start:.6f} segundos")
        print(f"  🔢 Intentos: {get_count('backtracking'):,}")
    else:
        print("  ❌ No se encontró solución")


def _resolver_bnb(matrix: list[list[int]]):
    """Resuelve con Branch and Bound y muestra resultados"""
    clear_screen()
    print("\n  RESOLVIENDO CON BRANCH AND BOUND\n")

    matrix_bnb = [row[:] for row in matrix]
    reset()

    time_start = time.time()
    matrix_solved = branch_and_bound(matrix_bnb)
    time_end = time.time()

    if matrix_solved:
        print("  ✅ Matriz resuelta:\n")
        print_sudoku(matrix_solved, show_instructions=False)
        print(f"\n  ⏱️  Tiempo: {time_end - time_start:.6f} segundos")
        print(f"  🔢 Intentos: {get_count():,}")
    else:
        print("  ❌ No se encontró solución")


def _resolver_ambos(matrix: list[list[int]]):
    """Resuelve con ambos algoritmos y muestra comparación"""
    # Resolver con Backtracking
    matrix_bt = copy.deepcopy(matrix)
    reset('backtracking')

    time_start_bt = time.time()
    matrix_solved_bt = backtracking(matrix_bt)
    time_end_bt = time.time()
    time_bt = time_end_bt - time_start_bt
    intentos_bt = get_count('backtracking')

    # Resolver con Branch and Bound
    matrix_bnb = [row[:] for row in matrix]
    reset()

    time_start_bnb = time.time()
    matrix_solved_bnb = branch_and_bound(matrix_bnb)
    time_end_bnb = time.time()
    time_bnb = time_end_bnb - time_start_bnb
    intentos_bnb = get_count()

    # Mostrar comparación
    clear_screen()
    print("\n  COMPARACIÓN DE ALGORITMOS\n")
    print("  " + "="*60)
    print(f"  {'Algoritmo':<25} {'Tiempo (s)':<15} {'Intentos':<15}")
    print("  " + "="*60)
    print(f"  {'Backtracking':<25} {time_bt:<15.6f} {intentos_bt:<15,}")
    print(f"  {'Branch and Bound':<25} {time_bnb:<15.6f} {intentos_bnb:<15,}")
    print("  " + "="*60)

    # Determinar ganador
    if time_bt < time_bnb:
        print("\n  🏆 Backtracking fue más rápido")
    elif time_bnb < time_bt:
        print("\n  🏆 Branch and Bound fue más rápido")
    else:
        print("\n  🤝 Empate en tiempo")

    if intentos_bt < intentos_bnb:
        print(f"  💡 Backtracking hizo menos intentos ({intentos_bt:,} vs {intentos_bnb:,})")
    elif intentos_bnb < intentos_bt:
        print(f"  💡 Branch and Bound hizo menos intentos ({intentos_bnb:,} vs {intentos_bt:,})")

    # Mostrar una de las soluciones
    if matrix_solved_bt:
        print("\n  Solución encontrada:\n")
        print_sudoku(matrix_solved_bt, show_instructions=False)
