import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Configura la conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Ryu2024$", 
    "database": "semana8"
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
    exit()

# Crea la ventana principal
root = tk.Tk()
root.geometry("400x460")
root.title("Gestión de Fauna/Flora")


# Función para agregar un objeto a la base de datos
def agregar_objeto():
    # Obtén los valores de los campos de entrada
    id_objeto = id_entry.get()
    nombre_cientifico = nombre_entry.get()
    habitat = habitat_entry.get()
    estado_conservacion = estado_entry.get()
    region_geografica = region_entry.get()

    # Inserta los datos en la tabla
    query = "INSERT INTO FaunaFlora (ID, NombreCientifico, Habitat, EstadoConservacion, RegionGeografica) VALUES (%s, %s, %s, %s, %s)"
    values = (id_objeto, nombre_cientifico, habitat, estado_conservacion, region_geografica)
    cursor.execute(query, values) 
    conn.commit()

    # Limpia los campos de entrada
    id_entry.delete(0, tk.END)
    nombre_entry.delete(0, tk.END)
    habitat_entry.delete(0, tk.END)
    estado_entry.delete(0, tk.END)
    region_entry.delete(0, tk.END)


# Función para actualizar la lista de objetos
def actualizar_lista():
    lista_fauna_flora.delete(0, tk.END)
    cargar_lista()  
    messagebox.showinfo("Información", "Lista actualizada correctamente")

# Botón para actualizar la lista
actualizar_lista_button = tk.Button(root, text="Actualizar Lista", fg="white", command=actualizar_lista, bg="green")
actualizar_lista_button.grid(row=9, columnspan=2)

# Crear un Listbox para mostrar la lista de objetos
lista_fauna_flora = tk.Listbox(root)
lista_fauna_flora.grid(row=6, columnspan=2)

# Función para cargar la lista de objetos desde la base de datos
def cargar_lista():
    cursor.execute("SELECT NombreCientifico FROM FaunaFlora")
    resultados = cursor.fetchall()
    for row in resultados:
        lista_fauna_flora.insert(tk.END, row[0])

# Llama a esta función después de establecer la conexión
cargar_lista()

def borrar_objeto():
    seleccionado = lista_fauna_flora.curselection()
    if seleccionado:
        nombre_seleccionado = lista_fauna_flora.get(seleccionado[0])
        query = "DELETE FROM FaunaFlora WHERE NombreCientifico = %s"
        cursor.execute(query, (nombre_seleccionado,))
        conn.commit()
        lista_fauna_flora.delete(seleccionado)
    else:
        print("Selecciona un objeto para borrar.")

# Agrega un botón "Borrar" y llama a la función correspondiente
borrar_button = tk.Button(root, text="Borrar", command=borrar_objeto)
borrar_button.grid(row=7, columnspan=2)


def cargar_info():
    seleccionado = lista_fauna_flora.curselection()
    if seleccionado:
        nombre_seleccionado = lista_fauna_flora.get(seleccionado[0])

        # Consulta para obtener los datos del objeto seleccionado
        cursor.execute("SELECT * FROM FaunaFlora WHERE NombreCientifico = %s", (nombre_seleccionado,))
        objeto = cursor.fetchone()

        # Cargar los datos en los campos de entrada
        id_entry.delete(0, tk.END)
        id_entry.insert(0, objeto[0])  # ID
        nombre_entry.delete(0, tk.END)
        nombre_entry.insert(0, objeto[1])  # NombreCientifico
        habitat_entry.delete(0, tk.END)
        habitat_entry.insert(0, objeto[2])  # Habitat
        estado_entry.delete(0, tk.END)
        estado_entry.insert(0, objeto[3])  # EstadoConservacion
        region_entry.delete(0, tk.END)
        region_entry.insert(0, objeto[4])  # RegionGeografica
    else:
        print("Selecciona un objeto para cargar su información.")

# Agrega un botón "Actualizar" y llama a la función correspondiente
actualizar_button = tk.Button(root, text="Mostrar Info", command=cargar_info)
actualizar_button.grid(row=8, columnspan=2)



# Etiquetas y campos de entrada
id_label = tk.Label(root, text="ID:", pady=5)
id_entry = tk.Entry(root)
nombre_label = tk.Label(root, text="Nombre Científico:", pady=5)
nombre_entry = tk.Entry(root)
habitat_label = tk.Label(root, text="Habitat:", pady=5)
habitat_entry = tk.Entry(root)
estado_label = tk.Label(root, text="Estado de Conservación:",pady=6)
estado_entry = tk.Entry(root)
region_label = tk.Label(root, text="Región Geográfica:", padx=55, pady=5)
region_entry = tk.Entry(root)
agregar_button = tk.Button(root, text="Agregar", command=agregar_objeto, padx=15, pady=3, bg="green", fg="white")
agregar_button.place(x=250, y=80)

# Posiciona los widgets en la ventana
id_label.grid(row=0, column=0)
id_entry.grid(row=0, column=1)
nombre_label.grid(row=1, column=0)
nombre_entry.grid(row=1, column=1)
habitat_label.grid(row=2, column=0)
habitat_entry.grid(row=2, column=1)
estado_label.grid(row=3, column=0)
estado_entry.grid(row=3, column=1)
region_label.grid(row=4, column=0)
region_entry.grid(row=4, column=1)
agregar_button.grid(row=5, columnspan=2)

# Cierra la conexión al cerrar la aplicación
def cerrar_conexion():
    cursor.close()
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", cerrar_conexion)

root.mainloop()
