"""
Módulo de Entidades para Software FJ.
Define la jerarquía de clases: EntidadBase, Cliente y Servicios con POO avanzada.
"""

import re
from abc import ABC, abstractmethod
from excepciones.errores import (
    ParametroFaltanteError,
    ClienteInvalidoError,
    ParametroServicioInvalidoError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Clase abstracta general que representa entidades trazables del sistema."""

    def __init__(self, id_entidad: str):
        self.id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El identificador (ID) de la entidad es obligatorio.")
        self._id_entidad = str(valor).strip().upper()

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los parámetros internos de la entidad."""
        pass

    @abstractmethod
    def mostrar_detalle(self) -> str:
        """Devuelve una descripción legible de la entidad."""
        pass


class Cliente(EntidadBase):
    """Representa a un cliente con validaciones robustas y encapsulamiento de datos."""

    PATRON_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str = "3000000000"):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar_parametros()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        limpio = str(valor).strip()
        if len(limpio) < 3:
            raise ClienteInvalidoError(f"El nombre '{limpio}' debe tener al menos 3 caracteres.")
        self._nombre = limpio

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        limpio = str(valor).strip()
        if not re.match(self.PATRON_EMAIL, limpio):
            raise ClienteInvalidoError(f"El correo '{limpio}' no tiene un formato válido.")
        self._correo = limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        limpio = str(valor).strip()
        if not limpio.isdigit() or not (7 <= len(limpio) <= 12):
            raise ClienteInvalidoError(
                f"El teléfono '{limpio}' debe contener solo números (7 a 12 dígitos)."
            )
        self._telefono = limpio

    def validar_parametros(self) -> None:
        if not self._nombre or not self._correo or not self._telefono:
            raise ParametroFaltanteError("Faltan datos personales obligatorios en el cliente.")

    def mostrar_detalle(self) -> str:
        return (
            f"Cliente [{self.id_entidad}] - Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        self._nombre_servicio = str(valor).strip()

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            tarifa_num = float(valor)
        except (ValueError, TypeError) as err_tipo:
            # Encadenamiento de excepciones (Exception Chaining)
            raise ParametroServicioInvalidoError(
                f"La tarifa base debe ser un número válido (Recibido: '{valor}')."
            ) from err_tipo

        if tarifa_num <= 0:
            raise ParametroServicioInvalidoError(
                f"La tarifa base debe ser mayor a 0 (Recibido: {tarifa_num})."
            )
        self._tarifa_base = tarifa_num

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self) -> None:
        """Método polimórfico para validar parámetros específicos de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, unidades: float) -> float:
        """Método polimórfico que calcula el costo base según el tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método polimórfico que describe las características del servicio."""
        pass

    # SOBRECARGA DE MÉTODOS mediante parámetros opcionales con valores por defecto
    def calcular_costo(
        self,
        unidades: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
        recargo_adicional: float = 0.0,
    ) -> float:
        """
        Calcula el costo total soportando múltiples variantes (Sobrecarga):
        - Variante 1: calcular_costo(unidades) -> retorna el costo base puro.
        - Variante 2: calcular_costo(unidades, impuesto=0.19) -> aplica IVA.
        - Variante 3: calcular_costo(unidades, impuesto, descuento, recargo_adicional) -> completo.
        """
        try:
            u_num = float(unidades)
            imp_num = float(impuesto)
            desc_num = float(descuento)
            rec_num = float(recargo_adicional)
        except (ValueError, TypeError) as err_conv:
            raise CalculoInconsistenteError(
                "Los parámetros para el cálculo de costos deben ser valores numéricos."
            ) from err_conv

        if u_num <= 0:
            raise ParametroServicioInvalidoError(
                f"Las unidades de duración deben ser mayores a 0 (Recibido: {u_num})."
            )
        if not (0.0 <= imp_num <= 0.50):
            raise CalculoInconsistenteError(
                f"Impuesto inconsistente ({imp_num * 100:.1f}%). Rango permitido: 0% a 50%."
            )
        if not (0.0 <= desc_num < 1.0):
            raise CalculoInconsistenteError(
                f"Descuento inconsistente ({desc_num * 100:.1f}%). Rango permitido: 0% a 99%."
            )
        if rec_num < 0:
            raise CalculoInconsistenteError("El recargo adicional no puede ser negativo.")

        subtotal = self.calcular_costo_base(u_num)
        valor_descuento = subtotal * desc_num
        base_gravable = subtotal - valor_descuento + rec_num
        total = base_gravable * (1.0 + imp_num)
        return round(total, 2)

    def mostrar_detalle(self) -> str:
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas calculado por horas."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_por_hora: float, capacidad: int):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_hora)
        self.capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self) -> None:
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ParametroServicioInvalidoError(
                f"La capacidad de la sala debe ser un entero mayor a 0 (Recibido: {self.capacidad})."
            )

    def calcular_costo_base(self, horas: float) -> float:
        return self.tarifa_base * horas

    def describir_servicio(self) -> str:
        estado = "DISPONIBLE" if self.disponible else "OCUPADO"
        return (
            f"Sala [{self.id_entidad}] {self.nombre_servicio} - "
            f"Capacidad: {self.capacidad} pers. - Tarifa/h: ${self.tarifa_base:,.2f} [{estado}]"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de equipos calculado por días más seguro."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_por_dia: float, seguro: float = 0.0):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_dia)
        self.seguro = seguro
        self.validar_parametros()

    def validar_parametros(self) -> None:
        try:
            self.seguro = float(self.seguro)
        except (ValueError, TypeError) as err:
            raise ParametroServicioInvalidoError("El valor del seguro debe ser numérico.") from err

        if self.seguro < 0:
            raise ParametroServicioInvalidoError("El valor del seguro no puede ser negativo.")

    def calcular_costo_base(self, dias: float) -> float:
        return (self.tarifa_base * dias) + self.seguro

    def describir_servicio(self) -> str:
        estado = "DISPONIBLE" if self.disponible else "OCUPADO"
        return (
            f"Equipo [{self.id_entidad}] {self.nombre_servicio} - "
            f"Tarifa/día: ${self.tarifa_base:,.2f} - Seguro: ${self.seguro:,.2f} [{estado}]"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Asesoría especializada calculada por sesiones."""

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        tarifa_por_sesion: float,
        area_especialidad: str,
    ):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_sesion)
        self.area_especialidad = area_especialidad
        self.validar_parametros()

    def validar_parametros(self) -> None:
        if not self.area_especialidad or not str(self.area_especialidad).strip():
            raise ParametroFaltanteError("El área de especialidad de la asesoría no puede estar vacía.")
        self.area_especialidad = str(self.area_especialidad).strip()

    def calcular_costo_base(self, sesiones: float) -> float:
        return self.tarifa_base * sesiones

    def describir_servicio(self) -> str:
        estado = "DISPONIBLE" if self.disponible else "OCUPADO"
        return (
            f"Asesoría [{self.id_entidad}] {self.nombre_servicio} "
            f"({self.area_especialidad}) - Tarifa/sesión: ${self.tarifa_base:,.2f} [{estado}]"
        )