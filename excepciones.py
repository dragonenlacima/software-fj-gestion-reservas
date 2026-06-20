"""
Módulo de excepciones personalizadas del sistema "Software FJ".

Define una jerarquía de excepciones que parte de una excepción base común
(`ErrorBaseSistema`), de la cual derivan todas las excepciones específicas del
dominio. Esto permite capturar errores de forma granular (cada tipo concreto) o
de forma genérica (la base), manteniendo mensajes claros en español para su
registro en el archivo de logs.
"""


# ---------------------------------------------------------------------------
# Excepción base de todo el sistema
# ---------------------------------------------------------------------------
class ErrorBaseSistema(Exception):
    """Excepción base de la cual heredan todas las excepciones del sistema."""


# ---------------------------------------------------------------------------
# Excepciones específicas del dominio (todas heredan de ErrorBaseSistema)
# ---------------------------------------------------------------------------
class DatoInvalidoError(ErrorBaseSistema):
    """Se lanza cuando un dato genérico no cumple el formato esperado."""


class ClienteInvalidoError(ErrorBaseSistema):
    """Se lanza cuando los datos de un cliente son inválidos."""


class ParametroInvalidoError(ErrorBaseSistema):
    """Se lanza cuando un parámetro de un servicio es inválido."""


class ServicioNoDisponibleError(ErrorBaseSistema):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(ErrorBaseSistema):
    """Se lanza cuando una reserva no cumple las reglas de negocio."""


class CalculoInconsistenteError(ErrorBaseSistema):
    """Se lanza cuando un cálculo de costos produce un valor incoherente."""
