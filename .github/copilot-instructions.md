## Repo quick-start for AI coding agents

This project is a small Sudoku solver implemented in Python. These instructions give focused, actionable context an AI agent needs to be productive: how the code is laid out, important conventions, run/debug steps, and examples to reference.

### Big picture
- Source root: `src/` — code is written as a simple package where `src/` is used as the working directory.
- Solver components live under `src/utils/`:
  - `utils.py` — helper functions, printing, matrix initialization, feasibility checks, difficulty generation.
  - `backtracking.py` — working backtracking solver and helper to generate a complete base matrix.
  - `byb.py` — a skeleton for Branch-and-Bound (pseudocode only; not implemented).
- Entrypoints:
  - `src/main.py` — demo runner that creates a base matrix, reduces difficulty and attempts to solve it.
  - `src/tests.py` — simple script with small print tests.

### How to run (developer workflows)
- Run from the `src` directory so relative imports resolve as written. Example (Windows PowerShell):

  ```powershell
  cd src
  python main.py
  # or run the quick tests
  python tests.py
  ```

- There is no requirements file — only stdlib is used (`random`, `typing`).

### Project-specific conventions and patterns
- Code uses Spanish identifiers and comments (e.g. `iniciateBaseMatrix`, `isFactible`). Preserve naming when editing to avoid breaking imports.
- Matrices are 9x9 nested lists of ints: `list[list[int]]`. Indexing is row-major. Several functions expect rows and columns as integers 0..8.
- The backtracking solver uses a single integer `E` (0..80) as a linear position; row = E // 9, col = E % 9. Look for that pattern in `backtracking.py` when altering the solver.
- Difficulty is created by removing cells; `makeDifficulty(matrix, 'easy'|'medium'|'hard')` selects removal ranges. Keep these literals unchanged.

### Important implementation notes / gotchas (discovered)
- `src/utils/__init__.py` exposes names via `__all__` — double-check names before refactoring exports. Some names in `__all__` appear inconsistent (e.g., `populate_with_dificulty` is listed but not defined). Be conservative: run the scripts after changes.
- `byb.py` is pseudocode only. Do not assume Branch-and-Bound is implemented; if asked to implement, treat `byb.py` as a starting design, not working code.
- The codebase relies on running from `src/` to resolve `from utils...` imports. If you change package layout, update import paths or add packaging metadata.

### Examples (copy-pasteable references)
- Create and solve a puzzle (from `src/main.py`):

  - `base_matrix = iniciateBaseMatrix()`  # builds a complete solved board
  - `matrix = makeDifficulty(base_matrix, 'easy')`  # remove cells to create puzzle
  - `matrix_solved = backtracking(matrix)`  # attempt to solve

- Useful helpers in `src/utils/utils.py`:
  - `print_matrix(matrix)` — pretty prints the 9x9 board
  - `initialize_matrix()` — returns 9x9 zero matrix
  - `isFactible(matrix, v, row, col)` — feasibility check for a candidate value

### What an AI agent should do first
1. Run `cd src && python main.py` locally to observe runtime behavior and outputs.
2. Read `src/utils/backtracking.py` to understand solver data flow (E index, recursion, feasibility checks).
3. When changing public function names or `__all__`, run `main.py` and `tests.py` to validate imports.

### When to ask the user
- Confirm whether you may rename Spanish-named functions for readability; renaming affects imports and may break scripts.
- Ask if they'd like Branch-and-Bound implemented (file `src/utils/byb.py` is a pseudocode stub).

If any section is unclear or you want more examples (unit-test scaffolding, packaging, or CI suggestions), tell me which parts to expand.
