"""
Módulo de configuración del sistema de logs de "Software FJ".

Expone la función `obtener_logger`, que devuelve un logger configurado para
escribir en `logs/sistema.log`. Si la carpeta `logs` no existe, se crea de forma
automática. Se registran los eventos exitosos con nivel INFO y las excepciones
capturadas con nivel ERROR, usando el formato solicitado:
"%(asctime)s | %(levelname)s | %(message)s".
"""

import logging
import os

# Ruta base: carpeta donde reside este módulo. Se calcula así para que el log
# siempre se genere dentro del proyecto, sin importar desde qué directorio se
# ejecute la aplicación.
_DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
_DIRECTORIO_LOGS = os.path.join(_DIRECTORIO_BASE, "logs")
_ARCHIVO_LOG = os.path.join(_DIRECTORIO_LOGS, "sistema.log")


def obtener_logger(nombre="software_fj"):
    """
    Crea (o recupera) un logger configurado para el sistema.

    - Crea la carpeta `logs` si todavía no existe.
    - Escribe en `logs/sistema.log` con el formato requerido.
    - Evita duplicar handlers si la función se invoca varias veces.

    :param nombre: Nombre lógico del logger.
    :return: Instancia de `logging.Logger` lista para usar.
    """
    # Se crea la carpeta de logs si aún no existe (operación idempotente).
    os.makedirs(_DIRECTORIO_LOGS, exist_ok=True)

    # logging.getLogger garantiza una única instancia por nombre (singleton).
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    # Solo se agrega el handler una vez para no duplicar líneas en el archivo.
    if not logger.handlers:
        manejador = logging.FileHandler(_ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger