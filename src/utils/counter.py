"""
Módulo para contar intentos en la resolución de Sudoku
Útil para comparar la eficiencia de diferentes algoritmos
"""

_count = 0


def increment():
    """
    Incrementa el contador en 1.
    Se llama cada vez que se intenta colocar un valor en una celda.
    """
    global _count
    _count += 1


def get_count():
    """
    Obtiene el valor actual del contador.
    
    Returns:
        int: Número de intentos realizados
    """
    return _count


def reset():
    """
    Reinicia el contador a 0.
    Se debe llamar antes de resolver un nuevo sudoku.
    """
    global _count
    _count = 0