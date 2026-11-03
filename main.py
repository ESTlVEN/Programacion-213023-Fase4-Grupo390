"""
Punto de Entrada Principal - Software FJ.
Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Gestión de datos en memoria y registro de eventos.
"""

from excepciones.errores import (
    SoftwareFJException,
    ClienteInvalidoError,
    ParametroServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)
from utilidades.logger import registrar_evento
from modelos.entidades import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva

# Estructuras de almacenamiento en memoria (Restricción: Sin Base de Datos)
clientes = []
servicios = []
reservas = []


def precargar_servicios_demo():
    """Carga inicial de servicios en memoria para pruebas rápidas."""
    servicios.append(ReservaSala("S01", "Sala de Juntas Ejecutiva", 50000.0, 10))
    servicios.append(AlquilerEquipo("E01", "Videoproyector Láser 4K", 30000.0, 15000.0))
    servicios.append(AsesoriaEspecializada("A01", "Asesoría Redes y Telecom", 80000.0, "Redes"))
    registrar_evento("INFO", "Servicios iniciales precargados en memoria.")


def registrar_cliente_interactivo():
    print("\n--- REGISTRAR NUEVO CLIENTE ---")
    id_cli = input("Ingrese documento/ID del cliente: ").strip()
    nombre = input("Ingrese nombre completo: ").strip()
    correo = input("Ingrese correo electrónico: ").strip()

    try:
        nuevo_cliente = Cliente(id_cli, nombre, correo)
        clientes.append(nuevo_cliente)
        registrar_evento("INFO", f"Cliente registrado exitosamente: [{id_cli}] {nombre}")
        print("✔ Cliente registrado exitosamente.")
    except ClienteInvalidoError as error:
        registrar_evento("ERROR", f"Fallo al registrar cliente: {error}")
        print(f"✖ Error de Validación: {error}")


def listar_clientes_interactivo():
    print("\n--- LISTA DE CLIENTES ---")
    if not clientes:
        print("No hay clientes registrados en memoria.")
        return
    for c in clientes:
        print(f"- {c.mostrar_detalle()}")


def listar_servicios_interactivo():
    print("\n--- CATÁLOGO DE SERVICIOS ---")
    if not servicios:
        print("No hay servicios disponibles.")
        return
    for s in servicios:
        estado = "DISPONIBLE" if s.disponible else "OCUPADO"
        print(f"- {s.mostrar_detalle()} | Estado: {estado}")


def crear_reserva_interactiva():
    print("\n--- CREAR RESERVA ---")
    if not clientes:
        print("✖ Debe registrar al menos un cliente antes de reservar.")
        return

    listar_servicios_interactivo()
    id_srv = input("\nIngrese el ID del servicio a reservar: ").strip()
    servicio_elegido = next((s for s in servicios if s.id_entidad == id_srv), None)

    if not servicio_elegido:
        print("✖ Servicio no encontrado.")
        return

    listar_clientes_interactivo()
    id_cli = input("\nIngrese el ID del cliente que reserva: ").strip()
    cliente_elegido = next((c for c in clientes if c.id_entidad == id_cli), None)

    if not cliente_elegido:
        print("✖ Cliente no encontrado.")
        return

    try:
        unidades = int(input("Ingrese la cantidad de unidades (horas / días / sesiones): "))
        id_res = f"RES-{len(reservas) + 1:03d}"
        nueva_reserva = Reserva(id_res, cliente_elegido, servicio_elegido, unidades)
        reservas.append(nueva_reserva)
        print(f"\n✔ Reserva realizada con éxito.")
        print(nueva_reserva.mostrar_detalle())
    except (SoftwareFJException, ValueError) as error:
        registrar_evento("ERROR", f"Error creando reserva: {error}")
        print(f"✖ Error al procesar reserva: {error}")


def cancelar_reserva_interactiva():
    print("\n--- CANCELAR RESERVA ---")
    if not reservas:
        print("No existen reservas en memoria.")
        return

    listar_reservas_interactivo()
    id_res = input("\nIngrese el código de la reserva a cancelar: ").strip()
    reserva_obj = next((r for r in reservas if r.id_reserva == id_res), None)

    if not reserva_obj:
        print("✖ Reserva no encontrada.")
        return

    try:
        reserva_obj.cancelar_reserva()
        print("✔ Reserva cancelada y servicio liberado correctamente.")
    except OperacionNoPermitidaError as error:
        registrar_evento("ADVERTENCIA", f"Intento no permitido en reserva {id_res}: {error}")
        print(f"✖ Error: {error}")


def listar_reservas_interactivo():
    print("\n--- HISTORIAL DE RESERVAS ---")
    if not reservas:
        print("No hay reservas registradas.")
        return
    for r in reservas:
        print("--------------------------------------------------")
        print(r.mostrar_detalle())


def main():
    precargar_servicios_demo()

    while True:
        print("\n===========================================")
        print("       SOFTWARE FJ - SISTEMA INTEGRADO     ")
        print("===========================================")
        print("1. Registrar Cliente")
        print("2. Listar Clientes")
        print("3. Listar Servicios y Disponibilidad")
        print("4. Crear Nueva Reserva")
        print("5. Cancelar Reserva")
        print("6. Listar Historial de Reservas")
        print("7. Salir")
        print("===========================================")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            registrar_cliente_interactivo()
        elif opcion == "2":
            listar_clientes_interactivo()
        elif opcion == "3":
            listar_servicios_interactivo()
        elif opcion == "4":
            crear_reserva_interactiva()
        elif opcion == "5":
            cancelar_reserva_interactiva()
        elif opcion == "6":
            listar_reservas_interactivo()
        elif opcion == "7":
            registrar_evento("INFO", "Cierre de sesión del sistema Software FJ.")
            print("\nGracias por utilizar Software FJ. Saliendo...")
            break
        else:
            print("✖ Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()