"""
Módulo de Reservas para Software FJ.
Gestiona el ciclo de vida de una reserva asociando Clientes y Servicios.
"""

from modelos.entidades import Cliente, Servicio
from excepciones.errores import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)
from utilidades.logger import registrar_evento


class Reserva:
    """Clase que representa una reserva dentro del sistema."""

    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, unidades: int):
        if not id_reserva or not str(id_reserva).strip():
            raise ReservaInvalidaError("El identificador de la reserva no puede estar vacío.")

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre_servicio}' no se encuentra disponible."
            )

        self._id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.unidades = unidades
        self.costo_total = servicio.calcular_costo(unidades)
        self.estado = self.ESTADO_CONFIRMADA

        # El servicio queda ocupado
        self.servicio.disponible = False

        registrar_evento(
            "INFO",
            f"Reserva creada [{self._id_reserva}]: Cliente {self.cliente.id_entidad} reservó '{self.servicio.nombre_servicio}' por ${self.costo_total:.2f}",
        )

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    def cancelar_reserva(self) -> None:
        """Cancela la reserva y libera el servicio asignado."""
        if self.estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError(
                f"La reserva [{self._id_reserva}] ya se encuentra cancelada."
            )

        self.estado = self.ESTADO_CANCELADA
        self.servicio.disponible = True

        registrar_evento(
            "INFO",
            f"Reserva cancelada [{self._id_reserva}]: Servicio '{self.servicio.nombre_servicio}' liberado.",
        )

    def mostrar_detalle(self) -> str:
        return (
            f"Reserva [{self._id_reserva}] - Estado: {self.estado}\n"
            f"  {self.cliente.mostrar_detalle()}\n"
            f"  {self.servicio.mostrar_detalle()}\n"
            f"  Unidades: {self.unidades} | Total a pagar: ${self.costo_total:.2f}"
        )