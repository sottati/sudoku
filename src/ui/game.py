"""
Lógica de juego para modos manual y automático
"""
import time
import copy
import threading
from typing import Set, Tuple, Optional
from utils.utils import isFactible, makeDifficulty
from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branch_and_bound
from utils.counter import reset, get_count
from ui.terminal import get_key, clear_screen, print_sudoku
from ui.visualizer import SudokuVisualizer
from ui.dual_visualizer import DualVisualizer


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


def modo_automatico(difficulty: str, algorithm: str, enable_animation: bool = True):
    """Modo automático - resolver sudoku con algoritmo

    Args:
        difficulty: Nivel de dificultad ('easy', 'medium', 'hard')
        algorithm: Algoritmo a usar ('backtracking', 'bnb', 'both')
        enable_animation: Si True, muestra animación. Si False, solo métricas
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
        _resolver_backtracking(matrix, enable_animation)
    elif algorithm == 'bnb':
        _resolver_bnb(matrix, enable_animation)
    elif algorithm == 'both':
        _resolver_ambos(matrix, enable_animation)

    print("\n  Presiona cualquier tecla para continuar...")
    get_key()


def _resolver_backtracking(matrix: list[list[int]], enable_animation: bool = True):
    """Resuelve con backtracking y muestra resultados"""
    clear_screen()
    print("\n  RESOLVIENDO CON BACKTRACKING\n")

    # Guardar celdas originales
    original_cells: Set[Tuple[int, int]] = set()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                original_cells.add((i, j))

    # Crear visualizer para animación con aceleración progresiva
    visualizer = SudokuVisualizer(matrix, original_cells, enable_animation=enable_animation)

    # Dibujar tablero inicial
    if enable_animation:
        print_sudoku(matrix, original_cells=original_cells, show_instructions=False)

    matrix_bt = copy.deepcopy(matrix)
    reset('backtracking')

    time_start = time.time()
    matrix_solved = backtracking(matrix_bt, visualizer=visualizer)
    time_end = time.time()

    # Limpiar y mostrar resultado final
    clear_screen()
    print("\n  RESOLVIENDO CON BACKTRACKING\n")

    if matrix_solved:
        print("  ✅ Matriz resuelta:\n")
        print_sudoku(matrix_solved, show_instructions=False)
        print(f"\n  ⏱️  Tiempo: {time_end - time_start:.6f} segundos")
        print(f"  🔢 Intentos: {get_count('backtracking'):,}")
    else:
        print("  ❌ No se encontró solución")


def _resolver_bnb(matrix: list[list[int]], enable_animation: bool = True):
    """Resuelve con Branch and Bound y muestra resultados"""
    clear_screen()
    print("\n  RESOLVIENDO CON BRANCH AND BOUND\n")

    # Guardar celdas originales
    original_cells: Set[Tuple[int, int]] = set()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                original_cells.add((i, j))

    # Crear visualizer para animación con aceleración progresiva
    visualizer = SudokuVisualizer(matrix, original_cells, enable_animation=enable_animation)

    # Dibujar tablero inicial
    if enable_animation:
        print_sudoku(matrix, original_cells=original_cells, show_instructions=False)

    matrix_bnb = [row[:] for row in matrix]
    reset()

    time_start = time.time()
    matrix_solved = branch_and_bound(matrix_bnb, visualizer=visualizer)
    time_end = time.time()

    # Limpiar y mostrar resultado final
    clear_screen()
    print("\n  RESOLVIENDO CON BRANCH AND BOUND\n")

    if matrix_solved:
        print("  ✅ Matriz resuelta:\n")
        print_sudoku(matrix_solved, show_instructions=False)
        print(f"\n  ⏱️  Tiempo: {time_end - time_start:.6f} segundos")
        print(f"  🔢 Intentos: {get_count():,}")
    else:
        print("  ❌ No se encontró solución")


def _resolver_ambos(matrix: list[list[int]], enable_animation: bool = True):
    """Resuelve con ambos algoritmos simultáneamente y muestra comparación"""

    # Guardar celdas originales
    original_cells: Set[Tuple[int, int]] = set()
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                original_cells.add((i, j))

    # Crear dual visualizer solo si animación está activada
    dual_vis = None
    if enable_animation:
        clear_screen()
        print("\n  COMPARACIÓN EN TIEMPO REAL\n")
        dual_vis = DualVisualizer(matrix, original_cells, delay=0.003)
        dual_vis.initial_draw()
    else:
        clear_screen()
        print("\n  COMPARANDO ALGORITMOS (sin animación)...\n")

    # Variables compartidas para resultados
    results = {'bt': None, 'bnb': None}
    times = {'bt': 0.0, 'bnb': 0.0}
    attempts = {'bt': 0, 'bnb': 0}

    # Wrapper visualizer para Backtracking (izquierda)
    class LeftVisualizer:
        def __init__(self, dual_vis, start_time):
            self.dual_vis = dual_vis
            self.start_time = start_time

        def update(self, matrix, row, col, value):
            if self.dual_vis:
                elapsed = time.time() - self.start_time
                attempts_count = get_count('backtracking')
                self.dual_vis.update_left(matrix, row, col, elapsed, attempts_count)

        def backtrack(self, matrix, row, col):
            self.update(matrix, row, col, 0)

    # Wrapper visualizer para Branch & Bound (derecha)
    class RightVisualizer:
        def __init__(self, dual_vis, start_time):
            self.dual_vis = dual_vis
            self.start_time = start_time

        def update(self, matrix, row, col, value):
            if self.dual_vis:
                elapsed = time.time() - self.start_time
                attempts_count = get_count()
                self.dual_vis.update_right(matrix, row, col, elapsed, attempts_count)

        def backtrack(self, matrix, row, col):
            self.update(matrix, row, col, 0)

    # Thread para Backtracking
    def run_backtracking():
        matrix_bt = copy.deepcopy(matrix)
        reset('backtracking')

        time_start = time.time()
        left_vis = LeftVisualizer(dual_vis, time_start)
        result = backtracking(matrix_bt, visualizer=left_vis)
        time_end = time.time()

        results['bt'] = result
        times['bt'] = time_end - time_start
        attempts['bt'] = get_count('backtracking')
        if dual_vis:
            dual_vis.mark_completed('left')

    # Thread para Branch & Bound
    def run_bnb():
        matrix_bnb = copy.deepcopy(matrix)
        reset()

        time_start = time.time()
        right_vis = RightVisualizer(dual_vis, time_start)
        result = branch_and_bound(matrix_bnb, visualizer=right_vis)
        time_end = time.time()

        results['bnb'] = result
        times['bnb'] = time_end - time_start
        attempts['bnb'] = get_count()
        if dual_vis:
            dual_vis.mark_completed('right')

    # Ejecutar ambos en paralelo
    thread_bt = threading.Thread(target=run_backtracking)
    thread_bnb = threading.Thread(target=run_bnb)

    thread_bt.start()
    thread_bnb.start()

    thread_bt.join()
    thread_bnb.join()

    # Mostrar tabla comparativa final
    if enable_animation:
        time.sleep(1)  # Pausa para ver resultado final
    else:
        clear_screen()
    print("\n\n  COMPARACIÓN DE ALGORITMOS\n")
    print("  " + "="*60)
    print(f"  {'Algoritmo':<25} {'Tiempo (s)':<15} {'Intentos':<15}")
    print("  " + "="*60)
    print(f"  {'Backtracking':<25} {times['bt']:<15.6f} {attempts['bt']:<15,}")
    print(f"  {'Branch and Bound':<25} {times['bnb']:<15.6f} {attempts['bnb']:<15,}")
    print("  " + "="*60)

    # Determinar ganador
    if times['bt'] < times['bnb']:
        print("\n  🏆 Backtracking fue más rápido")
    elif times['bnb'] < times['bt']:
        print("\n  🏆 Branch and Bound fue más rápido")
    else:
        print("\n  🤝 Empate en tiempo")

    if attempts['bt'] < attempts['bnb']:
        print(f"  💡 Backtracking hizo menos intentos ({attempts['bt']:,} vs {attempts['bnb']:,})")
    elif attempts['bnb'] < attempts['bt']:
        print(f"  💡 Branch and Bound hizo menos intentos ({attempts['bnb']:,} vs {attempts['bt']:,})")
