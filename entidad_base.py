"""
Módulo de la entidad base abstracta del sistema "Software FJ".

Define la clase abstracta `EntidadBase`, superclase común de `Cliente`,
`Servicio` y `Reserva`. Obliga a las subclases a implementar los métodos
`describir()` y `validar()`, garantizando así una interfaz uniforme en todo el
dominio (principio de polimorfismo).
"""

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Clase base abstracta para todas las entidades del dominio."""

    def __init__(self, id_entidad):
        """
        Inicializa la entidad con su identificador.

        :param id_entidad: Identificador único de la entidad.
        """
        # Identificador común a todas las subclases (atributo `id`).
        self.id = id_entidad

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad (a implementar)."""
        raise NotImplementedError

    @abstractmethod
    def validar(self):
        """Valida la coherencia interna de la entidad (a implementar)."""
        raise NotImplementedError
