# main.py
from modelo.registro import logger, registrar_error
from simulaciones import ejecutar_simulaciones
from gui import VentanaPrincipal
import tkinter as tk


def main():
    # Ejecutar las simulaciones de simulaciones.py
    try:
        ejecutar_simulaciones()
    except Exception as e:
        registrar_error("Error grave en simulación", e)
    finally:
        logger.info("Simulación finalizada. Abriendo interfaz gráfica...")

    # Lanzar interfaz gráfica
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()