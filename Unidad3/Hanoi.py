import tkinter as tk
import time

ANCHO = 1200
ALTO = 500

torres = [[], [], []]
movimientos = []
contador = 0
inicio_tiempo = 0
corriendo = False
animacion_id = None

MAX_ANIM = 200

posiciones = [
    ANCHO * 0.15,
    ANCHO * 0.50,
    ANCHO * 0.85
]

def dibujar_base():
    canvas.delete("all")
    canvas.create_rectangle(0, 380, ANCHO, 410, fill="#a56b00")

    for x in posiciones:
        canvas.create_rectangle(x-6, 200, x+6, 380, fill="#a56b00")

def dibujar_discos():
    n = escala.get()

    tower_top = 200
    tower_bottom = 380

    alto = max((tower_bottom - tower_top)/n, 4)

    espacio = posiciones[1] - posiciones[0]
    max_ancho = espacio * 0.28
    paso = max_ancho / n

    for i in range(3):
        for j, tamaño in enumerate(torres[i]):
            ancho = tamaño * paso
            x = posiciones[i]
            y = tower_bottom - j * alto

            canvas.create_rectangle(
                x-ancho,
                y-alto,
                x+ancho,
                y,
                fill="#8aa3ff",
                outline="#1d2aff",
                width=3
            )

def hanoi(n, origen, auxiliar, destino):
    if len(movimientos) >= MAX_ANIM:
        return

    if n == 1:
        movimientos.append((origen, destino))
    else:
        hanoi(n-1, origen, destino, auxiliar)

        if len(movimientos) < MAX_ANIM:
            movimientos.append((origen, destino))

        hanoi(n-1, auxiliar, origen, destino)

def actualizar_discos(valor):
    global torres

    n = int(valor)
    torres = [list(range(n,0,-1)), [], []]

    dibujar_base()
    dibujar_discos()

def iniciar():
    global torres, movimientos, contador, inicio_tiempo, corriendo

    n = escala.get()

    torres = [list(range(n,0,-1)),[],[]]
    movimientos = []
    contador = 0

    mejor = 2**n - 1

    label_mejor.config(text=f"Mejor : {mejor:,} movimientos")

    dibujar_base()
    dibujar_discos()

    inicio_tiempo = time.time()
    corriendo = True

    label_mov.config(text=f"{0:,} movimientos")

    hanoi(n,0,1,2)

    actualizar_tiempo()
    animar()

def actualizar_tiempo():
    if corriendo:
        t = time.time() - inicio_tiempo
        label_tiempo.config(text=f"Tiempo: {t:.2f} s")
        ventana.after(100, actualizar_tiempo)

def animar():
    global contador, corriendo, animacion_id

    if not corriendo:
        return

    if contador >= len(movimientos):
        corriendo = False
        return

    origen, destino = movimientos[contador]

    disco = torres[origen].pop()
    torres[destino].append(disco)

    contador += 1

    label_mov.config(text=f"{contador:,} movimientos")

    dibujar_base()
    dibujar_discos()

    animacion_id = ventana.after(120, animar)

def reset():
    global torres, contador, corriendo, movimientos, animacion_id

    corriendo = False
    contador = 0
    movimientos = []

    if animacion_id is not None:
        ventana.after_cancel(animacion_id)
        animacion_id = None

    n = escala.get()

    torres = [list(range(n,0,-1)),[],[]]

    label_mov.config(text=f"{0:,} movimientos")
    label_mejor.config(text="")
    label_tiempo.config(text="Tiempo: 0 s")
    label_estado.config(text="")

    dibujar_base()
    dibujar_discos()

ventana = tk.Tk()
ventana.title("Simulador Torre de Hanoi")
ventana.geometry("1250x650")

top = tk.Frame(ventana)
top.pack(pady=10)

btn_reset = tk.Button(top, text="Reset", command=reset)
btn_reset.pack(side="left", padx=10)

escala = tk.Scale(
    top,
    from_=1,
    to=64,
    orient="horizontal",
    label="Discos",
    length=250,
    command=actualizar_discos
)

escala.set(10)
escala.pack(side="left", padx=10)

tk.Button(top,text="5 discos",command=lambda:escala.set(5)).pack(side="left",padx=5)
tk.Button(top,text="10 discos",command=lambda:escala.set(10)).pack(side="left",padx=5)
tk.Button(top,text="30 discos",command=lambda:escala.set(30)).pack(side="left",padx=5)
tk.Button(top,text="64 discos",command=lambda:escala.set(64)).pack(side="left",padx=5)

btn_iniciar = tk.Button(top, text="Iniciar", command=iniciar)
btn_iniciar.pack(side="left", padx=10)

canvas = tk.Canvas(
    ventana,
    width=ANCHO,
    height=ALTO,
    bg="#ffffff"
)

canvas.pack(pady=20)

info = tk.Frame(ventana)
info.pack(pady=10)

label_mov = tk.Label(info,text=f"{0:,} movimientos",font=("Arial",14,"bold"),fg="blue")
label_mov.pack()

label_mejor = tk.Label(info,text="")
label_mejor.pack()

label_tiempo = tk.Label(info,text="Tiempo: 0 s")
label_tiempo.pack()

label_estado = tk.Label(info,text="",fg="red")
label_estado.pack()

dibujar_base()
actualizar_discos(escala.get())

ventana.mainloop()
