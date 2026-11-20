# modelo/registro.py
import logging
import sys
import os
from logging.handlers import RotatingFileHandler

LOG_FILE = "sistema.log"

def configurar_logging():
    """Configura el logger global para archivo y consola."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se llama varias veces
    if logger.handlers:
        return logger

    # Formato detallado: fecha, nivel, módulo, función y línea
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para archivo (rotativo: máx 5 MB, 3 backups)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para consola (solo errores y advertencias)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Hook para excepciones no capturadas
    def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Excepción no manejada", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_uncaught_exception
    return logger

# Instancia global del logger
logger = configurar_logging()

def registrar_error(mensaje: str, excepcion: Exception = None, nivel=logging.ERROR):
    """Registra un mensaje y, si se proporciona, la excepción asociada."""
    if excepcion:
        logger.log(nivel, f"{mensaje} | Excepción: {type(excepcion).__name__}: {excepcion}", exc_info=True)
    else:
        logger.log(nivel, mensaje)