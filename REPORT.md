# Análisis de rendimiento: Backtracking vs Branch-and-Bound

Este informe resume resultados empíricos al comparar los resolutores implementados para Sudoku.

- Entorno: Windows, Python 3.13
- Parámetros: 10 corridas por dificultad, `seed=123`
- Métricas: tiempo de resolución (segundos) y nodos explorados (según instrumentación en cada solver)

## Resultados

### easy
- Backtracking
  - Tiempo: mean=0.0002s, p50=0.0002s, p90≈0.0003s
  - Nodos: mean=160, p50=148, max=240
- Branch-and-Bound
  - Tiempo: mean=0.0021s, p50=0.0018s, p90≈0.0042s
  - Nodos: mean=29, p50=30, max=36

Observación: B&B explora muchas menos posiciones, pero su sobrecosto fijo (MRV + heap + copias) hace que sea más lento en tableros fáciles.

### medium
- Backtracking
  - Tiempo: mean=0.0019s, p50=0.0008s, p90≈0.0095s
  - Nodos: mean=1453, p50=604, max=6810
- Branch-and-Bound
  - Tiempo: mean=0.0120s, p50=0.0129s, p90≈0.0186s
  - Nodos: mean=44, p50=44, max=52

Observación: B&B mantiene muy pocos nodos y una varianza baja, pero el tiempo medio resultó mayor que BT en este set (sobrecosto domina). Aun así, BT muestra colas pesadas (picos mucho mayores).

### hard
- Backtracking
  - Tiempo: mean=0.0434s, p50=0.0065s, p90≈0.3306s
  - Nodos: mean=36,703, p50=5,392, max=311,741
- Branch-and-Bound
  - Tiempo: mean=0.0252s, p50=0.0263s, p90≈0.0322s
  - Nodos: mean=60, p50=56, max=87

Observación: En difícil la heurística MRV + poda por cota es muy efectiva: B&B explora órdenes de magnitud menos nodos y además es más rápido y estable. Backtracking muestra explosiones combinatorias en algunos casos (varianza alta y máximos muy grandes).

## Conclusiones
- El costo fijo de B&B (selección MRV, manejo de frontera en heap y copias de matriz) puede dominar en puzzles fáciles; BT suele ganar en tiempo allí, aunque expanda más nodos.
- A medida que aumenta la dificultad, B&B reduce drásticamente los nodos explorados y se vuelve competitivo o superior en tiempo, además de mucho más estable (menor varianza y sin outliers tan grandes).
- Para una herramienta robusta, B&B es preferible en juegos medianos/difíciles; para casos triviales, BT puro es suficiente y más rápido.

## Cómo reproducir
Desde `src/`:

```powershell
# Comparar ambos solvers en cada dificultad (10 corridas, semilla fija)
python -Xutf8 benchmark.py --solver both --difficulty easy --runs 10 --seed 123
python -Xutf8 benchmark.py --solver both --difficulty medium --runs 10 --seed 123
python -Xutf8 benchmark.py --solver both --difficulty hard --runs 10 --seed 123

# Ejecutar demo con métricas
python -Xutf8 main.py --solver bb --difficulty hard --seed 42 --metrics
```

Notas:
- Los números exactos pueden variar por CPU/SO, pero las tendencias deberían mantenerse.
- La métrica "nodos" en BT cuenta intentos de asignación; en B&B cuenta expansiones de estados (pops del heap) y se reporta `nodes`.
