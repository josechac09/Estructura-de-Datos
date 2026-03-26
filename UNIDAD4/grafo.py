import tkinter as tk
from tkinter import messagebox
import math

# =========================
# CLASE GRAFO
# =========================
class Grafo:
    def _init_(self, dirigido=False):
        self.dirigido = dirigido
        self.vertices = []
        self.aristas = []

    def esDirigido(self):
        return self.dirigido

    def insertaVertice(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
            return True
        return False

    def insertaArista(self, v, w):
        if v in self.vertices and w in self.vertices:
            self.aristas.append((v, w))
            return True
        return False

    def eliminaVertice(self, v):
        if v in self.vertices:
            self.vertices.remove(v)
            self.aristas = [(a, b) for (a, b) in self.aristas if a != v and b != v]

    def eliminaArista(self, v, w):
        if (v, w) in self.aristas:
            self.aristas.remove((v, w))

    def numVertices(self):
        return len(self.vertices)

    def numAristas(self):
        return len(self.aristas)

    def verticesAdyacentes(self, v):
        return [w for (a, w) in self.aristas if a == v]

    def grado(self, v):
        return len(self.verticesAdyacentes(v))

    def esAdyacente(self, v, w):
        return (v, w) in self.aristas


# =========================
# INTERFAZ
# =========================
class App:
    def _init_(self, root):
        self.root = root
        self.root.title("Grafo PRO sin librerías")
        self.root.geometry("1000x650")

        self.grafo = None
        self.posiciones = {}

        self.inicio()

    def inicio(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Selecciona el tipo de grafo", font=("Arial", 16)).pack(pady=10)

        tk.Button(frame, text="No Dirigido", width=20,
                  command=lambda: self.crear_grafo(False)).pack(pady=5)

        tk.Button(frame, text="Dirigido", width=20,
                  command=lambda: self.crear_grafo(True)).pack(pady=5)

    def crear_grafo(self, dirigido):
        self.grafo = Grafo(dirigido)
        messagebox.showinfo("INFO", f"Grafo {'Dirigido' if dirigido else 'No Dirigido'} creado")
        self.menu()

    def menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Panel izquierdo
        panel = tk.Frame(self.root)
        panel.pack(side="left", padx=10)

        tk.Label(panel, text="Controles", font=("Arial", 14)).pack(pady=10)

        self.v1 = tk.Entry(panel)
        self.v2 = tk.Entry(panel)

        self.v1.pack(pady=5)
        self.v2.pack(pady=5)

        tk.Button(panel, text="Agregar Vértice", command=self.agregar_vertice).pack(pady=5)
        tk.Button(panel, text="Agregar Arista", command=self.agregar_arista).pack(pady=5)
        tk.Button(panel, text="Eliminar Vértice", command=self.eliminar_vertice).pack(pady=5)
        tk.Button(panel, text="Eliminar Arista", command=self.eliminar_arista).pack(pady=5)
        tk.Button(panel, text="Info Grafo", command=self.info).pack(pady=5)

        # Canvas (dibujo)
        self.canvas = tk.Canvas(self.root, bg="white", width=700, height=600)
        self.canvas.pack(side="right")

    # =========================
    # FUNCIONES
    # =========================

    def agregar_vertice(self):
        v = self.v1.get()
        if self.grafo.insertaVertice(v):
            self.calcular_posiciones()
            self.dibujar()
        else:
            messagebox.showerror("Error", "Ya existe")

    def agregar_arista(self):
        v = self.v1.get()
        w = self.v2.get()
        if self.grafo.insertaArista(v, w):
            self.dibujar()
        else:
            messagebox.showerror("Error", "Error en arista")

    def eliminar_vertice(self):
        v = self.v1.get()
        self.grafo.eliminaVertice(v)
        self.calcular_posiciones()
        self.dibujar()

    def eliminar_arista(self):
        v = self.v1.get()
        w = self.v2.get()
        self.grafo.eliminaArista(v, w)
        self.dibujar()

    def info(self):
        tipo = "Dirigido" if self.grafo.esDirigido() else "No Dirigido"
        messagebox.showinfo("INFO",
                            f"Tipo: {tipo}\nVertices: {self.grafo.numVertices()}\nAristas: {self.grafo.numAristas()}")

    # =========================
    # DIBUJO
    # =========================

    def calcular_posiciones(self):
        n = len(self.grafo.vertices)
        if n == 0:
            return

        radio = 200
        centro_x = 350
        centro_y = 300

        self.posiciones = {}

        for i, v in enumerate(self.grafo.vertices):
            angulo = 2 * math.pi * i / n
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            self.posiciones[v] = (x, y)

    def dibujar(self):
        self.canvas.delete("all")

        # Dibujar aristas
        for v, w in self.grafo.aristas:
            if v in self.posiciones and w in self.posiciones:
                x1, y1 = self.posiciones[v]
                x2, y2 = self.posiciones[w]

                self.canvas.create_line(x1, y1, x2, y2, width=2)

                # Flecha si es dirigido
                if self.grafo.esDirigido():
                    self.canvas.create_line(x1, y1, x2, y2,
                                            arrow=tk.LAST, width=2)

        # Dibujar vértices
        for v, (x, y) in self.posiciones.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="skyblue")
            self.canvas.create_text(x, y, text=v, font=("Arial", 12, "bold"))


# =========================
# EJECUCIÓN
# =========================
root = tk.Tk()
app = App(root)
root.mainloop()
