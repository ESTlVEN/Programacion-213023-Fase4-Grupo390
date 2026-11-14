"""
Módulo de Utilidades de Registro (Logger) para Software FJ.
Gestiona la escritura y lectura de eventos y errores en archivo plano sin usar base de datos.
"""

import datetime
import os

ARCHIVO_LOG = "sistema_eventos.log"


def registrar_evento(nivel: str, mensaje: str, causa: Exception = None) -> None:
    """
    Registra un evento o error en el archivo de logs usando try/except/finally.
    """
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detalle_causa = ""
    if causa is not None:
        detalle_causa = f" | Causa raíz ({type(causa).__name__}): {causa}"

    linea_log = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}{detalle_causa}\n"

    archivo = None
    try:
        archivo = open(ARCHIVO_LOG, mode="a", encoding="utf-8")
        archivo.write(linea_log)
    except OSError as error_io:
        print(f"Error crítico de escritura en archivo de logs: {error_io}")
    finally:
        # Bloque finally obligatorio: garantiza liberación del archivo
        if archivo is not None and not archivo.closed:
            archivo.close()


def leer_historial_logs() -> str:
    """Lee y retorna el contenido íntegro del archivo de logs."""
    if not os.path.exists(ARCHIVO_LOG):
        return "El archivo de logs aún no contiene registros."

    archivo = None
    try:
        archivo = open(ARCHIVO_LOG, mode="r", encoding="utf-8")
        return archivo.read()
    except OSError as error_io:
        return f"No fue posible leer el archivo de logs: {error_io}"
    finally:
        if archivo is not None and not archivo.closed:
            archivo.close()


def reiniciar_logs() -> None:
    """Limpia el archivo de logs al iniciar una nueva batería de pruebas."""
    archivo = None
    try:
        archivo = open(ARCHIVO_LOG, mode="w", encoding="utf-8")
        archivo.write("=== BITÁCORA OFICIAL DE EVENTOS Y ERRORES - SOFTWARE FJ ===\n")
    except OSError:
        pass
    finally:
        if archivo is not None and not archivo.closed:
            archivo.close()