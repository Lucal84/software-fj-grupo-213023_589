# ==============================================================================
# Archivo: simulaciones.py
# Autor: Esloder Alvarez (Xloder-17)
# Descripción: Simulación de 12 operaciones completas (válidas e inválidas)
# para el sistema de gestión de Software FJ, con manejo robusto de excepciones
# y registro de eventos/errores en archivo de logs (sin base de datos).
# ==============================================================================


from modelo.cliente import Cliente
from modelo.servicios import ReservaSala, AlquilerEquipo, Asesoria
from modelo.reserva import Reserva
from modelo.registro import logger as logging #usar el logger central como propio
from modelo.excepciones import OperacionNoPermitidaError as ErrorSimulacionError #de igual manera usa la excepción personalizada


def ejecutar_simulaciones():
    """Ejecuta 12 operaciones de prueba demostrando estabilidad ante errores."""
    # Listas internas para gestionar los objetos en memoria (sin base de datos)
    clientes = []
    servicios = []
    reservas = []

    print("=" * 65)
    print("  INICIANDO SIMULACIONES - SISTEMA SOFTWARE FJ (12 OPERACIONES)")
    print("=" * 65)
    logging.info("=== Inicio de ejecución de simulaciones ===")

    # ------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de Cliente 1 (try / except / else / finally)
    # ------------------------------------------------------------------
    print("\n[Operación 1] Registro válido de Cliente 1...")
    try:
        c1 = Cliente("CLI-001", "Laura Martínez", "laura.m@correo.com", "3105551234")
    except ValueError as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 1 - Error al crear Cliente 1: {e}")
    else:
        clientes.append(c1)
        print(f"  -> Éxito: {c1.describir()}")
        logging.info(f"Op 1 - Cliente registrado: {c1.identificador}")
    finally:
        print("  -> Fin de la Operación 1.")

    # ------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de Cliente 2 (try / except / else)
    # ------------------------------------------------------------------
    print("\n[Operación 2] Registro válido de Cliente 2...")
    try:
        c2 = Cliente("CLI-002", "Carlos Gómez", "carlos.gomez@empresa.co", "3209876543")
    except ValueError as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 2 - Error al crear Cliente 2: {e}")
    else:
        clientes.append(c2)
        print(f"  -> Éxito: {c2.describir()}")
        logging.info(f"Op 2 - Cliente registrado: {c2.identificador}")

    # ------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de Cliente (correo sin '@' ni '.')
    # ------------------------------------------------------------------
    print("\n[Operación 3] Registro inválido de Cliente (correo incorrecto)...")
    try:
        c_invalido = Cliente("CLI-003", "Ana Ruiz", "correo_invalido", "3001112233")
        clientes.append(c_invalido)
    except ValueError as e:
        print(f"  -> Error controlado correctamente: {e}")
        logging.warning(f"Op 3 - Intento fallido de registro de cliente: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 4: Registro inválido de Cliente (teléfono con letras)
    # ------------------------------------------------------------------
    print("\n[Operación 4] Registro inválido de Cliente (teléfono inválido)...")
    try:
        c_tel_malo = Cliente("CLI-004", "Pedro López", "pedro@correo.com", "abc123")
        clientes.append(c_tel_malo)
    except ValueError as e:
        print(f"  -> Error controlado correctamente: {e}")
        logging.warning(f"Op 4 - Teléfono inválido rechazado: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 5: Creación válida de ReservaSala (capacidad > 20, recargo 20%)
    # ------------------------------------------------------------------
    print("\n[Operación 5] Creación válida de servicio ReservaSala...")
    try:
        s1 = ReservaSala("SER-001", "Sala Ejecutiva Norte", 50000.0, capacidad=25)
    except ValueError as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 5 - Error creando sala: {e}")
    else:
        servicios.append(s1)
        print(f"  -> Éxito: {s1.describir()}")
        logging.info(f"Op 5 - Servicio creado: {s1.identificador}")

    # ------------------------------------------------------------------
    # OPERACIÓN 6: Creación válida de AlquilerEquipo
    # ------------------------------------------------------------------
    print("\n[Operación 6] Creación válida de servicio AlquilerEquipo...")
    try:
        s2 = AlquilerEquipo("SER-002", "Portátiles Dell i7", 20000.0, cantidad_equipos=3)
    except ValueError as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 6 - Error creando alquiler de equipo: {e}")
    else:
        servicios.append(s2)
        print(f"  -> Éxito: {s2.describir()}")
        logging.info(f"Op 6 - Servicio creado: {s2.identificador}")

    # ------------------------------------------------------------------
    # OPERACIÓN 7: Creación válida de Asesoria
    # ------------------------------------------------------------------
    print("\n[Operación 7] Creación válida de servicio Asesoria...")
    try:
        s3 = Asesoria("SER-003", "Consultoría Cloud", 80000.0, especialidad="Arquitectura AWS")
    except ValueError as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 7 - Error creando asesoría: {e}")
    else:
        servicios.append(s3)
        print(f"  -> Éxito: {s3.describir()}")
        logging.info(f"Op 7 - Servicio creado: {s3.identificador}")

    # ------------------------------------------------------------------
    # OPERACIÓN 8: Creación inválida de servicio (tarifa negativa)
    # ------------------------------------------------------------------
    print("\n[Operación 8] Creación inválida de servicio (tarifa negativa)...")
    try:
        s_invalido = ReservaSala("SER-004", "Sala Sur", -15000.0, capacidad=10)
        servicios.append(s_invalido)
    except ValueError as e:
        print(f"  -> Error controlado correctamente: {e}")
        logging.warning(f"Op 8 - Servicio rechazado por tarifa inválida: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa (Crear -> Confirmar con impuesto/descuento -> Procesar)
    # ------------------------------------------------------------------
    print("\n[Operación 9] Reserva exitosa completa (Sala con IVA 19% y Desc 10%)...")
    try:
        r1 = Reserva("RES-001", clientes[0], servicios[0], duracion=3)
        r1.confirmar(impuesto=19.0, descuento=10.0)
        r1.procesar()
    except (ValueError, IndexError) as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 9 - Error en reserva 1: {e}")
    else:
        reservas.append(r1)
        print(f"  -> Éxito: {r1.describir()}")
        logging.info(f"Op 9 - Reserva procesada: {r1.identificador} | Total: ${r1.costo_total}")
    finally:
        print("  -> Verificación de estado finalizada para RES-001.")

    # ------------------------------------------------------------------
    # OPERACIÓN 10: Reserva confirmada y luego cancelada
    # ------------------------------------------------------------------
    print("\n[Operación 10] Reserva de equipos confirmada y posteriormente cancelada...")
    try:
        r2 = Reserva("RES-002", clientes[1], servicios[1], duracion=2)
        r2.confirmar(impuesto=19.0)
        r2.cancelar()
    except (ValueError, IndexError) as e:
        print(f"  -> Error: {e}")
        logging.error(f"Op 10 - Error en reserva 2: {e}")
    else:
        reservas.append(r2)
        print(f"  -> Éxito: {r2.describir()}")
        logging.info(f"Op 10 - Reserva cancelada correctamente: {r2.identificador}")

    # ------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida (servicio NO disponible)
    # ------------------------------------------------------------------
    print("\n[Operación 11] Intento de reserva con servicio NO disponible...")
    try:
        s_no_disp = Asesoria("SER-005", "Soporte Redes", 60000.0, "Redes Cisco", disponible=False)
        servicios.append(s_no_disp)
        r_fallida = Reserva("RES-003", clientes[0], s_no_disp, duracion=2)
        reservas.append(r_fallida)
    except ValueError as e:
        print(f"  -> Error controlado correctamente: {e}")
        logging.warning(f"Op 11 - Reserva rechazada por disponibilidad: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 12: Operación no permitida con encadenamiento de excepciones
    # ------------------------------------------------------------------
    print("\n[Operación 12] Intento de procesar una reserva ya CANCELADA...")
    try:
        try:
            # Intentamos procesar r2, que fue cancelada en la Operación 10
            reservas[1].procesar()
        except ValueError as causa_original:
            # Encadenamiento de excepciones (raise ... from ...)
            raise ErrorSimulacionError(
                "No es posible procesar la reserva RES-002 debido a su estado actual."
            ) from causa_original
    except ErrorSimulacionError as e:
        print(f"  -> Excepción personalizada capturada: {e}")
        print(f"  -> Causa original encadenada: {e.__cause__}")
        logging.error(f"Op 12 - {e} | Causa: {e.__cause__}")
    finally:
        print("  -> Limpieza y cierre de prueba de estado completado.")

    # --- Resumen final de la simulación ---
    print("\n" + "=" * 65)
    print("  RESUMEN FINAL DE LA SIMULACIÓN (EL SISTEMA SIGUE ACTIVO)")
    print("=" * 65)
    print(f"  * Clientes válidos registrados: {len(clientes)}")
    print(f"  * Servicios registrados:        {len(servicios)}")
    print(f"  * Reservas registradas:         {len(reservas)}")
    print("  * Registro de eventos guardado en: logs/eventos.log")
    print("=" * 65)
    logging.info("=== Fin de ejecución de simulaciones sin interrupciones ===")


# Punto de entrada para ejecutar directamente este archivo
if __name__ == "__main__":
    ejecutar_simulaciones()