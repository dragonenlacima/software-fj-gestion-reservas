"""
Módulo de reservas del sistema "Software FJ".

Define el enumerado `EstadoReserva` y la clase `Reserva`, que integra un cliente,
un servicio, una duración y un estado. El costo total se CONGELA al momento de
crear la reserva (no cambia aunque el servicio se modifique después). Todas las
operaciones (`confirmar`, `cancelar`, `procesar`) manejan excepciones y registran
los eventos relevantes en el log.
"""

from datetime import datetime
from enum import Enum

from entidad_base import EntidadBase
from excepciones import (
    ErrorBaseSistema,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from logger_config import obtener_logger

# Logger compartido del módulo de reservas.
_logger = obtener_logger()


class EstadoReserva(Enum):
    """Estados posibles del ciclo de vida de una reserva."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"


class Reserva(EntidadBase):
    """Representa una reserva que integra cliente, servicio, duración y estado."""

    def __init__(self, id_entidad, cliente, servicio, duracion):
        """Crea la reserva, la valida y congela su costo total."""
        super().__init__(id_entidad)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = EstadoReserva.PENDIENTE
        self.fecha_creacion = datetime.now()
        self.costo_total = None

        # Se valida la reserva (disponibilidad y duración) antes de continuar.
        self.validar()

        # Se congela el costo total en el momento de crear la reserva.
        try:
            self.costo_total = self.servicio.calcular_costo(aplicar_impuesto=True)
        except ErrorBaseSistema as exc:
            # Se encadena la excepción original para conservar su causa real.
            raise ReservaInvalidaError(
                "No fue posible congelar el costo de la reserva."
            ) from exc
        else:
            # Solo se registra el éxito si no hubo excepción (bloque else).
            _logger.info(
                "Reserva %s creada y costo congelado en %.2f.",
                self.id, self.costo_total,
            )

    def validar(self):
        """Valida disponibilidad del servicio y duración de la reserva."""
        # El servicio debe estar disponible.
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' no está disponible."
            )
        # La duración debe ser un número positivo.
        if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
            raise ReservaInvalidaError(
                "La duración de la reserva debe ser un valor positivo."
            )
        return True

    def confirmar(self):
        """
        Confirma la reserva.

        Demuestra el uso conjunto de try / except / else / finally:
        - except: registra y propaga el error si la confirmación falla.
        - else: aplica el cambio de estado solo si no hubo excepción.
        - finally: deja constancia del intento ocurra lo que ocurra.
        """
        try:
            if self.estado != EstadoReserva.PENDIENTE:
                raise ReservaInvalidaError(
                    "Solo se puede confirmar una reserva en estado PENDIENTE."
                )
            self.validar()
        except ErrorBaseSistema as exc:
            _logger.error("Error al confirmar la reserva %s: %s", self.id, exc)
            raise
        else:
            self.estado = EstadoReserva.CONFIRMADA
            _logger.info("Reserva %s confirmada correctamente.", self.id)
            return True
        finally:
            _logger.info(
                "Finalizó el intento de confirmación de la reserva %s.", self.id
            )

    def cancelar(self):
        """Cancela la reserva si su estado lo permite."""
        try:
            if self.estado in (EstadoReserva.PROCESADA, EstadoReserva.CANCELADA):
                raise ReservaInvalidaError(
                    "No se puede cancelar una reserva ya procesada o cancelada."
                )
        except ErrorBaseSistema as exc:
            _logger.error("Error al cancelar la reserva %s: %s", self.id, exc)
            raise
        else:
            self.estado = EstadoReserva.CANCELADA
            _logger.info("Reserva %s cancelada correctamente.", self.id)
            return True

    def procesar(self):
        """
        Procesa la reserva confirmada.

        Demuestra el uso de try / except / finally: el bloque finally siempre
        registra el cierre del intento, haya o no excepción.
        """
        try:
            if self.estado != EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaError(
                    "Solo se puede procesar una reserva en estado CONFIRMADA."
                )
            self.estado = EstadoReserva.PROCESADA
            _logger.info(
                "Reserva %s procesada. Costo total: %.2f.",
                self.id, self.costo_total,
            )
            return True
        except ErrorBaseSistema as exc:
            _logger.error("Error al procesar la reserva %s: %s", self.id, exc)
            raise
        finally:
            _logger.info(
                "Finalizó el intento de procesamiento de la reserva %s.", self.id
            )

    def describir(self):
        """Devuelve una descripción legible de la reserva."""
        costo = f"{self.costo_total:.2f}" if self.costo_total is not None else "N/D"
        return (
            f"Reserva #{self.id} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Estado: {self.estado.value} | Costo congelado: {costo}"
        )