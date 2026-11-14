"""
Punto de Entrada Principal - Software FJ.
Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Incluye Simulación Automática de 12 Operaciones, Auditoría try/except/else/finally e Interfaz Tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from excepciones.errores import SoftwareFJException
from utilidades.logger import registrar_evento, leer_historial_logs, reiniciar_logs
from modelos.entidades import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva

# Estructuras de almacenamiento en memoria (Sin Base de Datos)
clientes = []
servicios = []
reservas = []

# Métricas de auditoría actualizadas en bloques try / except / else / finally
auditoria = {
    "intentos": 0,
    "exitosas": 0,
    "errores": 0,
}


def registrar_cliente_seguro(id_cli: str, nombre: str, correo: str, telefono: str = "3000000000") -> str:
    """Registra un cliente utilizando bloques try / except / else / finally."""
    try:
        id_limpio = str(id_cli).strip().upper() if id_cli else ""
        if any(c.id_entidad == id_limpio for c in clientes):
            from excepciones.errores import OperacionNoPermitidaError
            raise OperacionNoPermitidaError(f"El cliente con ID '{id_limpio}' ya existe en el sistema.")
        nuevo_cliente = Cliente(id_cli, nombre, correo, telefono)
    except SoftwareFJException as error:
        auditoria["errores"] += 1
        registrar_evento("ERROR", f"Fallo al registrar cliente '{id_cli}': {error}", error.__cause__)
        return f"✖ [ERROR CONTROLADO] {error}"
    else:
        clientes.append(nuevo_cliente)
        auditoria["exitosas"] += 1
        registrar_evento("INFO", f"Cliente registrado exitosamente: {nuevo_cliente.mostrar_detalle()}")
        return f"✔ [OK] {nuevo_cliente.mostrar_detalle()}"
    finally:
        auditoria["intentos"] += 1


def registrar_servicio_seguro(tipo: str, id_srv: str, nombre: str, tarifa: float, param_extra):
    """Crea cualquiera de los 3 servicios especializados aplicando polimorfismo y bloques completos."""
    try:
        id_limpio = str(id_srv).strip().upper() if id_srv else ""
        if any(s.id_entidad == id_limpio for s in servicios):
            from excepciones.errores import OperacionNoPermitidaError
            raise OperacionNoPermitidaError(f"El servicio con ID '{id_limpio}' ya está registrado.")

        tipo_upper = str(tipo).strip().upper()
        if tipo_upper == "SALA":
            nuevo_srv = ReservaSala(id_srv, nombre, tarifa, int(param_extra))
        elif tipo_upper == "EQUIPO":
            nuevo_srv = AlquilerEquipo(id_srv, nombre, tarifa, float(param_extra))
        elif tipo_upper == "ASESORIA":
            nuevo_srv = AsesoriaEspecializada(id_srv, nombre, tarifa, str(param_extra))
        else:
            from excepciones.errores import ParametroServicioInvalidoError
            raise ParametroServicioInvalidoError(f"Tipo de servicio desconocido: '{tipo}'.")
    except (SoftwareFJException, ValueError) as error:
        auditoria["errores"] += 1
        registrar_evento("ERROR", f"Fallo al crear servicio '{id_srv}': {error}", getattr(error, "__cause__", None))
        return f"✖ [ERROR CONTROLADO] {error}"
    else:
        servicios.append(nuevo_srv)
        auditoria["exitosas"] += 1
        registrar_evento("INFO", f"Servicio creado: {nuevo_srv.describir_servicio()}")
        return f"✔ [OK] {nuevo_srv.describir_servicio()}"
    finally:
        auditoria["intentos"] += 1


def crear_reserva_segura(
    id_res: str, id_cli: str, id_srv: str, unidades: float, confirmar_inmediatamente: bool = True
) -> str:
    """Crea una reserva vinculando Cliente y Servicio con manejo de excepciones."""
    try:
        from excepciones.errores import ReservaInvalidaError, OperacionNoPermitidaError

        id_res_limpio = str(id_res).strip().upper() if id_res else ""
        if any(r.id_reserva == id_res_limpio for r in reservas):
            raise OperacionNoPermitidaError(f"El código de reserva '{id_res_limpio}' ya existe.")

        cliente_obj = next((c for c in clientes if c.id_entidad == str(id_cli).strip().upper()), None)
        if not cliente_obj:
            raise ReservaInvalidaError(f"No existe el cliente con ID '{id_cli}'.")

        servicio_obj = next((s for s in servicios if s.id_entidad == str(id_srv).strip().upper()), None)
        if not servicio_obj:
            raise ReservaInvalidaError(f"No existe el servicio con ID '{id_srv}'.")

        nueva_res = Reserva(id_res, cliente_obj, servicio_obj, unidades, confirmar_inmediatamente)
    except SoftwareFJException as error:
        auditoria["errores"] += 1
        registrar_evento("ERROR", f"Fallo al crear reserva '{id_res}': {error}", error.__cause__)
        return f"✖ [ERROR CONTROLADO] {error}"
    else:
        reservas.append(nueva_res)
        auditoria["exitosas"] += 1
        return f"✔ [OK] Reserva [{nueva_res.id_reserva}] creada en estado {nueva_res.estado} | Costo base: ${nueva_res.costo_total:,.2f}"
    finally:
        auditoria["intentos"] += 1


def operar_reserva_segura(
    id_res: str,
    accion: str,
    impuesto: float = 0.19,
    descuento: float = 0.0,
    recargo_adicional: float = 0.0,
) -> str:
    """Ejecuta CONFIRMAR, PROCESAR o CANCELAR sobre una reserva existente."""
    try:
        from excepciones.errores import ReservaInvalidaError, OperacionNoPermitidaError

        reserva_obj = next((r for r in reservas if r.id_reserva == str(id_res).strip().upper()), None)
        if not reserva_obj:
            raise ReservaInvalidaError(f"Reserva '{id_res}' no encontrada.")

        accion_up = accion.strip().upper()
        if accion_up == "CONFIRMAR":
            reserva_obj.confirmar_reserva()
            msg = f"Reserva [{reserva_obj.id_reserva}] CONFIRMADA y servicio bloqueado."
        elif accion_up == "PROCESAR":
            total = reserva_obj.procesar_reserva(impuesto, descuento, recargo_adicional)
            msg = (
                f"Reserva [{reserva_obj.id_reserva}] PROCESADA | Total con sobrecarga: ${total:,.2f} "
                f"(IVA={float(impuesto)*100:.0f}%, Desc={float(descuento)*100:.0f}%, Recargo=${float(recargo_adicional):,.0f})"
            )
        elif accion_up == "CANCELAR":
            reserva_obj.cancelar_reserva()
            msg = f"Reserva [{reserva_obj.id_reserva}] CANCELADA y servicio liberado."
        else:
            raise OperacionNoPermitidaError(f"Acción '{accion}' no válida.")
    except SoftwareFJException as error:
        auditoria["errores"] += 1
        causa_txt = f" | Causa raíz: {error.__cause__}" if error.__cause__ else ""
        registrar_evento("ERROR", f"Error en acción {accion} sobre {id_res}: {error}", error.__cause__)
        return f"✖ [ERROR CONTROLADO] {error}{causa_txt}"
    else:
        auditoria["exitosas"] += 1
        return f"✔ [OK] {msg}"
    finally:
        auditoria["intentos"] += 1


def ejecutar_simulacion_12_operaciones() -> list:
    """
    Simula 12 operaciones completas (válidas e inválidas) demostrando que el
    sistema continúa funcionando ante errores graves sin base de datos.
    """
    reiniciar_logs()
    clientes.clear()
    servicios.clear()
    reservas.clear()
    auditoria["intentos"] = 0
    auditoria["exitosas"] = 0
    auditoria["errores"] = 0

    salida = ["=== SIMULACIÓN AUTOMÁTICA DE 12 OPERACIONES - SOFTWARE FJ ===\n"]

    # Operación 1: Registro exitoso de clientes válidos
    salida.append("1. Registro de Clientes Válidos:")
    salida.append("   " + registrar_cliente_seguro("C01", "George Arteaga", "george.arteaga@unad.edu.co", "3158901234"))
    salida.append("   " + registrar_cliente_seguro("C02", "Camila Vargas", "camila.vargas@empresa.co", "3004567890"))

    # Operación 2: Registro inválido de cliente (Correo sin formato válido)
    salida.append("\n2. Registro Fallido de Cliente (Correo Inválido):")
    salida.append("   " + registrar_cliente_seguro("C03", "Pedro Gómez", "pedro_correo_invalido.com", "3101234567"))

    # Operación 3: Registro inválido de cliente (Parámetro faltante: Nombre vacío)
    salida.append("\n3. Registro Fallido de Cliente (Parámetro Faltante - Nombre vacío):")
    salida.append("   " + registrar_cliente_seguro("C04", "   ", "usuario@correo.com", "3119876543"))

    # Operación 4: Creación correcta de los 3 servicios especializados (Polimorfismo)
    salida.append("\n4. Creación Correcta de los 3 Servicios Especializados:")
    salida.append("   " + registrar_servicio_seguro("SALA", "S01", "Sala de Juntas Ejecutiva", 50000.0, 10))
    salida.append("   " + registrar_servicio_seguro("EQUIPO", "E01", "Videoproyector Láser 4K", 30000.0, 15000.0))
    salida.append("   " + registrar_servicio_seguro("ASESORIA", "A01", "Asesoría Redes y Telecom", 80000.0, "Redes"))

    # Operación 5: Creación incorrecta de servicios (Tarifa negativa y Seguro negativo)
    salida.append("\n5. Creación Fallida de Servicios (Tarifa Negativa y Seguro Negativo):")
    salida.append("   " + registrar_servicio_seguro("SALA", "S02", "Sala Auxiliar", -25000.0, 8))
    salida.append("   " + registrar_servicio_seguro("EQUIPO", "E02", "Portátil Workstation", 45000.0, -5000.0))

    # Operación 6: Reserva exitosa sobre Sala S01 y bloqueo automático
    salida.append("\n6. Reserva Exitosa RES-001 (Sala S01 por 4 horas - Bloquea disponibilidad):")
    salida.append("   " + crear_reserva_segura("RES-001", "C01", "S01", 4, confirmar_inmediatamente=True))

    # Operación 7: Intento fallido de reservar Sala S01 mientras está ocupada
    salida.append("\n7. Intento Fallido de Reserva sobre Servicio No Disponible (Sala S01 ocupada):")
    salida.append("   " + crear_reserva_segura("RES-002", "C02", "S01", 2, confirmar_inmediatamente=True))

    # Operación 8: Procesamiento exitoso de RES-001 con Sobrecarga (IVA 19%) y liberación de Sala S01
    salida.append("\n8. Procesamiento Exitoso de RES-001 con Sobrecarga (IVA 19%):")
    salida.append("   " + operar_reserva_segura("RES-001", "PROCESAR", impuesto=0.19))

    # Operación 9: Reserva en estado PENDIENTE e intento no permitido de procesarla sin confirmar
    salida.append("\n9. Intento de Procesar Reserva RES-003 en Estado PENDIENTE (Operación No Permitida):")
    salida.append("   " + crear_reserva_segura("RES-003", "C02", "A01", 3, confirmar_inmediatamente=False))
    salida.append("   " + operar_reserva_segura("RES-003", "PROCESAR", impuesto=0.19))

    # Operación 10: Confirmación de RES-003 y prueba de Encadenamiento de Excepciones (Descuento 130%)
    salida.append("\n10. Confirmación de RES-003 y Prueba de Encadenamiento de Excepciones (Descuento 130%):")
    salida.append("   " + operar_reserva_segura("RES-003", "CONFIRMAR"))
    salida.append("   " + operar_reserva_segura("RES-003", "PROCESAR", impuesto=0.19, descuento=1.30))

    # Operación 11: Liquidación exitosa de RES-003 con Sobrecarga Completa (IVA 19%, Desc 10%, Recargo $20,000)
    salida.append("\n11. Recuperación y Procesamiento Exitoso de RES-003 (Sobrecarga con IVA, Descuento y Recargo):")
    salida.append("   " + operar_reserva_segura("RES-003", "PROCESAR", impuesto=0.19, descuento=0.10, recargo_adicional=20000.0))

    # Operación 12: Creación y cancelación exitosa de RES-004 + intento prohibido de volver a cancelar
    salida.append("\n12. Cancelación Exitosa de RES-004 e Intento Prohibido de Doble Cancelación:")
    salida.append("   " + crear_reserva_segura("RES-004", "C01", "E01", 2, confirmar_inmediatamente=True))
    salida.append("   " + operar_reserva_segura("RES-004", "CANCELAR"))
    salida.append("   " + operar_reserva_segura("RES-004", "CANCELAR"))

    salida.append(
        f"\n=== RESUMEN DE AUDITORÍA (finally) -> Intentos: {auditoria['intentos']} | "
        f"Exitosas (else): {auditoria['exitosas']} | Errores Controlados (except): {auditoria['errores']} ==="
    )
    return salida


class InterfazSoftwareFJ:
    """Interfaz Gráfica de Usuario en Tkinter para operar y auditar Software FJ."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión (Fase 4)")
        self.root.geometry("960x740")
        self.root.resizable(False, False)
        self._construir_interfaz()
        self.ejecutar_simulacion_gui()

    def _construir_interfaz(self):
        # Encabezado
        header = tk.Frame(self.root, bg="#0F172A", pady=8)
        header.pack(fill="x")
        tk.Label(
            header,
            text="SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#0F172A",
        ).pack()
        tk.Label(
            header,
            text="Arquitectura Modular POO | Sobrecarga | Encadenamiento de Excepciones | try/except/else/finally",
            font=("Arial", 9),
            fg="#94A3B8",
            bg="#0F172A",
        ).pack()

        # Barra de estado y botón de simulación
        barra_top = tk.Frame(self.root, bg="#E2E8F0", pady=6, padx=15)
        barra_top.pack(fill="x")
        self.lbl_auditoria = tk.Label(
            barra_top,
            text="Auditoría (finally): Intentos: 0 | Exitosas: 0 | Errores: 0",
            font=("Consolas", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
        )
        self.lbl_auditoria.pack(side="left")

        tk.Button(
            barra_top,
            text="▶ Ejecutar 12 Operaciones de Simulación",
            font=("Arial", 9, "bold"),
            bg="#2563EB",
            fg="white",
            padx=10,
            command=self.ejecutar_simulacion_gui,
        ).pack(side="right")

        # Pestañas
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=6)

        self.tab_sim = tk.Frame(self.tabs)
        self.tab_gestion = tk.Frame(self.tabs)
        self.tab_logs = tk.Frame(self.tabs)

        self.tabs.add(self.tab_sim, text="1. Simulación (12 Operaciones)")
        self.tabs.add(self.tab_gestion, text="2. Panel Interactivo (Clientes, Servicios y Reservas)")
        self.tabs.add(self.tab_logs, text="3. Visor de Archivo (sistema_eventos.log)")

        # Pestaña 1: Consola de Simulación
        self.txt_sim = scrolledtext.ScrolledText(self.tab_sim, font=("Consolas", 9), bg="#0F172A", fg="#F8FAFC")
        self.txt_sim.pack(fill="both", expand=True, padx=6, pady=6)

        # Pestaña 2: Gestión Interactiva y Tablas
        self._construir_tab_gestion()

        # Pestaña 3: Archivo de Logs
        self.txt_logs = scrolledtext.ScrolledText(self.tab_logs, font=("Consolas", 9), bg="#FFFBEB", fg="#1E293B")
        self.txt_logs.pack(fill="both", expand=True, padx=6, pady=6)

        # Marca de agua institucional
        tk.Label(
            self.root,
            text=(
                "Presentado por: George Steven Arteaga Guzman y Jesus Steven Rodriguez Lopez | Curso: Programación (213023) - UNAD\n"
                "Fase 4 - Componente práctico - Prácticas simuladas | Fecha de entrega: 22 de noviembre de 2026"
            ),
            font=("Arial", 8, "italic"),
            fg="gray40",
            justify="center",
        ).pack(side="bottom", pady=5)

    def _construir_tab_gestion(self):
        # Formulario rápido de Cliente
        f_cli = tk.LabelFrame(self.tab_gestion, text="Registrar Cliente", padx=8, pady=5)
        f_cli.pack(fill="x", padx=8, pady=4)

        tk.Label(f_cli, text="ID:").grid(row=0, column=0)
        self.e_cli_id = tk.Entry(f_cli, width=8)
        self.e_cli_id.insert(0, "C05")
        self.e_cli_id.grid(row=0, column=1, padx=4)

        tk.Label(f_cli, text="Nombre:").grid(row=0, column=2)
        self.e_cli_nom = tk.Entry(f_cli, width=18)
        self.e_cli_nom.grid(row=0, column=3, padx=4)

        tk.Label(f_cli, text="Correo:").grid(row=0, column=4)
        self.e_cli_cor = tk.Entry(f_cli, width=22)
        self.e_cli_cor.grid(row=0, column=5, padx=4)

        tk.Label(f_cli, text="Teléfono:").grid(row=0, column=6)
        self.e_cli_tel = tk.Entry(f_cli, width=12)
        self.e_cli_tel.insert(0, "3150001122")
        self.e_cli_tel.grid(row=0, column=7, padx=4)

        tk.Button(
            f_cli, text="Guardar Cliente", bg="#16A34A", fg="white", command=self.gui_crear_cliente
        ).grid(row=0, column=8, padx=8)

        # Formulario rápido de Reserva y Procesamiento con Sobrecarga
        f_res = tk.LabelFrame(self.tab_gestion, text="Crear y Operar Reservas (Con Sobrecarga de Costos)", padx=8, pady=5)
        f_res.pack(fill="x", padx=8, pady=4)

        tk.Label(f_res, text="ID Reserva:").grid(row=0, column=0)
        self.e_res_id = tk.Entry(f_res, width=9)
        self.e_res_id.insert(0, "RES-005")
        self.e_res_id.grid(row=0, column=1, padx=4)

        tk.Label(f_res, text="ID Cliente:").grid(row=0, column=2)
        self.e_res_cli = tk.Entry(f_res, width=8)
        self.e_res_cli.insert(0, "C01")
        self.e_res_cli.grid(row=0, column=3, padx=4)

        tk.Label(f_res, text="ID Servicio:").grid(row=0, column=4)
        self.e_res_srv = tk.Entry(f_res, width=8)
        self.e_res_srv.insert(0, "S01")
        self.e_res_srv.grid(row=0, column=5, padx=4)

        tk.Label(f_res, text="Unidades:").grid(row=0, column=6)
        self.e_res_uni = tk.Entry(f_res, width=6)
        self.e_res_uni.insert(0, "2")
        self.e_res_uni.grid(row=0, column=7, padx=4)

        tk.Button(
            f_res, text="Crear Reserva", bg="#16A34A", fg="white", command=self.gui_crear_reserva
        ).grid(row=0, column=8, padx=6)

        tk.Label(f_res, text="IVA (0-0.5):").grid(row=1, column=0, pady=4)
        self.e_iva = tk.Entry(f_res, width=8)
        self.e_iva.insert(0, "0.19")
        self.e_iva.grid(row=1, column=1)

        tk.Label(f_res, text="Desc (0-0.99):").grid(row=1, column=2)
        self.e_desc = tk.Entry(f_res, width=8)
        self.e_desc.insert(0, "0.05")
        self.e_desc.grid(row=1, column=3)

        tk.Label(f_res, text="Recargo ($):").grid(row=1, column=4)
        self.e_rec = tk.Entry(f_res, width=8)
        self.e_rec.insert(0, "0")
        self.e_rec.grid(row=1, column=5)

        tk.Button(
            f_res, text="Procesar Reserva", bg="#7C3AED", fg="white",
            command=lambda: self.gui_operar_reserva("PROCESAR")
        ).grid(row=1, column=6, columnspan=2, padx=4)

        tk.Button(
            f_res, text="Cancelar Reserva", bg="#DC2626", fg="white",
            command=lambda: self.gui_operar_reserva("CANCELAR")
        ).grid(row=1, column=8, padx=4)

        # Tabla unificada de Reservas y Servicios
        cols = ("tipo", "id", "descripcion", "estado", "valor")
        self.tree = ttk.Treeview(self.tab_gestion, columns=cols, show="headings", height=14)
        self.tree.heading("tipo", text="Entidad")
        self.tree.heading("id", text="ID")
        self.tree.heading("descripcion", text="Detalle Polimórfico")
        self.tree.heading("estado", text="Estado / Disponibilidad")
        self.tree.heading("valor", text="Tarifa / Costo Total")

        self.tree.column("tipo", width=90, anchor="center")
        self.tree.column("id", width=90, anchor="center")
        self.tree.column("descripcion", width=420)
        self.tree.column("estado", width=130, anchor="center")
        self.tree.column("valor", width=150, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=8, pady=6)

    def refrescar_vistas(self):
        self.lbl_auditoria.config(
            text=(
                f"Auditoría (finally) -> Intentos: {auditoria['intentos']} | "
                f"Exitosas (else): {auditoria['exitosas']} | Errores (except): {auditoria['errores']}"
            )
        )
        for item in self.tree.get_children():
            self.tree.delete(item)

        for c in clientes:
            self.tree.insert("", tk.END, values=("CLIENTE", c.id_entidad, f"{c.nombre} ({c.correo})", "ACTIVO", c.telefono))
        for s in servicios:
            est = "DISPONIBLE" if s.disponible else "OCUPADO"
            self.tree.insert("", tk.END, values=("SERVICIO", s.id_entidad, s.nombre_servicio, est, f"${s.tarifa_base:,.2f}"))
        for r in reservas:
            det = f"Cliente {r.cliente.id_entidad} -> Servicio {r.servicio.id_entidad} ({r.unidades} u.)"
            self.tree.insert("", tk.END, values=("RESERVA", r.id_reserva, det, r.estado, f"${r.costo_total:,.2f}"))

        self.txt_logs.delete(1.0, tk.END)
        self.txt_logs.insert(tk.END, leer_historial_logs())
        self.txt_logs.see(tk.END)

    def ejecutar_simulacion_gui(self):
        lineas = ejecutar_simulacion_12_operaciones()
        self.txt_sim.delete(1.0, tk.END)
        for l in lineas:
            self.txt_sim.insert(tk.END, l + "\n")
        self.refrescar_vistas()

    def _notificar(self, resultado: str):
        self.txt_sim.insert(tk.END, f"\n[Operación Manual] {resultado}\n")
        self.txt_sim.see(tk.END)
        self.refrescar_vistas()
        if resultado.startswith("✔"):
            messagebox.showinfo("Operación Exitosa", resultado)
        else:
            messagebox.showwarning("Excepción Controlada", resultado)

    def gui_crear_cliente(self):
        res = registrar_cliente_seguro(
            self.e_cli_id.get(), self.e_cli_nom.get(), self.e_cli_cor.get(), self.e_cli_tel.get()
        )
        self._notificar(res)

    def gui_crear_reserva(self):
        res = crear_reserva_segura(
            self.e_res_id.get(), self.e_res_cli.get(), self.e_res_srv.get(), self.e_res_uni.get()
        )
        self._notificar(res)

    def gui_operar_reserva(self, accion: str):
        res = operar_reserva_segura(
            self.e_res_id.get(), accion, self.e_iva.get(), self.e_desc.get(), self.e_rec.get()
        )
        self._notificar(res)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazSoftwareFJ(ventana)
    ventana.mainloop()