"""
Módulo de Reservas para Software FJ.
Gestiona el ciclo de vida completo de una reserva: confirmación, procesamiento y cancelación.
"""

from modelos.entidades import EntidadBase, Cliente, Servicio
from excepciones.errores import (
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)
from utilidades.logger import registrar_evento


class Reserva(EntidadBase):
    """Clase que integra Cliente, Servicio, duración (unidades) y estado."""

    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_PROCESADA = "PROCESADA"
    ESTADO_CANCELADA = "CANCELADA"

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        unidades: float,
        confirmar_inmediatamente: bool = True,
    ):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.unidades = unidades
        self.estado = self.ESTADO_PENDIENTE
        self.costo_total = 0.0

        self.validar_parametros()

        # Costo base preliminar usando la variante 1 del método sobrecargado
        self.costo_total = self.servicio.calcular_costo(self.unidades)

        if confirmar_inmediatamente:
            self.confirmar_reserva()
        else:
            registrar_evento(
                "INFO",
                f"Reserva creada en estado PENDIENTE [{self.id_entidad}] para cliente {self.cliente.id_entidad}.",
            )

    @property
    def id_reserva(self) -> str:
        return self.id_entidad

    def validar_parametros(self) -> None:
        if self.cliente is None or self.servicio is None:
            raise ParametroFaltanteError("Cliente y Servicio son obligatorios para crear una reserva.")

        if not isinstance(self.cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Cliente.")

        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre_servicio}' [{self.servicio.id_entidad}] no está disponible."
            )

        try:
            self.unidades = float(self.unidades)
        except (ValueError, TypeError) as err:
            raise ReservaInvalidaError("Las unidades de duración deben ser un valor numérico.") from err

        if self.unidades <= 0:
            raise ReservaInvalidaError(f"La duración debe ser mayor a 0 (Recibido: {self.unidades}).")

    def confirmar_reserva(self) -> None:
        """Confirma una reserva pendiente y bloquea la disponibilidad del servicio."""
        if self.estado != self.ESTADO_PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se pueden confirmar reservas en estado PENDIENTE (Estado actual: {self.estado})."
            )
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre_servicio}' ya fue ocupado por otra reserva."
            )

        self.estado = self.ESTADO_CONFIRMADA
        self.servicio.disponible = False
        registrar_evento(
            "INFO",
            f"Reserva CONFIRMADA [{self.id_entidad}]: Cliente {self.cliente.id_entidad} -> "
            f"'{self.servicio.nombre_servicio}' (Costo base: ${self.costo_total:,.2f}).",
        )

    def procesar_reserva(
        self,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_adicional: float = 0.0,
    ) -> float:
        """
        Procesa financieramente la reserva aplicando sobrecarga de costos
        (impuestos, descuentos y recargos) y libera el servicio tras su culminación.
        """
        if self.estado != self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva [{self.id_entidad}] porque su estado es '{self.estado}' (Requiere CONFIRMADA)."
            )

        try:
            self.costo_total = self.servicio.calcular_costo(
                unidades=self.unidades,
                impuesto=impuesto,
                descuento=descuento,
                recargo_adicional=recargo_adicional,
            )
        except CalculoInconsistenteError as error_calc:
            # Encadenamiento explícito de excepciones (Requisito de rúbrica)
            raise CalculoInconsistenteError(
                f"Fallo al liquidar el cobro final de la reserva [{self.id_entidad}]."
            ) from error_calc

        self.estado = self.ESTADO_PROCESADA
        self.servicio.disponible = True
        registrar_evento(
            "INFO",
            f"Reserva PROCESADA [{self.id_entidad}]: Total facturado ${self.costo_total:,.2f} "
            f"(IVA: {impuesto*100:.0f}%, Desc: {descuento*100:.0f}%, Recargo: ${recargo_adicional:,.0f}). Servicio liberado.",
        )
        return self.costo_total

    def cancelar_reserva(self) -> None:
        """Cancela la reserva y libera el servicio si estaba bloqueado."""
        if self.estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id_entidad}] ya se encuentra cancelada."
            )
        if self.estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva [{self.id_entidad}] porque ya fue procesada y facturada."
            )

        if self.estado == self.ESTADO_CONFIRMADA:
            self.servicio.disponible = True

        self.estado = self.ESTADO_CANCELADA
        registrar_evento(
            "INFO",
            f"Reserva CANCELADA [{self.id_entidad}]: Servicio '{self.servicio.nombre_servicio}' liberado.",
        )

    def mostrar_detalle(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] - Estado: {self.estado}\n"
            f"  {self.cliente.mostrar_detalle()}\n"
            f"  {self.servicio.mostrar_detalle()}\n"
            f"  Unidades: {self.unidades} | Total: ${self.costo_total:,.2f}"
        )