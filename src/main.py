"""
Sudoku Solver - Main Entry Point
Implementa UI con termios para juego manual y resolución automática
"""
from ui.terminal import menu, clear_screen
from ui.game import modo_manual, modo_automatico


def main():
    """Función principal con menú interactivo"""

    while True:
        clear_screen()
        print("""
    ███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
    ██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
    ███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
    ╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
    ███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
    ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
        """)

        # Menú principal
        opciones_principal = ["Modo Manual", "Modo Automático", "Salir"]
        seleccion = menu("=== MENÚ PRINCIPAL ===", opciones_principal)

        if seleccion == 2:  # Salir
            clear_screen()
            print("\n  ¡Hasta luego!\n")
            break

        # Seleccionar dificultad
        clear_screen()
        opciones_dificultad = ["Fácil", "Medio", "Difícil"]
        dificultad_idx = menu("=== SELECCIONAR DIFICULTAD ===", opciones_dificultad)

        difficulty_map = {0: "easy", 1: "medium", 2: "hard"}
        difficulty = difficulty_map[dificultad_idx]

        if seleccion == 0:  # Modo Manual
            modo_manual(difficulty)

        elif seleccion == 1:  # Modo Automático
            # Seleccionar algoritmo
            clear_screen()
            opciones_algoritmo = ["Backtracking", "Branch and Bound", "Ambos (comparar)"]
            algoritmo_idx = menu("=== SELECCIONAR ALGORITMO ===", opciones_algoritmo)

            algorithm_map = {0: "backtracking", 1: "bnb", 2: "both"}
            algorithm = algorithm_map[algoritmo_idx]

            modo_automatico(difficulty, algorithm)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n  Programa interrumpido\n")