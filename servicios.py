"""
Módulo de servicios del sistema "Software FJ".

Define la clase abstracta `Servicio` y tres servicios especializados que aplican
POLIMORFISMO (sobrescriben `calcular_costo`, `describir` y `validar_parametros`).

El cálculo de costos admite SOBRECARGA de dos formas complementarias:
  1. Parámetros opcionales: `calcular_costo()`,
     `calcular_costo(aplicar_impuesto=True)`,
     `calcular_costo(aplicar_impuesto=True, descuento=0.10)`.
  2. `functools.singledispatchmethod`: el descuento se interpreta según su tipo
     (float = fracción 0.10 -> 10%; int = porcentaje entero 10 -> 10%).

Se usa la constante `IVA = 0.19` (19%). `validar_parametros()` lanza
`ParametroInvalidoError` ante valores inválidos y, si un cálculo resulta negativo
o incoherente, se lanza `CalculoInconsistenteError`.
"""

import functools
from abc import ABC, abstractmethod

from entidad_base import EntidadBase
from excepciones import CalculoInconsistenteError, ParametroInvalidoError

# Constante de IVA (19%) aplicada en el cálculo de costos.
IVA = 0.19


class Servicio(EntidadBase, ABC):
    """Clase base abstracta para todos los servicios ofrecidos."""

    def __init__(self, id_entidad, nombre, costo_base, disponible=True):
        """Inicializa los atributos comunes a todo servicio."""
        super().__init__(id_entidad)
        self.nombre = nombre
        self.costo_base = costo_base
        self.disponible = disponible

    # ----- Métodos abstractos (polimorfismo en las subclases) ---------------
    @abstractmethod
    def calcular_costo(self, aplicar_impuesto=False, descuento=0.0):
        """Calcula el costo del servicio. Cada subclase lo sobrescribe."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible del servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self):
        """Valida los parámetros propios del servicio."""
        raise NotImplementedError

    # ----- Sobrecarga del descuento por tipo (singledispatchmethod) ---------
    @functools.singledispatchmethod
    def _aplicar_descuento(self, descuento, costo):
        """Implementación por defecto: el tipo de descuento no es soportado."""
        raise ParametroInvalidoError(
            f"Tipo de descuento no soportado: {type(descuento).__name__}."
        )

    @_aplicar_descuento.register
    def _(self, descuento: float, costo):
        # Descuento expresado como fracción (0.10 = 10%).
        if not 0.0 <= descuento < 1.0:
            raise ParametroInvalidoError(
                "El descuento (fracción) debe estar entre 0 y 1."
            )
        return costo * (1 - descuento)

    @_aplicar_descuento.register
    def _(self, descuento: int, costo):
        # Descuento expresado como porcentaje entero (10 = 10%).
        if not 0 <= descuento < 100:
            raise ParametroInvalidoError(
                "El descuento (porcentaje) debe estar entre 0 y 100."
            )
        return costo * (1 - descuento / 100)

    # ----- Validación común (implementa EntidadBase.validar) ----------------
    def validar(self):
        """Valida atributos comunes y delega los específicos en la subclase."""
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ParametroInvalidoError("El nombre del servicio es obligatorio.")
        if not isinstance(self.costo_base, (int, float)) or self.costo_base < 0:
            raise ParametroInvalidoError("El costo base no puede ser negativo.")
        # Validación específica (polimorfismo): cada subclase la implementa.
        self.validar_parametros()
        return True

    # ----- Ajuste de costo: aplica descuento e impuesto ---------------------
    def _ajustar_costo(self, costo, aplicar_impuesto=False, descuento=0.0):
        """
        Aplica descuento e IVA sobre un costo base ya calculado.

        Demuestra el encadenamiento de excepciones (`raise ... from ...`) y
        garantiza que el resultado nunca sea negativo o incoherente.
        """
        try:
            # Si hay descuento, se interpreta según su tipo (singledispatch).
            if descuento:
                costo = self._aplicar_descuento(descuento, costo)
            # Si corresponde, se aplica el IVA.
            if aplicar_impuesto:
                costo = costo * (1 + IVA)
        except ParametroInvalidoError:
            # Error de parámetro de descuento: se propaga tal cual.
            raise
        except (TypeError, ValueError) as exc:
            # Cualquier error aritmético se encadena como cálculo inconsistente.
            raise CalculoInconsistenteError(
                "Ocurrió un error al ajustar el costo del servicio."
            ) from exc

        # El costo final nunca puede ser negativo (regla de coherencia).
        if costo < 0:
            raise CalculoInconsistenteError(
                "El costo calculado resultó negativo, lo cual es incoherente."
            )
        return round(costo, 2)


# ---------------------------------------------------------------------------
# Servicio especializado 1: Reserva de Sala
# ---------------------------------------------------------------------------
class ReservaSala(Servicio):
    """Servicio de reserva de una sala (depende de capacidad y horas)."""

    def __init__(self, id_entidad, costo_base, capacidad, horas, disponible=True):
        super().__init__(id_entidad, "Reserva de Sala", costo_base, disponible)
        self.capacidad = capacidad
        self.horas = horas

    def validar_parametros(self):
        # La capacidad debe ser un entero positivo.
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ParametroInvalidoError(
                "La capacidad debe ser un entero positivo."
            )
        # Las horas deben ser un valor numérico positivo.
        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise ParametroInvalidoError(
                "Las horas deben ser un valor positivo."
            )
        return True

    def calcular_costo(self, aplicar_impuesto=False, descuento=0.0):
        # Se validan los parámetros antes de calcular (polimorfismo).
        self.validar_parametros()
        # Costo base por cada hora reservada.
        costo = self.costo_base * self.horas
        return self._ajustar_costo(costo, aplicar_impuesto, descuento)

    def describir(self):
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Servicio #{self.id} - Reserva de Sala "
            f"(capacidad={self.capacidad}, horas={self.horas}, {estado})"
        )


# ---------------------------------------------------------------------------
# Servicio especializado 2: Alquiler de Equipos
# ---------------------------------------------------------------------------
class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos (depende de cantidad y días)."""

    def __init__(self, id_entidad, costo_base, tipo_equipo, cantidad, dias,
                 disponible=True):
        super().__init__(id_entidad, "Alquiler de Equipos", costo_base, disponible)
        self.tipo_equipo = tipo_equipo
        self.cantidad = cantidad
        self.dias = dias

    def validar_parametros(self):
        # El tipo de equipo es obligatorio.
        if not isinstance(self.tipo_equipo, str) or not self.tipo_equipo.strip():
            raise ParametroInvalidoError("El tipo de equipo es obligatorio.")
        # La cantidad debe ser un entero positivo.
        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ParametroInvalidoError(
                "La cantidad debe ser un entero positivo."
            )
        # Los días deben ser un entero positivo.
        if not isinstance(self.dias, int) or self.dias <= 0:
            raise ParametroInvalidoError("Los días deben ser un entero positivo.")
        return True

    def calcular_costo(self, aplicar_impuesto=False, descuento=0.0):
        self.validar_parametros()
        # Costo base por equipo y por día.
        costo = self.costo_base * self.cantidad * self.dias
        return self._ajustar_costo(costo, aplicar_impuesto, descuento)

    def describir(self):
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Servicio #{self.id} - Alquiler de Equipos "
            f"({self.cantidad} x {self.tipo_equipo}, {self.dias} día(s), {estado})"
        )


