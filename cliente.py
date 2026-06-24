"""
Módulo del cliente del sistema "Software FJ".

Define la clase `Cliente`, que encapsula los datos personales mediante atributos
privados (`__nombre`, `__documento`, `__correo`, `__telefono`) expuestos por
*properties* con validaciones robustas. Cualquier dato inválido genera
`ClienteInvalidoError` o `DatoInvalidoError`.
"""

import re

from entidad_base import EntidadBase
from excepciones import ClienteInvalidoError, DatoInvalidoError


class Cliente(EntidadBase):
    """Representa a un cliente con sus datos personales validados."""

    # Expresiones regulares precompiladas para validar los datos del cliente.
    _PATRON_NOMBRE = re.compile(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+")
    _PATRON_DOCUMENTO = re.compile(r"\d{6,10}")
    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
    _PATRON_TELEFONO = re.compile(r"\d{7,15}")

    def __init__(self, id_entidad, nombre, documento, correo, telefono):
        """Inicializa el cliente; cada asignación valida mediante su setter."""
        super().__init__(id_entidad)
        # Al asignar a las properties se ejecutan las validaciones de inmediato.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ----- Propiedad: nombre -------------------------------------------------
    @property
    def nombre(self):
        """Nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre no puede estar vacío.
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        # El nombre solo admite letras (incluidas tildes y ñ) y espacios.
        if not self._PATRON_NOMBRE.fullmatch(valor.strip()):
            raise DatoInvalidoError(
                "El nombre solo puede contener letras y espacios."
            )
        self.__nombre = valor.strip()

    # ----- Propiedad: documento ---------------------------------------------
    @property
    def documento(self):
        """Documento de identidad (cadena numérica de 6 a 10 dígitos)."""
        return self.__documento

    @documento.setter
    def documento(self, valor):
        texto = str(valor).strip()
        # El documento debe ser numérico y tener entre 6 y 10 dígitos.
        if not self._PATRON_DOCUMENTO.fullmatch(texto):
            raise ClienteInvalidoError(
                "El documento debe ser numérico de 6 a 10 dígitos."
            )
        self.__documento = texto

    # ----- Propiedad: correo -------------------------------------------------
    @property
    def correo(self):
        """Correo electrónico validado por expresión regular."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # El correo debe cumplir el patrón usuario@dominio.extension.
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise DatoInvalidoError("El correo no tiene un formato válido.")
        self.__correo = valor.strip()

    # ----- Propiedad: telefono ----------------------------------------------
    @property
    def telefono(self):
        """Teléfono de contacto (cadena numérica de 7 a 15 dígitos)."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        # El teléfono debe ser numérico.
        if not self._PATRON_TELEFONO.fullmatch(texto):
            raise DatoInvalidoError(
                "El teléfono debe ser numérico (7 a 15 dígitos)."
            )
        self.__telefono = texto

    # ----- Métodos heredados de EntidadBase ---------------------------------
    def describir(self):
        """Devuelve una descripción legible del cliente."""
        return (
            f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )

    def validar(self):
        """
        Revalida todos los datos reasignándolos a sus properties.

        Al reasignar cada atributo se vuelven a ejecutar las validaciones; si
        alguno fuese inválido se lanzaría la excepción correspondiente.
        """
        self.nombre = self.__nombre
        self.documento = self.__documento
        self.correo = self.__correo
        self.telefono = self.__telefono
        return True