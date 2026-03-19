import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font

class Nodo:
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
        self.sig = None

class ListaIngredientes:

    def __init__(self):
        self.inicio = None

    def insertar(self, ingrediente):
        nuevo = Nodo(ingrediente)

        if self.inicio is None:
            self.inicio = nuevo
        else:
            aux = self.inicio
            while aux.sig:
                aux = aux.sig
            aux.sig = nuevo

    def obtener_lista(self):
        ingredientes = []
        aux = self.inicio

        while aux:
            ingredientes.append(aux.ingrediente)
            aux = aux.sig

        return ingredientes

    def eliminar(self, ingrediente):

        if self.inicio is None:
            return False

        if self.inicio.ingrediente == ingrediente:
            self.inicio = self.inicio.sig
            return True

        ant = self.inicio
        aux = self.inicio.sig

        while aux:
            if aux.ingrediente == ingrediente:
                ant.sig = aux.sig
                return True
            ant = aux
            aux = aux.sig

        return False

class Postre:

    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaIngredientes()

POSTRES = []

def cargar_ejemplos():

    flan = Postre("Flan")
    flan.ingredientes.insertar("Leche")
    flan.ingredientes.insertar("Huevo")
    flan.ingredientes.insertar("Azúcar")

    gelatina = Postre("Gelatina")
    gelatina.ingredientes.insertar("Agua")
    gelatina.ingredientes.insertar("Gelatina en polvo")
    gelatina.ingredientes.insertar("Azúcar")

    pastel = Postre("Pastel")
    pastel.ingredientes.insertar("Harina")
    pastel.ingredientes.insertar("Huevo")
    pastel.ingredientes.insertar("Mantequilla")

    POSTRES.extend([flan, gelatina, pastel])
    POSTRES.sort(key=lambda x: x.nombre)

def buscar_postre(nombre):
    for p in POSTRES:
        if p.nombre.lower() == nombre.lower():
            return p
    return None

def actualizar_lista():

    lista.delete(0, tk.END)

    for p in POSTRES:
        ingredientes = ", ".join(p.ingredientes.obtener_lista())
        texto = p.nombre + " -> " + ingredientes
        lista.insert(tk.END, texto)

def mostrar_ingredientes():

    nombre = entry_postre.get()
    postre = buscar_postre(nombre)

    if postre:
        ing = "\n".join(postre.ingredientes.obtener_lista())
        messagebox.showinfo("Ingredientes", ing)
    else:
        messagebox.showerror("Error", "Postre no encontrado")

def agregar_ingrediente():

    nombre = entry_postre.get()
    ingrediente = entry_ingrediente.get()

    postre = buscar_postre(nombre)

    if postre:
        postre.ingredientes.insertar(ingrediente)
        actualizar_lista()
    else:
        messagebox.showerror("Error", "Postre no existe")

def eliminar_ingrediente():

    nombre = entry_postre.get()
    ingrediente = entry_ingrediente.get()

    postre = buscar_postre(nombre)

    if postre:
        eliminado = postre.ingredientes.eliminar(ingrediente)

        if eliminado:
            actualizar_lista()
        else:
            messagebox.showerror("Error", "Ingrediente no encontrado")
    else:
        messagebox.showerror("Error", "Postre no existe")

def agregar_postre():

    nombre = entry_postre.get()

    if buscar_postre(nombre):
        messagebox.showerror("Error", "El postre ya existe")
        return

    nuevo = Postre(nombre)
    POSTRES.append(nuevo)

    POSTRES.sort(key=lambda x: x.nombre)

    actualizar_lista()

def eliminar_postre():

    nombre = entry_postre.get()
    postre = buscar_postre(nombre)

    if postre:
        POSTRES.remove(postre)
        actualizar_lista()
    else:
        messagebox.showerror("Error", "Postre no encontrado")

ventana = tk.Tk()
ventana.title("Sistema de Postres")
ventana.geometry("600x500")

title_label = tk.Label(ventana, text="Gestor de Postres", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

main_frame = ttk.Frame(ventana, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.LabelFrame(main_frame, text="Entradas", padding="10")
input_frame.pack(fill=tk.X, pady=5)

ttk.Label(input_frame, text="Nombre del postre:").grid(row=0, column=0, sticky=tk.W, pady=2)
entry_postre = ttk.Entry(input_frame, width=30)
entry_postre.grid(row=0, column=1, pady=2, padx=5)

ttk.Label(input_frame, text="Ingrediente:").grid(row=1, column=0, sticky=tk.W, pady=2)
entry_ingrediente = ttk.Entry(input_frame, width=30)
entry_ingrediente.grid(row=1, column=1, pady=2, padx=5)

buttons_frame = ttk.LabelFrame(main_frame, text="Acciones", padding="10")
buttons_frame.pack(fill=tk.X, pady=5)

btn_mostrar = ttk.Button(buttons_frame, text="Mostrar Ingredientes", command=mostrar_ingredientes)
btn_mostrar.grid(row=0, column=0, padx=5, pady=5)

btn_agregar_ing = ttk.Button(buttons_frame, text="Agregar Ingrediente", command=agregar_ingrediente)
btn_agregar_ing.grid(row=0, column=1, padx=5, pady=5)

btn_eliminar_ing = ttk.Button(buttons_frame, text="Eliminar Ingrediente", command=eliminar_ingrediente)
btn_eliminar_ing.grid(row=0, column=2, padx=5, pady=5)

btn_agregar_postre = ttk.Button(buttons_frame, text="Agregar Postre", command=agregar_postre)
btn_agregar_postre.grid(row=1, column=0, padx=5, pady=5)

btn_eliminar_postre = ttk.Button(buttons_frame, text="Eliminar Postre", command=eliminar_postre)
btn_eliminar_postre.grid(row=1, column=1, padx=5, pady=5)

list_frame = ttk.LabelFrame(main_frame, text="Lista de Postres", padding="10")
list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

scrollbar = ttk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista = tk.Listbox(list_frame, width=60, height=10, yscrollcommand=scrollbar.set)
lista.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=lista.yview)

cargar_ejemplos()
actualizar_lista()

ventana.mainloop()
