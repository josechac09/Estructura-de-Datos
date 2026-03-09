import tkinter as tk

CAPACIDAD = 8
X_OFFSET = 50

# creativity globals
import random

pila = []
tope = 0
esperando = False

# maintain a parallel list of colors for stack elements
colors = []


def dibujar():

    canvas.delete("all")

    x1 = 420 + X_OFFSET
    x2 = 520 + X_OFFSET
    y = 450

    # optional background color change for creativity
    canvas.configure(bg=random.choice(["#f0f8ff","#fafad2","#e6e6fa","#ffe4e1"]))

    for i in range(CAPACIDAD):

        fillcol = colors[i] if i < len(colors) else "white"
        canvas.create_rectangle(x1, y, x2, y-45, outline="black", width=2, fill=fillcol)

        if i < len(pila):
            canvas.create_text((x1+x2)/2, y-22,
                               text=pila[i],
                               font=("Comic Sans MS",16,"bold"),
                               fill="darkblue")

        canvas.create_text(x2+30, y-22,
                           text=str(i+1),
                           font=("Arial",12))

        y -= 45

    canvas.create_text(120 + X_OFFSET,60,
                       text=f"TOPE = {tope}",
                       font=("Arial",18,"bold"),
                       fill="green")

    canvas.create_text(120 + X_OFFSET,100,
                       text=f"PILA = {pila}",
                       font=("Arial",16))

    if tope > 0:

        pos = 450 - (tope-1)*45 - 22

        canvas.create_text(360 + X_OFFSET,pos,
                           text="← TOPE",
                           font=("Arial",14,"bold"),
                           fill="red")


def insertar():

    global tope

    valor = entrada.get().upper()

    if valor == "":
        return

    if len(pila) < CAPACIDAD:

        pila.append(valor)
        tope += 1

        colors.append(random.choice(["#ff9999","#99ff99","#9999ff","#ffcc99","#cc99ff"]))

        estado.config(text=f"Insertado ({valor})")

        dibujar()

    entrada.delete(0, tk.END)


def eliminar_auto(valor):

    global tope, esperando

    if len(pila) > 0:
        pila.pop()
        tope -= 1

        if colors:
            colors.pop()

    estado.config(text=f"Elemento eliminado ({valor})")

    esperando = False

    dibujar()


def eliminar():

    global esperando, tope

    if esperando:
        return

    valor = entrada.get().upper()

    if valor == "":
        return

    if len(pila) < CAPACIDAD:

        pila.append(valor)
        tope += 1

        estado.config(text=f"Insertando {valor} y eliminando en 3s")

        esperando = True

        dibujar()

        ventana.after(3000, lambda: eliminar_auto(valor))

    entrada.delete(0, tk.END)


def reiniciar():

    global pila,tope,esperando

    pila=[]
    tope=0
    esperando=False
    colors.clear()

    estado.config(text="PILA VACÍA")

    dibujar()


ventana = tk.Tk()
ventana.title("Simulación Manual de Pila")
ventana.geometry("900x600")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

estado = tk.Label(frame_top,
                  text="PILA VACÍA",
                  font=("Arial",20,"bold"))
estado.pack()

frame_control = tk.Frame(ventana)
frame_control.pack(pady=10)

entrada = tk.Entry(frame_control,
                   font=("Arial",16),
                   width=5,
                   justify="center")
entrada.pack(side="left", padx=10)

btn_insertar = tk.Button(frame_control,
                         text="Insertar",
                         font=("Arial",14),
                         command=insertar)
btn_insertar.pack(side="left", padx=5)

btn_eliminar = tk.Button(frame_control,
                         text="Eliminar",
                         font=("Arial",14),
                         command=eliminar)
btn_eliminar.pack(side="left", padx=5)

btn_reset = tk.Button(frame_control,
                      text="Reiniciar",
                      font=("Arial",14),
                      command=reiniciar)
btn_reset.pack(side="left", padx=5)

canvas = tk.Canvas(ventana, bg="white")
canvas.pack(fill="both", expand=True)

dibujar()

ventana.mainloop()
