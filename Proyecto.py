import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json #guarda datos en archivo de texto
import os   #interactua con el sistema operativo
from datetime import datetime

# Archivos
ARCHIVO_USUARIOS = "medicos.json"
ARCHIVO_HISTORIAL = "historial_camas.json"

# --------- MODELOS ---------
class Paciente:
    def __init__(self, nombre):
        self.nombre = nombre

class Enfermero:
    def __init__(self, nombre):
        self.nombre = nombre
        self.camas = {f"C{i}": None for i in range(1, 10)}

    def asignar_paciente(self, paciente, doctor):
        for cama, ocupado in self.camas.items():
            if ocupado is None:
                self.camas[cama] = paciente
                registrar_evento(paciente.nombre, cama, self.nombre, doctor, "ingreso")
                return cama
        return None

    def dar_de_alta(self, cama, doctor):
        paciente = self.camas[cama]
        if paciente:
            registrar_evento(paciente.nombre, cama, self.nombre, doctor, "alta")
            self.camas[cama] = None
            return True
        return False

    def estado_camas(self):
        return {c: p.nombre if p else "Libre" for c, p in self.camas.items()}

# --------- FUNCIONES DE ARCHIVOS ---------
def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r") as f:
            return json.load(f)
    return []

def guardar_historial():
    with open(ARCHIVO_HISTORIAL, "w") as f:
        json.dump(historial, f)

def registrar_evento(paciente, cama, enfermero, doctor, tipo):
    registro = {
        "paciente": paciente,
        "cama": cama,
        "enfermero": enfermero,
        "doctor": doctor,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": tipo
    }
    historial.append(registro)
    guardar_historial()

# --------- INTERFAZ ---------
def interfaz_login():
    for widget in ventana.winfo_children():
        widget.destroy()

    frame_login = tk.Frame(ventana, bg="lightblue")
    frame_login.pack(expand=True)

    tk.Label(frame_login, text="Sistema Hospitalario", font=("Arial", 16), bg="lightblue").pack(pady=10)
    tk.Label(frame_login, text="Usuario:", bg="lightblue").pack()
    entry_usuario = tk.Entry(frame_login)
    entry_usuario.pack()

    tk.Label(frame_login, text="Contraseña:", bg="lightblue").pack()
    entry_contra = tk.Entry(frame_login, show="*")
    entry_contra.pack()

    def login():
        user = entry_usuario.get()
        pwd = entry_contra.get()
        if user in usuarios and usuarios[user]["contraseña"] == pwd:
            medico_info["nombre"] = user
            medico_info["especialidad"] = usuarios[user]["especialidad"]
            medico_info["turno"] = usuarios[user]["turno"]
            iniciar_aplicacion()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar():
        user = entry_usuario.get()
        pwd = entry_contra.get()
        if user in usuarios:
            messagebox.showerror("Error", "El usuario ya existe")
            return
        especialidad = simpledialog.askstring("Especialidad", "¿Cuál es tu especialidad?")
        turno = simpledialog.askstring("Turno", "¿Cuál es tu turno? (mañana/tarde/noche)")
        if not user or not pwd or not especialidad or not turno:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        usuarios[user] = {
            "contraseña": pwd,
            "especialidad": especialidad,
            "turno": turno
        }
        guardar_usuarios()
        messagebox.showinfo("Registrado", "Usuario registrado correctamente")
        medico_info["nombre"] = user
        medico_info["especialidad"] = especialidad
        medico_info["turno"] = turno
        iniciar_aplicacion()

    tk.Button(frame_login, text="Iniciar sesión", command=login).pack(pady=5)
    tk.Button(frame_login, text="Registrarse", command=registrar).pack()

def iniciar_aplicacion():
    global menu_lateral, area_dinamica
    for widget in ventana.winfo_children():
        widget.destroy()

    menu_lateral = tk.Frame(ventana, bg="lightblue", width=180)
    menu_lateral.pack(side="left", fill="y")

    area_dinamica = tk.Frame(ventana, bg="white")
    area_dinamica.pack(side="right", expand=True, fill="both")

    tk.Button(menu_lateral, text="Inicio", width=18, command=saludo_bienvenida).pack(pady=10)
    tk.Button(menu_lateral, text="Agregar Paciente", width=18, command=agregar_paciente_ui).pack(pady=10)
    tk.Button(menu_lateral, text="Ver Camas", width=18, command=ver_camas_ui).pack(pady=10)
    tk.Button(menu_lateral, text="Historial", width=18, command=ver_historial).pack(pady=10)
    tk.Button(menu_lateral, text="Estética", width=18, command=estetica_ui).pack(pady=10)
    tk.Button(menu_lateral, text="Resetear Sistema", width=18, command=resetear_sistema).pack(pady=10)
    tk.Button(menu_lateral, text="Salir", width=18, command=ventana.destroy).pack(pady=20)

    saludo_bienvenida()

