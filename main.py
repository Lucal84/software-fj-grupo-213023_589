# main.py
import sys
from modelo.registro import logger, registrar_error
from modelo.excepciones import ValidacionError, ServicioNoDisponibleError, OperacionNoPermitidaError
from modelo.cliente import Cliente
from modelo.servicios import ReservaSala, AlquilerEquipo, Asesoria
from modelo.reserva import Reserva

def simular_operaciones():
    """Ejecuta 10 operaciones de prueba (válidas e inválidas)."""
    logger.info("=== INICIO DE SIMULACIÓN DE OPERACIONES ===")

    # 1. Registro válido de cliente
    try:
        c1 = Cliente("C001", "Ana Pérez", "ana@mail.com", "3001234567")
        logger.info(f"Cliente registrado: {c1.describir()}")
    except Exception as e:
        logger.error("Error en op1", exc_info=True)

    # 2. Registro inválido de cliente (nombre muy corto)
    try:
        c2 = Cliente("C002", "Lu", "lu@mail.com", "3009876543")
    except ValueError as e:
        registrar_error("Op2: Nombre inválido", e)

    # 3. Registro inválido de cliente (correo sin @)
    try:
        c3 = Cliente("C003", "Carlos Ruiz", "carlosmail.com", "3015556666")
    except ValueError as e:
        registrar_error("Op3: Correo inválido", e)

    # 4. Creación válida de servicio (ReservaSala)
    try:
        s1 = ReservaSala("S001", "Sala Magna", 50.0, 25)
        logger.info(f"Servicio creado: {s1.describir()}")
    except Exception as e:
        logger.error("Error en op4", exc_info=True)

    # 5. Creación inválida de servicio (tarifa negativa)
    try:
        s2 = AlquilerEquipo("S002", "Laptop HP", -10.0, 5)
    except ValueError as e:
        registrar_error("Op5: Tarifa negativa", e)

    # 6. Creación válida de servicio (Asesoria)
    try:
        s3 = Asesoria("S003", "Consultoría Python", 80.0, "Desarrollo")
        logger.info(f"Servicio creado: {s3.describir()}")
    except Exception as e:
        logger.error("Error en op6", exc_info=True)

    # --- Reservas ---
    # 7. Reserva exitosa
    try:
        r1 = Reserva("R001", c1, s1, 4)
        r1.confirmar(impuesto=10, descuento=5)
        logger.info(f"Reserva exitosa: {r1.describir()}")
    except Exception as e:
        registrar_error("Op7: Error en reserva válida", e)

    # 8. Reserva fallida (duración excesiva para el servicio)
    try:
        r2 = Reserva("R002", c1, s3, 0)  # duración inválida (0)
    except ValueError as e:
        registrar_error("Op8: Duración inválida", e)

    # 9. Reserva fallida (servicio no disponible)
    try:
        s1.disponible = False
        r3 = Reserva("R003", c1, s1, 2)
        r3.confirmar()
    except Exception as e:
        registrar_error("Op9: Servicio no disponible", e)
    finally:
        s1.disponible = True  # Restaurar estado

    # 10. Encadenamiento de excepciones (intento de cancelar una reserva ya procesada)
    try:
        r4 = Reserva("R004", c1, s3, 2)
        r4.confirmar()
        r4.procesar()
        try:
            r4.cancelar()  # Esto lanzará OperacionNoPermitidaError
        except Exception as e:
            raise OperacionNoPermitidaError("No se puede cancelar una reserva procesada.") from e
    except OperacionNoPermitidaError as e:
        registrar_error("Op10: Encadenamiento de excepciones", e)
    except Exception as e:
        registrar_error("Op10: Error inesperado", e)

    logger.info("=== FIN DE SIMULACIÓN ===")

def main():
    # Ejecutar simulación (10 operaciones)
    try:
        simular_operaciones()
    except Exception as e:
        registrar_error("Error grave en simulación", e)
    finally:
        logger.info("Simulación finalizada. Abriendo interfaz gráfica...")

    # Lanzar interfaz gráfica
    import tkinter as tk
    from gui import VentanaPrincipal
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()