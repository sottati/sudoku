# Sudoku GUI

Interfaz gráfica en Tkinter para jugar o resolver un Sudoku.

## Requisitos
- Python 3.10+

## Cómo ejecutar

En Windows PowerShell (desde la carpeta del repositorio):

```powershell
python .\src\main.py
```

Si no tenés Python en el PATH, instalalo desde https://www.python.org/downloads/ y asegurate de marcar "Add python.exe to PATH" durante la instalación.

## Funcionalidades
- Elegí la dificultad: easy, medium o hard.
- Elegí entre jugar o resolver automáticamente.
- Auto-resolver muestra dos soluciones: Backtracking y Branch & Bound, con tiempo e intentos.
– En modo juego:
  - Tablero con celdas fijas bloqueadas.
  - Sólo permite ingresar dígitos 1-9.
  - Sin sistema de vidas: si te equivocás, sólo se limpia la celda y podés intentar de nuevo.

## Notas
- La generación de tableros usa un Sudoku resuelto por backtracking y luego oculta celdas según la dificultad.
- Los contadores de intentos provienen de `utils/counter.py`. Backtracking usa el contador `backtracking` y Branch & Bound usa el contador por defecto.