def saludo_bienvenida():
    limpiar_area()
    tk.Label(area_dinamica, text="🩺 Bienvenido al Control de Pacientes", font=("Arial", 16)).pack(pady=20)
    tk.Label(area_dinamica, text=f"Médico: {medico_info['nombre']} | Especialidad: {medico_info['especialidad']} | Turno: {medico_info['turno']}", font=("Arial", 12)).pack(pady=5)

def agregar_paciente_ui():
    limpiar_area()
    tk.Label(area_dinamica, text="Agregar nuevo paciente", font=("Arial", 14)).pack(pady=10)

    def agregar():
        nombre = entrada_nombre.get()
        if not nombre:
            messagebox.showerror("Error", "Debes ingresar un nombre.")
            return

        paciente = Paciente(nombre)
        cama_asignada = enfermero_global.asignar_paciente(paciente, medico_info["nombre"])

        if cama_asignada:
            messagebox.showinfo("Paciente asignado", f"{nombre} fue asignado a la cama {cama_asignada}.")
        else:
            messagebox.showwarning("Camas llenas", "No hay camas disponibles.")
        entrada_nombre.delete(0, tk.END)

    tk.Label(area_dinamica, text="Nombre del paciente:").pack()
    entrada_nombre = tk.Entry(area_dinamica)
    entrada_nombre.pack(pady=5)
    tk.Button(area_dinamica, text="Asignar paciente", command=agregar).pack(pady=10)

def ver_camas_ui():
    limpiar_area()
    tk.Label(area_dinamica, text="🛏 Estado de las camas", font=("Arial", 14)).pack(pady=10)

    info = f"Médico: {medico_info['nombre']} | Especialidad: {medico_info['especialidad']} | Turno: {medico_info['turno']}\nEnfermero: {enfermero_global.nombre}"
    tk.Label(area_dinamica, text=info, font=("Arial", 10, "italic")).pack(pady=5)

    for cama, ocupante in enfermero_global.estado_camas().items():
        frame = tk.Frame(area_dinamica)
        frame.pack(fill="x", padx=10, pady=2)

        estado = "Libre" if ocupante == "Libre" else "Ocupada"
        texto = f"{cama} - Estado: {estado} - Paciente: {ocupante if ocupante != 'Libre' else '-'}"
        tk.Label(frame, text=texto, width=80, anchor="w").pack(side="left")

        if ocupante != "Libre":
            tk.Button(frame, text="Dar de alta", command=lambda c=cama: dar_alta(c)).pack(side="right")

def dar_alta(cama):
    if enfermero_global.dar_de_alta(cama, medico_info["nombre"]):
        messagebox.showinfo("Alta registrada", f"El paciente de la cama {cama} fue dado de alta.")
        ver_camas_ui()
    else:
        messagebox.showerror("Error", "No se pudo dar de alta.")

def ver_historial():
    limpiar_area()
    tk.Label(area_dinamica, text="📋 Historial de pacientes", font=("Arial", 14)).pack(pady=10)

    tabla = ttk.Treeview(area_dinamica, columns=("evento", "paciente", "cama", "enfermero", "doctor", "fecha"), show="headings")
    for col in ("evento", "paciente", "cama", "enfermero", "doctor", "fecha"):
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center", width=120 if col != "fecha" else 180)

    for registro in historial:
        tabla.insert("", "end", values=(registro["evento"], registro["paciente"], registro["cama"], registro["enfermero"], registro["doctor"], registro["fecha"]))

    tabla.pack(expand=True, fill="both", padx=10, pady=10)

def resetear_sistema():
    if messagebox.askyesno("Confirmar", "¿Estás seguro de borrar todo el historial y vaciar las camas?"):
        enfermero_global.camas = {f"C{i}": None for i in range(1, 10)}
        historial.clear()
        guardar_historial()
        messagebox.showinfo("Sistema reiniciado", "Todo el historial fue eliminado.")

def estetica_ui():
    limpiar_area()
    tk.Label(area_dinamica, text="Configuración estética", font=("Arial", 14)).pack(pady=10)
    colores = ["lightblue", "lightgreen", "lightyellow", "lightgray", "white"]

    def cambiar_color(c):
        ventana.config(bg=c)
        menu_lateral.config(bg=c)
        area_dinamica.config(bg=c)

    for c in colores:
        tk.Button(area_dinamica, text=c, bg=c, width=20, command=lambda col=c: cambiar_color(col)).pack(pady=2)

def limpiar_area():
    for widget in area_dinamica.winfo_children():
        widget.destroy()

# --------- VARIABLES GLOBALES ---------
usuarios = cargar_usuarios()
historial = cargar_historial()
medico_info = {"nombre": "", "especialidad": "", "turno": ""}
enfermero_global = Enfermero("Laura Gómez")

# --------- INICIO DE LA APLICACIÓN ---------
ventana = tk.Tk()
ventana.title("Sistema Hospitalario")
ventana.state("zoomed")  # Abrir en pantalla completa
ventana.config(bg="lightblue")

interfaz_login()
ventana.mainloop()
