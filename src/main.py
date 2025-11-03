"""
Interfaz gráfica de Sudoku con selección de dificultad y modo (jugar o auto-resolver).

Reglas de juego:
- No se marcan aciertos/errores.
- Sólo se permiten valores 1-9 válidos según el estado actual (fila/columna/cuadrante).
- Las celdas fijas no se pueden editar.
"""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import font as tkfont
from typing import Literal, Callable

from utils.backtracking import iniciateBaseMatrix, backtracking
from utils.byb import branch_and_bound
from utils.counter import reset, get_count
from utils.utils import makeDifficulty, isFactible


Difficulty = Literal["easy", "medium", "hard"]


class SudokuGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sudoku")
        self.resizable(False, False)

        # Fuentes (tamaño aumentado)
        self.font_title = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_subtitle = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.font_label = tkfont.Font(family="Segoe UI", size=13)
        self.font_button = tkfont.Font(family="Segoe UI", size=12)
        self.font_cell = tkfont.Font(family="Segoe UI", size=18)
        self.font_result_cell = tkfont.Font(family="Segoe UI", size=14)

        # Estado del juego
        self.difficulty: Difficulty = "easy"
        self.solution: list[list[int]] | None = None
        self.puzzle: list[list[int]] | None = None
        self.fixed: list[list[bool]] | None = None
        
        # Estado de animación
        self.animation_running = False
        self.animation_speed = 50  # ms entre pasos

        # Frames principales
        self.frame_start = tk.Frame(self, padx=16, pady=16)
        self.frame_board = tk.Frame(self, padx=16, pady=16)
        self.frame_results = tk.Frame(self, padx=16, pady=16)
        self.frame_animated = tk.Frame(self, padx=16, pady=16)

        # Construcción de pantallas
        self._build_start_screen()
        self._build_board_screen()
        self._build_results_screen()
        self._build_animated_screen()

        # Mostrar inicio
        self._show_frame(self.frame_start)

    # -------- Pantallas --------
    def _show_frame(self, frame: tk.Frame):
        for f in (self.frame_start, self.frame_board, self.frame_results, self.frame_animated):
            f.pack_forget()
        frame.pack()

    def _build_start_screen(self):
        tk.Label(self.frame_start, text="Elegí dificultad y modo", font=self.font_title).pack(pady=(0, 10))
        self.diff_var = tk.StringVar(value="easy")
        for value, text in ("easy", "Fácil"), ("medium", "Medio"), ("hard", "Difícil"):
            tk.Radiobutton(self.frame_start, text=text, value=value, variable=self.diff_var, font=self.font_label).pack(anchor="w")
        btns = tk.Frame(self.frame_start)
        btns.pack(pady=(12, 0))
        tk.Button(btns, text="Jugar", width=18, command=self._start_play, font=self.font_button).pack(side="left", padx=6)
        tk.Button(btns, text="Resolver automáticamente", width=22, command=self._start_auto, font=self.font_button).pack(side="left", padx=6)
        tk.Button(btns, text="Ver animación", width=18, command=self._start_animated, font=self.font_button).pack(side="left", padx=6)

    def _build_board_screen(self):
        # Cabecera
        top = tk.Frame(self.frame_board)
        top.pack(fill="x")
        self.label_info = tk.Label(top, text="", font=self.font_label)
        self.label_info.pack(side="left")
        tk.Button(top, text="Reiniciar", command=self._restart_play, font=self.font_button).pack(side="right", padx=6)
        tk.Button(top, text="Volver", command=lambda: self._show_frame(self.frame_start), font=self.font_button).pack(side="right")

        # Tablero 9x9
        grid = tk.Frame(self.frame_board, bd=2, relief="groove", padx=4, pady=4)
        grid.pack(pady=8)

        self.entries: list[list[tk.Entry]] = [[None for _ in range(9)] for _ in range(9)]  # type: ignore
        self.widget_to_pos: dict[str, tuple[int, int]] = {}
        self.pending_clear: dict[tuple[int, int], str] = {}

        for r in range(9):
            for c in range(9):
                e = tk.Entry(grid, width=2, justify="center", font=self.font_cell)
                e.grid(row=r, column=c,
                       padx=(0 if c % 3 != 0 else 6, 3),
                       pady=(0 if r % 3 != 0 else 6, 3),
                       ipadx=4, ipady=4)
                if ((r // 3) + (c // 3)) % 2 == 0:
                    e.configure(bg="#f7f7f7")
                self.entries[r][c] = e
                # Validación de dígitos por celda
                vcmd = (self.register(self._validate_input_cell), "%P", "%d", "%W")
                e.configure(validate="key", validatecommand=vcmd)
                self.widget_to_pos[str(e)] = (r, c)
                # Comprobación contextual post-input
                e.bind("<KeyRelease>", lambda ev, rr=r, cc=c: self._on_cell_key(ev, rr, cc))

    def _build_results_screen(self):
        tk.Label(self.frame_results, text="Resultados de Auto-Resolución", font=self.font_title).pack(pady=(0, 10))

        container = tk.Frame(self.frame_results)
        container.pack()

        self.panel_bt = self._create_result_panel(container, "Backtracking")
        self.panel_bt.pack(side="left", padx=10)

        self.panel_bnb = self._create_result_panel(container, "Branch & Bound")
        self.panel_bnb.pack(side="left", padx=10)

        tk.Button(self.frame_results, text="Volver", command=lambda: self._show_frame(self.frame_start), font=self.font_button).pack(pady=(10, 0))

    def _build_animated_screen(self):
        """Construye la pantalla de animación"""
        # Título
        tk.Label(self.frame_animated, text="Resolución Animada", font=self.font_title).pack(pady=(0, 10))
        
        # Controles superiores
        controls = tk.Frame(self.frame_animated)
        controls.pack(pady=8)
        
        self.anim_algo_var = tk.StringVar(value="backtracking")
        tk.Label(controls, text="Algoritmo:", font=self.font_label).pack(side="left", padx=5)
        tk.Radiobutton(controls, text="Backtracking", value="backtracking", 
                      variable=self.anim_algo_var, font=self.font_label).pack(side="left")
        tk.Radiobutton(controls, text="Branch & Bound", value="bnb", 
                      variable=self.anim_algo_var, font=self.font_label).pack(side="left")
        
        # Control de velocidad
        speed_frame = tk.Frame(self.frame_animated)
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="Velocidad:", font=self.font_label).pack(side="left", padx=5)
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=500, orient="horizontal", 
                                    length=200, command=self._update_speed)
        self.speed_scale.set(50)
        self.speed_scale.pack(side="left")
        tk.Label(speed_frame, text="ms", font=self.font_label).pack(side="left")
        
        # Tablero animado
        grid = tk.Frame(self.frame_animated, bd=2, relief="groove", padx=4, pady=4)
        grid.pack(pady=8)
        
        self.anim_cells: list[list[tk.Label]] = []
        for r in range(9):
            row_cells: list[tk.Label] = []
            for c in range(9):
                lbl = tk.Label(grid, text="", width=2, font=self.font_cell, 
                             relief="solid", bd=1)
                lbl.grid(row=r, column=c,
                        padx=(0 if c % 3 != 0 else 6, 2),
                        pady=(0 if r % 3 != 0 else 6, 2),
                        ipadx=4, ipady=4)
                if ((r // 3) + (c // 3)) % 2 == 0:
                    lbl.configure(bg="#f7f7f7")
                row_cells.append(lbl)
            self.anim_cells.append(row_cells)
        
        # Info de estado
        self.anim_info = tk.Label(self.frame_animated, text="", font=self.font_label)
        self.anim_info.pack(pady=5)
        
        # Botones
        btn_frame = tk.Frame(self.frame_animated)
        btn_frame.pack(pady=10)
        self.btn_start_anim = tk.Button(btn_frame, text="Iniciar", width=12, 
                                       command=self._run_animation, font=self.font_button)
        self.btn_start_anim.pack(side="left", padx=5)
        self.btn_pause_anim = tk.Button(btn_frame, text="Pausar", width=12, 
                                       command=self._pause_animation, font=self.font_button, state="disabled")
        self.btn_pause_anim.pack(side="left", padx=5)
        tk.Button(btn_frame, text="Volver", width=12, 
                 command=lambda: self._show_frame(self.frame_start), font=self.font_button).pack(side="left", padx=5)

    def _create_result_panel(self, parent: tk.Widget, title: str) -> tk.Frame:
        frame = tk.Frame(parent, bd=2, relief="groove", padx=10, pady=10)
        tk.Label(frame, text=title, font=self.font_subtitle).pack()
        grid = tk.Frame(frame, padx=6, pady=6)
        grid.pack(pady=6)
        cells: list[list[tk.Label]] = []
        for r in range(9):
            row_cells: list[tk.Label] = []
            for c in range(9):
                lbl = tk.Label(grid, text="", width=2, font=self.font_result_cell, relief="solid", bd=1)
                lbl.grid(row=r, column=c,
                         padx=(0 if c % 3 != 0 else 6, 2),
                         pady=(0 if r % 3 != 0 else 6, 2))
                if ((r // 3) + (c // 3)) % 2 == 0:
                    lbl.configure(bg="#f7f7f7")
                row_cells.append(lbl)
            cells.append(row_cells)
        frame.grid_cells = cells  # type: ignore[attr-defined]
        frame.label_time = tk.Label(frame, text="Tiempo: -", font=self.font_label)
        frame.label_time.pack()
        frame.label_tries = tk.Label(frame, text="Intentos: -", font=self.font_label)
        frame.label_tries.pack()
        return frame

    # -------- Navegación / Acciones --------
    def _start_play(self):
        self.difficulty = self.diff_var.get()  # type: ignore[assignment]
        base = iniciateBaseMatrix()
        solution = [row[:] for row in base]
        puzzle = makeDifficulty([row[:] for row in solution], self.difficulty)

        self.solution = solution  # no se usa para validar entradas
        self.puzzle = puzzle
        self.fixed = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]

        reset()

        self._render_board()
        self._show_frame(self.frame_board)

    def _restart_play(self):
        if self.puzzle is None:
            return
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                e.configure(state="normal")
                if self.fixed and self.fixed[r][c]:
                    e.delete(0, tk.END)
                    e.insert(0, str(self.puzzle[r][c]))
                    e.configure(state="disabled", disabledforeground="#000000")
                else:
                    e.delete(0, tk.END)

    def _start_auto(self):
        self.difficulty = self.diff_var.get()  # type: ignore[assignment]
        base = iniciateBaseMatrix()
        solution = [row[:] for row in base]
        puzzle = makeDifficulty([row[:] for row in solution], self.difficulty)

        reset()
        t0 = time.perf_counter()
        solved_bt = backtracking([row[:] for row in puzzle])
        t1 = time.perf_counter()
        tries_bt = get_count("backtracking")

        reset()
        t2 = time.perf_counter()
        solved_bnb = branch_and_bound([row[:] for row in puzzle])
        t3 = time.perf_counter()
        tries_bnb = get_count()

        self._render_result_panel(self.panel_bt, solved_bt, t1 - t0, tries_bt)
        self._render_result_panel(self.panel_bnb, solved_bnb, t3 - t2, tries_bnb)

        total_empty = sum(1 for i in range(9) for j in range(9) if puzzle[i][j] == 0)
        info = f"Dificultad: {self.difficulty} · Celdas vacías: {total_empty}"
        if hasattr(self, "results_info"):
            self.results_info.config(text=info)
        else:
            self.results_info = tk.Label(self.frame_results, text=info, font=("Segoe UI", 10))
            self.results_info.pack(pady=(6, 0))

        self._show_frame(self.frame_results)

    def _start_animated(self):
        """Inicia la pantalla de animación"""
        self.difficulty = self.diff_var.get()  # type: ignore[assignment]
        base = iniciateBaseMatrix()
        solution = [row[:] for row in base]
        self.puzzle = makeDifficulty([row[:] for row in solution], self.difficulty)
        self.fixed = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        
        # Limpiar tablero animado
        for r in range(9):
            for c in range(9):
                val = self.puzzle[r][c]
                self.anim_cells[r][c].config(
                    text=str(val) if val != 0 else "",
                    fg="#000000" if val != 0 else "#666666",
                    bg="#e0e0e0" if val != 0 else ("#f7f7f7" if ((r // 3) + (c // 3)) % 2 == 0 else "#ffffff")
                )
        
        self.anim_info.config(text=f"Dificultad: {self.difficulty} · Presiona 'Iniciar' para comenzar")
        self.btn_start_anim.config(state="normal")
        self.btn_pause_anim.config(state="disabled")
        self.animation_running = False
        
        self._show_frame(self.frame_animated)

    def _update_speed(self, value):
        """Actualiza la velocidad de animación"""
        self.animation_speed = int(value)

    def _run_animation(self):
        """Ejecuta la animación paso a paso"""
        if self.animation_running:
            return
        
        self.animation_running = True
        self.btn_start_anim.config(state="disabled")
        self.btn_pause_anim.config(state="normal")
        
        algo = self.anim_algo_var.get()
        puzzle_copy = [row[:] for row in self.puzzle]  # type: ignore
        
        # Crear generador de pasos
        if algo == "backtracking":
            steps = self._backtracking_steps(puzzle_copy, 0)
        else:
            steps = self._bnb_steps(puzzle_copy)
        
        self._animate_steps(steps, 0)

    def _pause_animation(self):
        """Pausa la animación"""
        self.animation_running = False
        self.btn_start_anim.config(state="normal")
        self.btn_pause_anim.config(state="disabled")

    def _animate_steps(self, steps: list[tuple[int, int, int, str]], index: int):
        """Anima los pasos uno por uno"""
        if not self.animation_running or index >= len(steps):
            self.animation_running = False
            self.btn_start_anim.config(state="normal")
            self.btn_pause_anim.config(state="disabled")
            if index >= len(steps):
                self.anim_info.config(text=f"✓ Completado! ({len(steps)} pasos)")
            return
        
        row, col, value, action = steps[index]
        
        # Actualizar celda
        if action == "try":
            self.anim_cells[row][col].config(text=str(value), fg="#0066cc", bg="#e3f2fd")
        elif action == "backtrack":
            self.anim_cells[row][col].config(text="", fg="#666666", 
                                            bg="#f7f7f7" if ((row // 3) + (col // 3)) % 2 == 0 else "#ffffff")
        elif action == "success":
            self.anim_cells[row][col].config(text=str(value), fg="#006400", bg="#c8e6c9")
        
        self.anim_info.config(text=f"Paso {index + 1}/{len(steps)} · Celda ({row},{col}) = {value}")
        
        # Programar siguiente paso
        self.after(self.animation_speed, lambda: self._animate_steps(steps, index + 1))

    def _backtracking_steps(self, board: list[list[int]], cell_index: int) -> list[tuple[int, int, int, str]]:
        """Genera los pasos del backtracking"""
        steps: list[tuple[int, int, int, str]] = []
        
        def solve(ci: int) -> bool:
            if ci == 81:
                return True
            
            row, col = divmod(ci, 9)
            
            if board[row][col] != 0:
                return solve(ci + 1)
            
            from utils.utils import generateValues
            for value in generateValues():
                steps.append((row, col, value, "try"))
                board[row][col] = value
                
                if isFactible(board, value, row, col):
                    if solve(ci + 1):
                        steps.append((row, col, value, "success"))
                        return True
                
                board[row][col] = 0
                steps.append((row, col, value, "backtrack"))
            
            return False
        
        solve(0)
        return steps

    def _bnb_steps(self, matrix: list[list[int]]) -> list[tuple[int, int, int, str]]:
        """Genera los pasos del Branch and Bound (simplificado)"""
        steps: list[tuple[int, int, int, str]] = []
        
        def solve() -> bool:
            # Encontrar celda vacía con menos opciones
            min_options = 10
            best_cell = None
            
            for r in range(9):
                for c in range(9):
                    if matrix[r][c] == 0:
                        options = self._get_valid_values(matrix, r, c)
                        if len(options) < min_options:
                            min_options = len(options)
                            best_cell = (r, c, options)
            
            if best_cell is None:
                return True  # Completo
            
            row, col, options = best_cell
            
            for value in sorted(options):
                steps.append((row, col, value, "try"))
                matrix[row][col] = value
                
                if solve():
                    steps.append((row, col, value, "success"))
                    return True
                
                matrix[row][col] = 0
                steps.append((row, col, value, "backtrack"))
            
            return False
        
        solve()
        return steps

    def _get_valid_values(self, matrix: list[list[int]], row: int, col: int) -> set[int]:
        """Obtiene valores válidos para una celda"""
        used = set()
        
        # Fila y columna
        for i in range(9):
            used.add(matrix[row][i])
            used.add(matrix[i][col])
        
        # Subcuadro
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                used.add(matrix[box_r + i][box_c + j])
        
        return set(range(1, 10)) - used

    # -------- Render helpers --------
    def _render_board(self):
        assert self.puzzle is not None
        self.label_info.config(text=f"Dificultad: {self.difficulty}")

        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                e.configure(state="normal", fg="#000000")
                e.delete(0, tk.END)
                val = self.puzzle[r][c]
                if val != 0:
                    e.insert(0, str(val))
                    e.configure(state="disabled", disabledforeground="#000000")

    def _render_result_panel(self, panel: tk.Frame, matrix: list[list[int]] | None, elapsed: float, tries: int):
        for r in range(9):
            for c in range(9):
                lbl: tk.Label = panel.grid_cells[r][c]  # type: ignore[attr-defined]
                lbl.config(text=str(matrix[r][c]) if matrix else "·")
        panel.label_time.config(text=f"Tiempo: {elapsed:.6f} s")
        panel.label_tries.config(text=f"Intentos: {tries}")

    # -------- Validación y feedback --------
    def _validate_input_cell(self, proposed: str, action: str, widget_path: str) -> bool:
        # Permitir borrar
        if action == "0":
            return True
        # Permitir vacío
        if len(proposed) == 0:
            return True
        # Restringir a un solo dígito 1-9
        return len(proposed) == 1 and proposed in "123456789"

    def _on_cell_key(self, event: tk.Event, row: int, col: int):
        # No actuar sobre celdas fijas
        if self.fixed and self.fixed[row][col]:
            return
        e: tk.Entry = event.widget  # type: ignore[assignment]
        text = e.get().strip()

        # Cancelar borrado pendiente si el usuario editó
        key = (row, col)
        if key in self.pending_clear:
            try:
                self.after_cancel(self.pending_clear[key])
            except Exception:
                pass
            finally:
                del self.pending_clear[key]

        if text == "":
            e.configure(fg="#000000")
            return
        if not text.isdigit():
            return

        # Construir tablero actual y validar contexto
        matrix: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                t = self.entries[r][c].get().strip()
                if t.isdigit():
                    matrix[r][c] = int(t)

        value = int(text)
        matrix[row][col] = value

        if isFactible(matrix, value, row, col):
            # Válido en el contexto actual: sin pistas, sólo normalizar color
            e.configure(fg="#000000")
            
            # Verificar si el sudoku está completo
            self._check_completion(matrix)
        else:
            # Mostrar en rojo brevemente y borrar automáticamente
            e.configure(fg="#b00020")

            last_text = text

            def clear_if_unchanged():
                current = e.get().strip()
                if current == last_text:
                    e.delete(0, tk.END)
                    e.configure(fg="#000000")
                # limpiar id pendiente
                if key in self.pending_clear:
                    del self.pending_clear[key]

            after_id = self.after(500, clear_if_unchanged)
            self.pending_clear[key] = after_id

    def _check_completion(self, matrix: list[list[int]]):
        """Verifica si el Sudoku está completado correctamente"""
        # 1. Verificar que no haya celdas vacías
        for r in range(9):
            for c in range(9):
                if matrix[r][c] == 0:
                    return  # Aún hay celdas vacías
        
        # 2. Verificar que todas las celdas sean válidas
        for r in range(9):
            for c in range(9):
                value = matrix[r][c]
                if not isFactible(matrix, value, r, c):
                    return  # Hay errores
        
        # 3. ¡Sudoku completado correctamente!
        self._show_victory()
    
    def _show_victory(self):
        """Muestra mensaje de victoria y deshabilita el tablero"""
        # Deshabilitar todas las celdas editables
        for r in range(9):
            for c in range(9):
                if self.fixed and not self.fixed[r][c]:
                    self.entries[r][c].configure(state="disabled", disabledforeground="#006400")
        
        # Actualizar mensaje
        self.label_info.config(
            text=f"¡Felicitaciones! Completaste el Sudoku ({self.difficulty})",
            fg="#006400",
            font=self.font_subtitle
        )
        
        # Opcional: Mostrar diálogo
        import tkinter.messagebox as mb
        mb.showinfo("¡Victoria!", "¡Felicitaciones! Has completado el Sudoku correctamente.")


def gui_main():
    app = SudokuGUI()
    app.mainloop()


if __name__ == "__main__":
    gui_main()