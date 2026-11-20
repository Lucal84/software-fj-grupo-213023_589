# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modelo.cliente import Cliente
from modelo.servicios import ReservaSala, AlquilerEquipo, Asesoria
from modelo.reserva import Reserva
from modelo.registro import registrar_error

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Management System")
        self.root.geometry("900x650")

        # Listas internas para almacenar objetos (simulan la "base de datos")
        self.clientes = []
        self.servicios = []
        self.reservas = []

        self._crear_pestanas()

    def _crear_pestanas(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Pestaña Clientes ---
        frame_cliente = ttk.Frame(notebook)
        notebook.add(frame_cliente, text="Clients")
        self._crear_formulario_cliente(frame_cliente)

        # --- Pestaña Servicios ---
        frame_servicio = ttk.Frame(notebook)
        notebook.add(frame_servicio, text="Services")
        self._crear_formulario_servicio(frame_servicio)

        # --- Pestaña Reservas ---
        frame_reserva = ttk.Frame(notebook)
        notebook.add(frame_reserva, text="Reservations")
        self._crear_formulario_reserva(frame_reserva)

    def _crear_formulario_cliente(self, parent):
        ttk.Label(parent, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_cli_id = ttk.Entry(parent, width=30)
        self.entry_cli_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_cli_nombre = ttk.Entry(parent, width=30)
        self.entry_cli_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_cli_correo = ttk.Entry(parent, width=30)
        self.entry_cli_correo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_cli_telefono = ttk.Entry(parent, width=30)
        self.entry_cli_telefono.grid(row=3, column=1, padx=5, pady=5)

        btn = ttk.Button(parent, text="Register Client", command=self._registrar_cliente)
        btn.grid(row=4, column=0, columnspan=2, pady=10)

    def _registrar_cliente(self):
        try:
            cliente = Cliente(
                self.entry_cli_id.get(),
                self.entry_cli_nombre.get(),
                self.entry_cli_correo.get(),
                self.entry_cli_telefono.get()
            )
            self.clientes.append(cliente)
            messagebox.showinfo("Success", f"Client '{cliente.nombre}' registered.")
        except Exception as e:
            registrar_error("Error al registrar cliente", e)
            messagebox.showerror("Error", str(e))

    def _crear_formulario_servicio(self, parent):
        # Tipo de servicio
        ttk.Label(parent, text="Service Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_tipo = ttk.Combobox(parent, values=["Room Reservation", "Equipment Rental", "Consulting"], state="readonly")
        self.combo_tipo.grid(row=0, column=1, padx=5, pady=5)

        # Campos comunes
        campos = [
            ("ID:", "entry_serv_id"),
            ("Name:", "entry_serv_nombre"),
            ("Base Rate ($/h):", "entry_serv_tarifa"),
            ("Capacity/Quantity/Specialty:", "entry_serv_extra")
        ]
        for i, (label, attr) in enumerate(campos, start=1):
            ttk.Label(parent, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(parent, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)

        btn = ttk.Button(parent, text="Create Service", command=self._crear_servicio)
        btn.grid(row=5, column=0, columnspan=2, pady=10)

    def _crear_servicio(self):
        try:
            tipo = self.combo_tipo.get()
            id_s = self.entry_serv_id.get()
            nombre = self.entry_serv_nombre.get()
            tarifa = float(self.entry_serv_tarifa.get())
            extra = self.entry_serv_extra.get()

            if tipo == "Room Reservation":
                servicio = ReservaSala(id_s, nombre, tarifa, capacidad=int(extra))
            elif tipo == "Equipment Rental":
                servicio = AlquilerEquipo(id_s, nombre, tarifa, cantidad_equipos=int(extra))
            elif tipo == "Consulting":
                servicio = Asesoria(id_s, nombre, tarifa, especialidad=extra)
            else:
                raise ValueError("Select a service type.")

            self.servicios.append(servicio)
            messagebox.showinfo("Success", f"Service '{servicio.nombre}' created.")
        except Exception as e:
            registrar_error("Error al crear servicio", e)
            messagebox.showerror("Error", str(e))

    def _crear_formulario_reserva(self, parent):
        ttk.Label(parent, text="Reservation ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_res_id = ttk.Entry(parent, width=30)
        self.entry_res_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Client (name):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_cliente = ttk.Combobox(parent, values=[c.nombre for c in self.clientes], state="readonly")
        self.combo_cliente.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Service (name):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_servicio = ttk.Combobox(parent, values=[s.nombre for s in self.servicios], state="readonly")
        self.combo_servicio.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Duration (hours):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_res_duracion = ttk.Entry(parent, width=30)
        self.entry_res_duracion.grid(row=3, column=1, padx=5, pady=5)

        # Botones de acción
        frame_botones = ttk.Frame(parent)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botones, text="Confirm Reservation", command=lambda: self._accion_reserva("confirmar")).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Cancel Reservation", command=lambda: self._accion_reserva("cancelar")).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Process Reservation", command=lambda: self._accion_reserva("procesar")).pack(side="left", padx=5)

    def _accion_reserva(self, accion):
        try:
            id_r = self.entry_res_id.get()
            nombre_cliente = self.combo_cliente.get()
            nombre_servicio = self.combo_servicio.get()
            duracion = int(self.entry_res_duracion.get())

            cliente = next((c for c in self.clientes if c.nombre == nombre_cliente), None)
            servicio = next((s for s in self.servicios if s.nombre == nombre_servicio), None)

            if not cliente or not servicio:
                raise ValueError("Client or service not found.")

            reserva = Reserva(id_r, cliente, servicio, duracion)

            if accion == "confirmar":
                reserva.confirmar()
                msg = f"Reservation {id_r} confirmed. Total: ${reserva.costo_total}"
            elif accion == "cancelar":
                reserva.cancelar()
                msg = f"Reservation {id_r} cancelled."
            elif accion == "procesar":
                reserva.procesar()
                msg = f"Reservation {id_r} processed."
            else:
                raise ValueError("Invalid action.")

            self.reservas.append(reserva)
            messagebox.showinfo("Success", msg)
        except Exception as e:
            registrar_error(f"Error en acción de reserva ({accion})", e)
            messagebox.showerror("Error", str(e))