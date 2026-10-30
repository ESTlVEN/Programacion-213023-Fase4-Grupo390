"""
Módulo de Excepciones Personalizadas para Software FJ.
Define la jerarquía de errores para controlar las reglas de negocio.
"""

class SoftwareFJException(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass


class ClienteInvalidoError(SoftwareFJException):
    """Se lanza cuando los datos de un cliente no cumplen con las validaciones."""
    pass


class ParametroServicioInvalidoError(SoftwareFJException):
    """Se lanza cuando los parámetros de un servicio (precio, capacidad, tiempo) son erróneos."""
    pass


class ServicioNoDisponibleError(SoftwareFJException):
    """Se lanza cuando se solicita un servicio que no tiene disponibilidad o cupo."""
    pass


class ReservaInvalidaError(SoftwareFJException):
    """Se lanza cuando una reserva no cuenta con los datos o entidades requeridas."""
    pass


class OperacionNoPermitidaError(SoftwareFJException):
    """Se lanza cuando se intenta realizar una transición de estado ilegal en una reserva."""
    pass