import tkinter as tk
from tkinter import messagebox

class Cola:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.items:
            return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def actualizar_dibujo():
    canvas.delete("all")

    xA = 150
    xB = 300
    xR = 450
    y_inicio = 60
    alto = 40
    ancho = 60
    espacio = 50

    canvas.create_text(xA+30,30,text="Cola A",font=("Arial",14,"bold"))
    canvas.create_text(xB+30,30,text="Cola B",font=("Arial",14,"bold"))
    canvas.create_text(xR+30,30,text="Cola Resultado",font=("Arial",14,"bold"))

    filas = max(len(colaA.items), len(colaB.items), len(colaR.items))

    for i in range(filas):

        y = y_inicio + i*espacio

        if i < len(colaA.items):
            canvas.create_rectangle(xA,y,xA+ancho,y+alto,fill="lightblue")
            canvas.create_text(xA+30,y+20,text=str(colaA.items[i]),font=("Arial",12,"bold"))

        if i < len(colaB.items):
            canvas.create_rectangle(xB,y,xB+ancho,y+alto,fill="lightgreen")
            canvas.create_text(xB+30,y+20,text=str(colaB.items[i]),font=("Arial",12,"bold"))

        if i < len(colaR.items):
            canvas.create_rectangle(xR,y,xR+ancho,y+alto,fill="lightyellow")
            canvas.create_text(xR+30,y+20,text=str(colaR.items[i]),font=("Arial",12,"bold"))


def agregar_A():
    try:
        num = int(entradaA.get())
        colaA.enqueue(num)
        entradaA.delete(0, tk.END)
        actualizar_dibujo()
    except:
        messagebox.showerror("Error","Ingrese un número válido")


def agregar_B():
    try:
        num = int(entradaB.get())
        colaB.enqueue(num)
        entradaB.delete(0, tk.END)
        actualizar_dibujo()
    except:
        messagebox.showerror("Error","Ingrese un número válido")


def sumar():

    colaR.items.clear()

    if colaA.size() != colaB.size():
        messagebox.showerror("Error","Las colas deben tener el mismo tamaño")
        return

    tempA = Cola()
    tempB = Cola()

    tempA.items = colaA.items.copy()
    tempB.items = colaB.items.copy()

    while not tempA.is_empty():
        colaR.enqueue(tempA.dequeue() + tempB.dequeue())

    actualizar_dibujo()


def restablecer():
    colaA.items.clear()
    colaB.items.clear()
    colaR.items.clear()
    actualizar_dibujo()


colaA = Cola()
colaB = Cola()
colaR = Cola()

ventana = tk.Tk()
ventana.title("Colas con Suma")
ventana.geometry("650x400")

tk.Label(ventana,text="Agregar a Cola A").pack()
entradaA = tk.Entry(ventana)
entradaA.pack()

tk.Button(ventana,text="Insertar en Cola A",command=agregar_A).pack(pady=3)

tk.Label(ventana,text="Agregar a Cola B").pack()
entradaB = tk.Entry(ventana)
entradaB.pack()

tk.Button(ventana,text="Insertar en Cola B",command=agregar_B).pack(pady=3)

tk.Button(ventana,text="Sumar Colas",command=sumar).pack(pady=5)

tk.Button(ventana,text="Restablecer",command=restablecer).pack(pady=5)

canvas = tk.Canvas(ventana,width=600,height=450,bg="white")
canvas.pack(pady=10)

ventana.mainloop()
