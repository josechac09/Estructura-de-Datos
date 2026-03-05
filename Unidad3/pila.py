import tkinter as tk
from tkinter import messagebox

pila = []
MAX = 7

def actualizar_pila():
    canvas.delete("all")

    y = 320
    for elemento in reversed(pila):
        canvas.create_rectangle(120, y, 220, y-40, fill="lightblue")
        canvas.create_text(170, y-20, text=str(elemento), font=("Arial", 12, "bold"))
        y -= 45

    if pila:
        etiqueta_tope.config(text="Tope (Peek): " + str(pila[-1]))
    else:
        etiqueta_tope.config(text="Pila vacía (isEmpty)")

    etiqueta_size.config(text="Tamaño (Size): " + str(len(pila)))

def push():
    valor = entrada.get()

    if valor == "":
        messagebox.showwarning("Error", "Ingrese un valor")
        return

    if len(pila) >= MAX:
        messagebox.showwarning("Pila llena (isFull)", "La pila ya tiene 7 elementos")
        return

    pila.append(valor)
    entrada.delete(0, tk.END)
    actualizar_pila()

def pop():
    if not pila:
        messagebox.showwarning("Error", "La pila está vacía (isEmpty)")
        return

    eliminado = pila.pop()
    messagebox.showinfo("Elemento eliminado", "Se quitó: " + str(eliminado) + " (Pop)")
    actualizar_pila()

def peek():
    if not pila:
        messagebox.showinfo("Tope (Peek)", "La pila está vacía (isEmpty)")
    else:
        messagebox.showinfo("Tope (Peek)", "Elemento en el tope: " + str(pila[-1]))

def isempty():
    if not pila:
        messagebox.showinfo("Estado (isEmpty)", "La pila está vacía")
    else:
        messagebox.showinfo("Estado (isEmpty)", "La pila tiene elementos")

def size():
    messagebox.showinfo("Tamaño (Size)", "La pila tiene " + str(len(pila)) + " elementos")

def clear():
    pila.clear()
    actualizar_pila()
    messagebox.showinfo("Vaciar pila (Clear)", "La pila ha sido vaciada")

ventana = tk.Tk()
ventana.title("Simulador de Pila")
ventana.geometry("400x550")

titulo = tk.Label(ventana, text="Simulador de Pila (Stack)", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

entrada = tk.Entry(ventana)
entrada.pack(pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack()

tk.Button(frame_botones, text="Insertar (Push)", width=12, command=push).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Quitar (Pop)", width=12, command=pop).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Ver Tope (Peek)", width=14, command=peek).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="¿Vacía? (isEmpty)", width=14, command=isempty).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Mostrar Tamaño (Size)", width=30, command=size).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(frame_botones, text="Vaciar pila (Clear)", width=30, command=clear).grid(row=3, column=0, columnspan=2, pady=5)

etiqueta_tope = tk.Label(ventana, text="Pila vacía (isEmpty)", font=("Arial", 11))
etiqueta_tope.pack()

etiqueta_size = tk.Label(ventana, text="Tamaño (Size): 0", font=("Arial", 11))
etiqueta_size.pack()

canvas = tk.Canvas(ventana, width=350, height=340, bg="white")
canvas.pack(pady=10)

ventana.mainloop()
