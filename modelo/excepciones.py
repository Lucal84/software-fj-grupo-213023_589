# modelo/excepciones.py

class SistemaError(Exception):
    """Excepción base para todos los errores del sistema."""
    pass

class ValidacionError(SistemaError):
    """Error en la validación de datos (clientes, servicios, reservas)."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """El servicio solicitado no está disponible."""
    pass

class OperacionNoPermitidaError(SistemaError):
    """La operación no está permitida en el estado actual de la reserva."""
    pass

class CalculoInconsistenteError(SistemaError):
    """Los cálculos de costos produjeron resultados inválidos."""
    pass

class ParametroFaltanteError(SistemaError):
    """Faltan parámetros obligatorios para realizar una operación."""
    pass