# ---------------------------------------------------------------------------
# Servicio especializado 3: Asesoría Especializada
# ---------------------------------------------------------------------------
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría (el nivel experto encarece el costo)."""

    # Factor multiplicador aplicado cuando la asesoría es de nivel experto.
    FACTOR_EXPERTO = 1.5

    def __init__(self, id_entidad, costo_base, area, horas, nivel_experto=False,
                 disponible=True):
        super().__init__(id_entidad, "Asesoría Especializada", costo_base,
                         disponible)
        self.area = area
        self.horas = horas
        self.nivel_experto = nivel_experto

    def validar_parametros(self):
        # El área de asesoría es obligatoria.
        if not isinstance(self.area, str) or not self.area.strip():
            raise ParametroInvalidoError("El área de asesoría es obligatoria.")
        # Las horas deben ser un valor numérico positivo.
        if not isinstance(self.horas, (int, float)) or self.horas <= 0:
            raise ParametroInvalidoError("Las horas deben ser un valor positivo.")
        # El nivel experto debe ser un valor booleano.
        if not isinstance(self.nivel_experto, bool):
            raise ParametroInvalidoError("El nivel experto debe ser booleano.")
        return True

    def calcular_costo(self, aplicar_impuesto=False, descuento=0.0):
        self.validar_parametros()
        # Costo base por hora de asesoría.
        costo = self.costo_base * self.horas
        # Si es de nivel experto, se aplica el factor de recargo.
        if self.nivel_experto:
            costo *= self.FACTOR_EXPERTO
        return self._ajustar_costo(costo, aplicar_impuesto, descuento)

    def describir(self):
        estado = "disponible" if self.disponible else "no disponible"
        nivel = "experto" if self.nivel_experto else "estándar"
        return (
            f"Servicio #{self.id} - Asesoría Especializada "
            f"(área={self.area}, horas={self.horas}, nivel={nivel}, {estado})"
        )
