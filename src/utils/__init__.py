"""Paquete utils: re-exporta funciones clave para uso conveniente en el resto del proyecto.

Advertencia: mantener este archivo sincronizado con los nombres definidos en utils/*.py
para evitar ExportErrors. Si se renombra una función pública, revisar __all__ aquí.
"""

from .utils import *
from .backtracking import iniciateBaseMatrix, backtracking
from .byb import branchAndBound

# Exportar símbolos clave y corregir entradas inexistentes
__all__ = [
	# utils.py
	'print_matrix', 'initialize_matrix', 'populate_matrix', 'makeDifficulty',
	'chooseCells', 'generateValues', 'isFactible', 'returnCuadrante', 'set_seed',
	'checkRow', 'checkCol', 'checkCuadrante',
	# backtracking.py
	'iniciateBaseMatrix', 'backtracking',
	# byb.py
	'branchAndBound',
]
