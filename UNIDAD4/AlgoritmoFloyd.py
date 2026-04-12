import tkinter as tk
from tkinter import messagebox
import math

INF = float('inf')

def floyd_warshall(n, dist):
    next_node = [[None]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if dist[i][j] != INF and i != j:
                next_node[i][j] = j

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

    return dist, next_node


def obtener_ruta(u, v, next_node):
    if next_node[u][v] is None:
        return []

    ruta = [u]
    while u != v:
        u = next_node[u][v]
        ruta.append(u)
    return ruta


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("Floyd con Grafo Visual PRO")
        self.root.geometry("1100x700")

        main = tk.Frame(root)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        tk.Label(left, text="Número de nodos").grid(row=0, column=0)

        self.entry_n = tk.Entry(left, width=10)
        self.entry_n.grid(row=0, column=1)

        tk.Button(left, text="Crear matriz",
                  command=self.crear_matriz)\
            .grid(row=1, column=0, columnspan=2, pady=5)

        self.frame_matriz = tk.Frame(left)
        self.frame_matriz.grid(row=2, column=0,
                               columnspan=2, pady=10)

        tk.Button(left, text="Calcular Floyd",
                  command=self.calcular)\
            .grid(row=3, column=0, columnspan=2, pady=5)

        tk.Label(left, text="Nodo origen").grid(row=4, column=0)

        self.origen = tk.Entry(left, width=10)
        self.origen.grid(row=4, column=1)

        tk.Label(left, text="Nodo destino").grid(row=5, column=0)

        self.destino = tk.Entry(left, width=10)
        self.destino.grid(row=5, column=1)

        tk.Button(left, text="Mostrar ruta",
                  command=self.mostrar_ruta)\
            .grid(row=6, column=0, columnspan=2, pady=5)

        result_frame = tk.Frame(left)
        result_frame.grid(row=7, column=0,
                          columnspan=2, pady=10)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")

        self.resultado = tk.Text(
            result_frame,
            height=12,
            width=40,
            yscrollcommand=scrollbar.set
        )

        self.resultado.pack()
        scrollbar.config(command=self.resultado.yview)

        right = tk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(right, bg="white")
        self.canvas.pack(fill="both", expand=True)

        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        self.entradas = []
        self.dist = []
        self.original = []
        self.next_node = []
        self.posiciones = {}

    def crear_matriz(self):

        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Ingrese un número válido")
            return

        self.entradas = []

        for i in range(n):
            fila = []
            for j in range(n):
                e = tk.Entry(self.frame_matriz, width=5, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)

                if i == j:
                    e.insert(0, "0")

                fila.append(e)
            self.entradas.append(fila)

    def calcular(self):

        try:
            n = int(self.entry_n.get())
        except:
            messagebox.showerror("Error", "Número inválido")
            return

        self.dist = []

        try:
            for i in range(n):
                fila = []
                for j in range(n):
                    val = self.entradas[i][j].get()

                    if val == "" or val.lower() in ["inf", "∞"]:
                        fila.append(INF)
                    else:
                        fila.append(float(val))

                self.dist.append(fila)
        except:
            messagebox.showerror("Error", "Datos inválidos en la matriz")
            return

        self.original = [fila[:] for fila in self.dist]

        self.dist, self.next_node = floyd_warshall(n, self.dist)

        for i in range(n):
            if self.dist[i][i] < 0:
                messagebox.showwarning("Advertencia", "Hay ciclo negativo")
                break

        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, "Matriz final:\n")

        for fila in self.dist:
            self.resultado.insert(tk.END, str(fila) + "\n")

        self.dibujar_grafo()

    def ajustar_linea(self, x1, y1, x2, y2, offset=25):

        dx = x2 - x1
        dy = y2 - y1

        dist = math.hypot(dx, dy)

        if dist == 0:
            return x1, y1, x2, y2

        return (
            x1 + dx/dist * offset,
            y1 + dy/dist * offset,
            x2 - dx/dist * offset,
            y2 - dy/dist * offset
        )

    def dibujar_grafo(self):

        self.canvas.delete("all")

        n = len(self.original)

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        cx = width // 2
        cy = height // 2

        radio = min(width, height) // 2 - 120

        self.posiciones = {}

        for i in range(n):
            ang = 2 * math.pi * i / n
            x = cx + radio * math.cos(ang)
            y = cy + radio * math.sin(ang)
            self.posiciones[i] = (x, y)

        for i in range(n):
            for j in range(n):

                if self.original[i][j] != INF and i != j:

                    x1, y1 = self.posiciones[i]
                    x2, y2 = self.posiciones[j]

                    x1n, y1n, x2n, y2n = self.ajustar_linea(x1, y1, x2, y2)

                    self.canvas.create_line(
                        x1n, y1n, x2n, y2n,
                        fill="gray",
                        width=2,
                        arrow=tk.LAST
                    )

                    mx = (x1n + x2n)/2
                    my = (y1n + y2n)/2

                    dx = x2n - x1n
                    dy = y2n - y1n
                    dist = math.hypot(dx, dy)

                    if dist != 0:
                        offset = 12
                        mx += -dy/dist * offset
                        my += dx/dist * offset

                    self.canvas.create_text(
                        mx, my,
                        text=str(int(self.original[i][j])),
                        font=("Arial", 10, "bold")
                    )

        for i, (x, y) in self.posiciones.items():
            self.canvas.create_oval(
                x-23, y-23, x+23, y+23,
                fill="#d7ecff", width=2
            )
            self.canvas.create_text(
                x, y,
                text=str(i+1),
                font=("Arial", 11, "bold")
            )

    def mostrar_ruta(self):

        if not self.next_node:
            messagebox.showerror("Error", "Primero calcula Floyd")
            return

        try:
            u = int(self.origen.get()) - 1
            v = int(self.destino.get()) - 1
        except:
            messagebox.showerror("Error", "Nodos inválidos")
            return

        if u < 0 or v < 0 or u >= len(self.dist) or v >= len(self.dist):
            messagebox.showerror("Error", "Fuera de rango")
            return

        ruta = obtener_ruta(u, v, self.next_node)

        if not ruta:
            messagebox.showinfo("Resultado", "No hay ruta")
            return

        ruta_visual = [x+1 for x in ruta]
        distancia = self.dist[u][v]

        self.resultado.insert(
            tk.END,
            f"\nRuta: {' → '.join(map(str, ruta_visual))}"
            f"\nDistancia = {distancia}\n"
        )

        for i in range(len(ruta)-1):

            x1, y1 = self.posiciones[ruta[i]]
            x2, y2 = self.posiciones[ruta[i+1]]

            x1n, y1n, x2n, y2n = self.ajustar_linea(x1, y1, x2, y2)

            self.canvas.create_line(
                x1n, y1n, x2n, y2n,
                fill="red",
                width=4,
                arrow=tk.LAST
            )


root = tk.Tk()
app = App(root)
root.mainloop()
