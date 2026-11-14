# Programacion-213023-Fase4-Grupo390
Sistema Integral de Gestión - Software FJ

# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Repositorio oficial del proyecto **Software FJ**, desarrollado en Python bajo una arquitectura modular orientada a objetos (POO), manejo robusto de excepciones personalizadas, encadenamiento de errores, persistencia de bitácora en archivo plano e interfaz gráfica de usuario con **Tkinter**.

---

## 📋 Información Académica

* **Curso:** Programación (213023) - Grupo 390
* **Fase:** Fase 4 - Componente práctico - Prácticas simuladas
* **Institución:** Universidad Nacional Abierta y a Distancia (UNAD)
* **Autores:**
  * George Steven Arteaga Guzman
  * Jesus Steven Rodriguez Lopez
* **Fecha de entrega:** 22 de noviembre de 2026

---

## 🗂️ Arquitectura Modular del Proyecto

El sistema está desacoplado en paquetes especializados según su responsabilidad dentro de la lógica de negocio:

```text
Programacion-213023-Fase4-Grupo390/
├── excepciones/
│   └── errores.py            # Jerarquía de excepciones personalizadas del dominio
├── modelos/
│   ├── entidades.py          # Clases abstractas, Cliente y subtipos de Servicio (Polimorfismo y Sobrecarga)
│   └── reserva.py            # Gestión del ciclo de vida de reservas y encadenamiento de excepciones
├── utilidades/
│   └── logger.py             # Escritura y lectura de bitácora en archivo plano con cierre garantizado
├── main.py                   # Punto de entrada, auditoría try/except/else/finally, simulación e interfaz Tkinter
├── sistema_eventos.log       # Bitácora oficial autogenerada con eventos [INFO] y fallos [ERROR]
└── README.md                 # Documentación general del repositorio