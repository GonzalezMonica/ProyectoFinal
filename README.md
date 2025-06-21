 # ProyectoFinal
🏥 Sistema de Control Hospitalario
Este proyecto es una aplicación de escritorio desarrollada en Python con Tkinter, diseñada para simular un sistema básico de control hospitalario. Permite al personal médico gestionar camas, asignar pacientes, registrar eventos clínicos y mantener un historial persistente de atención.

# Características principales:
  
  ~Registro e inicio de sesión de médicos con nombre, especialidad y turno.

  ~Asignación automática de camas a nuevos pacientes.

  ~Visualización del estado actual de las camas (ocupadas o libres).

  ~Funcionalidad para dar de alta pacientes y liberar camas.

  ~Registro de historial clínico con fecha, médico, paciente, cama y tipo de evento (ingreso o alta).

  ~Persistencia de datos mediante archivos .json (no se pierden los datos al cerrar la aplicación).

  ~Opción para personalizar la estética del sistema.

  ~Función para resetear todo el sistema (vaciar camas y borrar historial).

# Archivos importantes:

  ~sistema_hospitalario.py: Código principal del sistema.

  ~medicos.json: Archivo que almacena los médicos registrados.

  ~historial_camas.json: Archivo que guarda todos los eventos del historial (ingresos y altas).

