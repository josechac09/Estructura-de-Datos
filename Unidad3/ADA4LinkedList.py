import tkinter as tk
from tkinter import ttk, messagebox
from MyLinkedList import MyLinkedList, DoublyLinkedList, CircularLinkedList

simple = MyLinkedList()
doble = DoublyLinkedList()
circular = CircularLinkedList()

def obtener_estructura():
    tipo = combo.get()
    if tipo == "Simple":
        return simple
    elif tipo == "Doble":
        return doble
    else:
        return circular

def obtener_lista():
    return obtener_estructura().to_list()

def insertar_inicio():
    valor = entry_valor.get().strip()

    if not valor:
        messagebox.showwarning("Advertencia", "Ingresa un valor")
        return

    obtener_estructura().insert_first(valor)

    entry_valor.delete(0, tk.END)
    dibujar()

def insertar_final():
    valor = entry_valor.get().strip()

    if not valor:
        messagebox.showwarning("Advertencia", "Ingresa un valor")
        return

    obtener_estructura().insert_last(valor)

    entry_valor.delete(0, tk.END)
    dibujar()

def insertar_posicion():
    valor = entry_valor.get().strip()
    posicion_str = entry_posicion.get()

    if not valor or not posicion_str:
        messagebox.showwarning("Advertencia", "Ingresa valor y posición")
        return

    try:
        posicion = int(posicion_str)
    except ValueError:
        messagebox.showerror("Error", "La posición debe ser un número")
        return

    obtener_estructura().insert_at_position(posicion, valor)

    entry_valor.delete(0, tk.END)
    entry_posicion.delete(0, tk.END)
    dibujar()

def eliminar():
    valor = entry_valor.get().strip()

    if not valor:
        messagebox.showwarning("Advertencia", "Ingresa un valor")
        return

    obtener_estructura().delete_node(valor)

    entry_valor.delete(0, tk.END)
    dibujar()

def dibujar():
    canvas.delete("all")

    datos = obtener_lista()

    if not datos:
        canvas.create_text(
            550, 200,
            text="Lista vacía",
            font=("Arial", 14, "bold"),
            fill="gray"
        )
        return

    total = len(datos)
    x = max(60, (1100 - total * 120) // 2)
    y = 150

    x_inicio = x
    tipo = combo.get()

    for i, d in enumerate(datos):

        canvas.create_rectangle(
            x, y,
            x+80, y+40,
            fill="#8bc34a",
            outline="#2e7d32",
            width=2
        )

        canvas.create_text(
            x+40,
            y+20,
            text=str(d),
            font=("Arial", 11, "bold")
        )

        canvas.create_oval(
            x+70, y+15,
            x+85, y+30,
            fill="#1976d2"
        )

        if i < total - 1:
            if tipo == "Doble":
                canvas.create_line(x+85, y+15, x+120, y+15, arrow=tk.LAST, width=2)
                canvas.create_line(x+120, y+25, x+85, y+25, arrow=tk.LAST, width=2)
            else:
                canvas.create_line(x+85, y+20, x+120, y+20, arrow=tk.LAST, width=2)

        x += 120

    x_fin = x - 40

    canvas.create_text(
        x_inicio + 40,
        y - 60,
        text="INICIO",
        font=("Arial", 11, "bold"),
        fill="#1976d2"
    )

    if tipo != "Circular":
        canvas.create_text(
            x_fin,
            y - 60,
            text="FIN",
            font=("Arial", 11, "bold"),
            fill="#d32f2f"
        )

    if tipo == "Circular" and total > 1:

        canvas.create_line(
            x_fin, y+20,
            x_fin, y+100,
            x_inicio-20, y+100,
            x_inicio-20, y+20,
            smooth=True,
            splinesteps=20,
            dash=(3, 2),
            width=2
        )

        canvas.create_line(
            x_inicio-20, y+20,
            x_inicio, y+20,
            arrow=tk.LAST,
            width=2
        )

        canvas.create_text(
            550,
            y+130,
            text="Regresa al inicio",
            font=("Arial", 10, "italic"),
            fill="#d32f2f"
        )

root = tk.Tk()
root.title("MyLinkedList Visual")
root.geometry("1200x600")

frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Tipo lista").grid(row=0, column=0, padx=5)

combo = ttk.Combobox(
    frame,
    values=["Simple", "Doble", "Circular"],
    state="readonly",
    width=10
)
combo.current(0)
combo.grid(row=0, column=1, padx=5)

ttk.Label(frame, text="Valor").grid(row=0, column=2, padx=5)

entry_valor = ttk.Entry(frame, width=10)
entry_valor.grid(row=0, column=3, padx=5)

ttk.Label(frame, text="Posición").grid(row=0, column=4, padx=5)

entry_posicion = ttk.Entry(frame, width=8)
entry_posicion.grid(row=0, column=5, padx=5)

ttk.Button(frame, text="Insertar Inicio", command=insertar_inicio)\
    .grid(row=1, column=0, padx=5, pady=5)

ttk.Button(frame, text="Insertar Final", command=insertar_final)\
    .grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame, text="Insertar en Posición", command=insertar_posicion)\
    .grid(row=1, column=2, padx=5, pady=5)

ttk.Button(frame, text="Eliminar", command=eliminar)\
    .grid(row=1, column=3, padx=5, pady=5)

canvas = tk.Canvas(
    root,
    width=1100,
    height=400,
    bg="#f4f6f8"
)
canvas.pack(pady=20)

root.mainloop()
