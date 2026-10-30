"""
Módulo de Registro de Eventos (Logger) para Software FJ.
Gestiona la persistencia en archivo plano .log con marcas de tiempo.
"""

from datetime import datetime

NOMBRE_ARCHIVO_LOG = "sistema_eventos.log"


def registrar_evento(tipo: str, mensaje: str) -> None:
    """
    Registra una entrada en el archivo de log con fecha, hora y nivel de severidad.
    Usa el contexto seguro 'with' para garantizar el cierre del archivo.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha_hora}] [{tipo.upper()}]: {mensaje}\n"

    with open(NOMBRE_ARCHIVO_LOG, mode="a", encoding="utf-8") as archivo:
        archivo.write(linea)
