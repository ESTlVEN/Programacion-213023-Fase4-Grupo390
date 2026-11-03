"""
Módulo de Entidades para Software FJ.
Define la jerarquía de clases: Clientes y Servicios con Programación Orientada a Objetos.
"""

from abc import ABC, abstractmethod
from excepciones.errores import ClienteInvalidoError, ParametroServicioInvalidoError


class EntidadBase(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def mostrar_detalle(self) -> str:
        """Devuelve una descripción legible de la entidad."""
        pass


class Cliente(EntidadBase):
    """Representa a un cliente con validación y encapsulamiento."""

    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    def mostrar_detalle(self) -> str:
        return f"Cliente [{self.id_entidad}] - Nombre: {self.nombre} | Correo: {self.correo}"


class Servicio(EntidadBase):
    """Clase abstracta base para los servicios de Software FJ."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float):
        super().__init__(id_servicio)
        if tarifa_base <= 0:
            raise ParametroServicioInvalidoError("La tarifa base debe ser mayor a 0.")
        self.nombre_servicio = nombre_servicio
        self._tarifa_base = tarifa_base
        self.disponible = True

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self, unidades: int) -> float:
        """Calcula el costo total en base a la unidad de medida específica."""
        pass


class ReservaSala(Servicio):
    """Servicio de salas calculado por horas."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_por_hora: float, capacidad: int):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_hora)
        if capacidad <= 0:
            raise ParametroServicioInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        self.capacidad = capacidad

    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ParametroServicioInvalidoError("Las horas de reserva deben ser mayores a 0.")
        return self.tarifa_base * horas

    def mostrar_detalle(self) -> str:
        return f"Sala [{self.id_entidad}] {self.nombre_servicio} - Capacidad: {self.capacidad} pers. - Tarifa/h: ${self.tarifa_base:.2f}"


class AlquilerEquipo(Servicio):
    """Servicio de equipos calculado por días con valor de seguro."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_por_dia: float, seguro: float = 0.0):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_dia)
        if seguro < 0:
            raise ParametroServicioInvalidoError("El valor del seguro no puede ser negativo.")
        self.seguro = seguro

    def calcular_costo(self, dias: int) -> float:
        if dias <= 0:
            raise ParametroServicioInvalidoError("Los días de alquiler deben ser mayores a 0.")
        return (self.tarifa_base * dias) + self.seguro

    def mostrar_detalle(self) -> str:
        return f"Equipo [{self.id_entidad}] {self.nombre_servicio} - Tarifa/día: ${self.tarifa_base:.2f} - Seguro: ${self.seguro:.2f}"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría calculado por cantidad de sesiones."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_por_sesion: float, area_especialidad: str):
        super().__init__(id_servicio, nombre_servicio, tarifa_por_sesion)
        self.area_especialidad = area_especialidad

    def calcular_costo(self, sesiones: int) -> float:
        if sesiones <= 0:
            raise ParametroServicioInvalidoError("La cantidad de sesiones debe ser mayor a 0.")
        return self.tarifa_base * sesiones

    def mostrar_detalle(self) -> str:
        return f"Asesoría [{self.id_entidad}] {self.nombre_servicio} ({self.area_especialidad}) - Tarifa/sesión: ${self.tarifa_base:.2f}"