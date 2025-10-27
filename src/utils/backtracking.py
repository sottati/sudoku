from utils.utils import generateValues, initialize_matrix, isFactible, populate_matrix


def backtracking(S: list[list[int]], E: int = 0, metrics: dict | None = None) -> list[list[int]] | None:
    """Resuelve el Sudoku por backtracking puro.

    Parámetros:
    - S: matriz 9x9 con 0 en las celdas vacías (se modifica IN-PLACE durante la búsqueda).
    - E: índice lineal 0..80 que recorre la matriz en orden fila-major.

    Flujo (diagrama simplificado):
        E -> (row = E // 9, col = E % 9)
        ├─ si S[row][col] != 0: backtracking(S, E+1)
        └─ si S[row][col] == 0:
             para v en 1..9:
               S[row][col] = v
               si isFactible(S, v, row, col):
                   r = backtracking(S, E+1)
                   si r != None: return r
               S[row][col] = 0
             return None

    Complejidad (aprox.):
    - Peor caso exponencial en 9x9, pero con las podas de fila/col/cuadrante funciona bien.
    - Promedio depende de cuántas celdas vacías haya y de la dispersión de candidatos.

    Casos límite:
    - Sudoku ya completo (E==81 de entrada) -> retorna S.
    - Sudoku insatisfactible -> retorna None.
    - Tableros con múltiples soluciones -> retorna la primera que encuentra según orden 1..9.
    """
    # Métricas opcionales: contar llamadas recursivas
    if metrics is not None:
        metrics["calls"] = metrics.get("calls", 0) + 1

    if E == 81:
        return S

    row, col = E // 9, E % 9  # Mapeo lineal -> (fila, columna)

    # Saltar los números ya llenados (diagonal al crear y números dados del puzzle)
    if S[row][col] != 0:
        return backtracking(S, E + 1, metrics)

    # Probar candidatos en orden 1..9
    for v in generateValues():
        # Métricas opcionales: contar intentos de asignación (nodos expandidos)
        if metrics is not None:
            metrics["nodes"] = metrics.get("nodes", 0) + 1
        S[row][col] = v
        if isFactible(S, v, row, col):
            resultado = backtracking(S, E + 1, metrics)
            if resultado is not None:
                return resultado
        # Deshacer si no funciona
        S[row][col] = 0

    # Ningún valor funcionó para esta celda
    return None


def iniciateBaseMatrix() -> list[list[int]]:
    """Construye una solución completa de Sudoku para usar como base.

    Pasos:
    1) Crear matriz vacía.
    2) Popular la diagonal principal con números aleatorios válidos por subcuadrícula.
    3) Completar el resto con backtracking.

    Devuelve: una matriz 9x9 resuelta.
    """
    base_matrix = initialize_matrix()
    base_matrix = populate_matrix(base_matrix)
    base_matrix = backtracking(base_matrix)
    return base_matrix