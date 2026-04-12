import tkinter as tk
from tkinter import messagebox
import heapq
import math

grafo = {
    0: {1: 2, 2: 6},
    1: {0: 2, 3: 5},
    2: {0: 6, 3: 8},
    3: {1: 5, 2: 8, 4: 10, 5: 15},
    4: {3: 10, 5: 6, 6: 2},
    5: {3: 15, 4: 6, 6: 6},
    6: {4: 2, 5: 6}
}

pos = {
    0: (80, 200),
    1: (180, 100),
    2: (180, 300),
    3: (350, 200),
    4: (520, 300),
    5: (520, 100),
    6: (650, 200)
}

def dijkstra(grafo, inicio):

    dist = {n: float('inf') for n in grafo}
    prev = {n: None for n in grafo}

    dist[inicio] = 0

    pq = [(0, inicio)]

    while pq:

        d, nodo = heapq.heappop(pq)

        if d > dist[nodo]:
            continue

        for vecino, peso in grafo[nodo].items():

            nueva = d + peso

            if nueva < dist[vecino]:

                dist[vecino] = nueva
                prev[vecino] = nodo

                heapq.heappush(pq, (nueva, vecino))

    return dist, prev


def reconstruir(prev, destino):

    camino = []

    while destino is not None:

        camino.insert(0, destino)
        destino = prev[destino]

    return camino


def agregar_nodo():

    try:

        nuevo = int(nuevo_nodo_entry.get())

        if nuevo in grafo:

            messagebox.showerror("Error", "El nodo ya existe")
            return

        grafo[nuevo] = {}


        angulo = len(pos) * 40

        x = 350 + 220 * math.cos(math.radians(angulo))
        y = 180 + 150 * math.sin(math.radians(angulo))

        pos[nuevo] = (x, y)

        dibujar()

    except:

        messagebox.showerror("Error", "Número inválido")


def eliminar_nodo():

    try:

        nodo = int(eliminar_nodo_entry.get())

        if nodo not in grafo:

            messagebox.showerror("Error", "Nodo no existe")
            return

      
        for n in grafo:

            if nodo in grafo[n]:

                del grafo[n][nodo]

        
        del grafo[nodo]
        del pos[nodo]

        dibujar()

    except:

        messagebox.showerror("Error", "Número inválido")


def cambiar_costo():

    try:

        n1 = int(origen_entry.get())
        n2 = int(destino_entry.get())
        nuevo = int(costo_entry.get())

        if n1 not in grafo or n2 not in grafo:

            messagebox.showerror("Error", "Nodo no existe")
            return

        grafo[n1][n2] = nuevo
        grafo[n2][n1] = nuevo

        dibujar()

        messagebox.showinfo("Listo", "Costo actualizado")

    except:

        messagebox.showerror("Error", "Datos inválidos")

def dibujar(camino=None):

    canvas.delete("all")

    camino_edges = set()

    if camino:

        for i in range(len(camino) - 1):

            camino_edges.add((camino[i], camino[i+1]))
            camino_edges.add((camino[i+1], camino[i]))

    
    for nodo in grafo:

        for vecino, peso in grafo[nodo].items():

            if nodo > vecino:
                continue

            x1, y1 = pos[nodo]
            x2, y2 = pos[vecino]

            es_camino = (nodo, vecino) in camino_edges

            color = "#e74c3c" if es_camino else "#2c3e50"
            grosor = 5 if es_camino else 2

            canvas.create_line(
                x1, y1,
                x2, y2,
                fill=color,
                width=grosor
            )

            mx, my = (x1+x2)/2, (y1+y2)/2

            canvas.create_oval(mx-12, my-12, mx+12, my+12, fill="white")

            canvas.create_text(
                mx,
                my,
                text=str(peso),
                fill="#2980b9",
                font=("Arial", 11, "bold")
            )

    for nodo, (x, y) in pos.items():

        canvas.create_oval(
            x-20,
            y-20,
            x+20,
            y+20,
            fill="#3498db"
        )

        canvas.create_text(
            x,
            y,
            text=str(nodo),
            fill="white",
            font=("Arial", 13, "bold")
        )

def calcular():

    try:

        destino = int(destino_final.get())

        if destino not in grafo:

            messagebox.showerror("Error", "Nodo inválido")
            return

        dist, prev = dijkstra(grafo, 0)

        camino = reconstruir(prev, destino)

        dibujar(camino)

        resultado.config(
            text=f"Camino: {' -> '.join(map(str, camino))} | Costo: {dist[destino]}"
        )

    except:

        messagebox.showerror("Error", "Ingresa número válido")


ventana = tk.Tk()
ventana.title("Dijkstra editable")

canvas = tk.Canvas(
    ventana,
    width=750,
    height=360
)

canvas.pack()

frame0 = tk.Frame(ventana)
frame0.pack(pady=5)

tk.Label(frame0, text="Nuevo nodo").pack(side="left")

nuevo_nodo_entry = tk.Entry(frame0, width=5)
nuevo_nodo_entry.pack(side="left")

tk.Button(
    frame0,
    text="Agregar",
    command=agregar_nodo
).pack(side="left")

tk.Label(frame0, text="Eliminar nodo").pack(side="left")

eliminar_nodo_entry = tk.Entry(frame0, width=5)
eliminar_nodo_entry.pack(side="left")

tk.Button(
    frame0,
    text="Eliminar",
    command=eliminar_nodo
).pack(side="left")

frame1 = tk.Frame(ventana)
frame1.pack(pady=5)

tk.Label(frame1, text="Nodo 1").pack(side="left")

origen_entry = tk.Entry(frame1, width=5)
origen_entry.pack(side="left")

tk.Label(frame1, text="Nodo 2").pack(side="left")

destino_entry = tk.Entry(frame1, width=5)
destino_entry.pack(side="left")

tk.Label(frame1, text="Costo").pack(side="left")

costo_entry = tk.Entry(frame1, width=5)
costo_entry.pack(side="left")

tk.Button(
    frame1,
    text="Cambiar costo",
    command=cambiar_costo
).pack(side="left")

frame2 = tk.Frame(ventana)
frame2.pack(pady=5)

tk.Label(frame2, text="Destino final").pack(side="left")

destino_final = tk.Entry(frame2, width=5)
destino_final.pack(side="left")

tk.Button(
    frame2,
    text="Calcular ruta",
    command=calcular
).pack(side="left")


resultado = tk.Label(
    ventana,
    text="",
    font=("Arial", 12, "bold")
)

resultado.pack(pady=5)


dibujar()

ventana.mainloop()
