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


