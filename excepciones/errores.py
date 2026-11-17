"""
Módulo de Excepciones Personalizadas para Software FJ.
Define la jerarquía de errores para controlar las reglas de negocio.
"""


class SoftwareFJException(Exception):
    """Clase base para todas las excepciones controladas del sistema Software FJ."""
    pass


class ParametroFaltanteError(SoftwareFJException):
    """Se lanza cuando un parámetro obligatorio es nulo o está vacío."""
    pass


class ClienteInvalidoError(SoftwareFJException):
    """Se lanza cuando los datos personales de un cliente no superan las validaciones."""
    pass


class ParametroServicioInvalidoError(SoftwareFJException):
    """Se lanza cuando los parámetros de configuración de un servicio son erróneos."""
    pass


class ServicioNoDisponibleError(SoftwareFJException):
    """Se lanza cuando se solicita reservar un servicio que está ocupado o inactivo."""
    pass


class ReservaInvalidaError(SoftwareFJException):
    """Se lanza cuando una reserva carece de entidades válidas o duración permitida."""
    pass


class OperacionNoPermitidaError(SoftwareFJException):
    """Se lanza cuando se intenta una transición de estado ilegal o un duplicado."""
    pass


class CalculoInconsistenteError(SoftwareFJException):
    """Se lanza cuando se detectan anomalías matemáticas en tarifas, impuestos o descuentos."""
    pass