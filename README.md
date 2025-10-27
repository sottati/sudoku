# Solver de Sudoku (Python)

Un generador y resolutor de Sudoku en Python con dos algoritmos:
- Backtracking (`bt`)
- Branch-and-Bound (`bb`) con heurística MRV y una cola de prioridad

Este repositorio usa `src/` como directorio de trabajo.

## Inicio rápido

Ejemplos en Windows PowerShell con el intérprete configurado:

```powershell
cd .\src
# Backtracking, puzzle fácil
C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe main.py --solver bt --difficulty easy

# Branch-and-Bound, puzzle medio, semilla fija para reproducibilidad
C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe main.py --solver bb --difficulty medium --seed 42
```

Sugerencia: para bordes Unicode bonitos en consolas Windows, ejecuta esto una vez por sesión:
```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
```

## Tests

Compara ambos solvers sobre el mismo puzzle generado:
```powershell
cd .\src
C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe tests.py --difficulty medium --seed 123
```

## Benchmark

Mide el tiempo promedio de resolución para uno o ambos solvers sobre múltiples puzzles:
```powershell
cd .\src
# Both solvers, 5 runs, medium difficulty, reproducible seed
C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe benchmark.py --solver both --difficulty medium --runs 5 --seed 123
```

La salida muestra media, p50 y p90 aproximado.

También se reportan “nodos explorados” por solver:
- Backtracking: cantidad de intentos de asignación (colocar un valor en una celda vacía).
- Branch-and-Bound: cantidad de estados expandidos (pops del heap) y nodos generados internamente.
 
Ejemplo de resultados y reflexión: consulta `REPORT.md` en la raíz del repo.

## Estructura

- `src/main.py` — demo de CLI con `--solver {bt,bb}`, `--difficulty` y `--seed` opcional.
- `src/tests.py` — prueba simple que verifica que ambos solvers produzcan la misma solución.
- `src/benchmark.py` — script de medición de tiempos para uno o ambos solvers.
- `src/utils/utils.py` — utilidades: impresión (`print_matrix` con fallback ASCII), inicialización, selección de dificultad, chequeos de factibilidad, `set_seed`.
- `src/utils/backtracking.py` — solver de backtracking e `iniciateBaseMatrix`.
- `src/utils/byb.py` — solver Branch-and-Bound (MRV + frontera con heap).

## Guía del código

- Representación y convenciones (ver `src/utils/utils.py`):
	- Tablero = `list[list[int]]` 9x9, con 0 para celdas vacías.
	- Índices `row`, `col` en 0..8. Cuadrantes 0..8 según `(row//3)*3 + (col//3)`.
	- `print_matrix` intenta Unicode; si la consola no lo soporta, usa ASCII.
- Generación de base y puzzles:
	- `iniciateBaseMatrix()` crea una solución completa partiendo de la diagonal principal aleatoria y completando por backtracking.
	- `makeDifficulty(matrix, 'easy'|'medium'|'hard')` vacía celdas para crear un puzzle (no garantiza unicidad de solución).
- Solvers:
	- Backtracking (`src/utils/backtracking.py`):
		- Recorre la grilla con índice lineal `E` (0..80) ⇒ fila = `E//9`, col = `E%9`.
		- Intenta 1..9 y usa `isFactible` (fila/col/cuadrante) para podar.
		- Docstring incluye diagrama de flujo, complejidad y casos límite.
	- Branch-and-Bound (`src/utils/byb.py`):
		- Heurística MRV (celda con menos candidatos), expande hijos por candidato.
		- Frontera con `heapq`: costo = celdas vacías (menos es mejor).
		- Docstring incluye diagrama del ciclo, complejidad y casos límite.
- Reproducibilidad:
	- `set_seed(seed)` fija la semilla del RNG global para tener puzzles repetibles.

## Análisis sugerido

Para replicar el análisis de eficiencia solicitado en la consigna:
- Tiempo y nodos por dificultad creciente:
	```powershell
	cd .\src
	# 10 corridas por solver, dificultad fácil/medio/difícil
	C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe benchmark.py --solver both --difficulty easy --runs 10 --seed 123
	C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe benchmark.py --solver both --difficulty medium --runs 10 --seed 123
	C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe benchmark.py --solver both --difficulty hard --runs 10 --seed 123
	```
- Ejecución única con métricas desde CLI:
	```powershell
	cd .\src
	C:\Users\hok\AppData\Local\Programs\Python\Python313\python.exe main.py --solver bb --difficulty medium --seed 42 --metrics
	```

Sugerencia de reflexión: observa cómo B&B típicamente reduce el número de nodos respecto de backtracking
al priorizar celdas más restringidas (MRV) y al podar estados sin candidatos, especialmente a medida que
el número de celdas vacías (mayor dificultad) crece.

## Notas

- La dificultad se aplica quitando entradas de una base totalmente resuelta (`makeDifficulty` con literales `easy|medium|hard`).
- La utilidad `set_seed` asegura puzzles reproducibles entre ejecuciones.
- Ejecuta desde el directorio `src/` (los imports asumen `from utils...`).
