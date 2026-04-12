import tkinter as tk
from tkinter import messagebox
import math

class KruskalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Kruskal")

        self.canvas = tk.Canvas(root, width=900, height=500, bg="white")
        self.canvas.pack()

        self.nodes = {}
        self.edges = []
        self.edge_lines = {}

        self.max_edges = 0
        self.current_edges = 0

        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Cantidad de aristas").grid(row=0, column=0)
        self.edge_count_entry = tk.Entry(frame, width=5)
        self.edge_count_entry.grid(row=0, column=1)

        tk.Button(frame, text="Definir", command=self.set_edge_count).grid(row=0, column=2)

        tk.Label(frame, text="Nodo A").grid(row=1, column=0)
        self.n1 = tk.Entry(frame, width=5)
        self.n1.grid(row=1, column=1)

        tk.Label(frame, text="Nodo B").grid(row=1, column=2)
        self.n2 = tk.Entry(frame, width=5)
        self.n2.grid(row=1, column=3)

        tk.Label(frame, text="Peso").grid(row=1, column=4)
        self.weight = tk.Entry(frame, width=5)
        self.weight.grid(row=1, column=5)

        self.add_btn = tk.Button(frame, text="Agregar arista", command=self.add_edge, state="disabled")
        self.add_btn.grid(row=1, column=6)

        tk.Button(frame, text="Ejecutar Kruskal", command=self.kruskal).grid(row=1, column=7)
        tk.Button(frame, text="Limpiar", command=self.clear).grid(row=1, column=8)

        self.status_label = tk.Label(frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=9)

    def set_edge_count(self):
        try:
            self.max_edges = int(self.edge_count_entry.get())
            self.current_edges = 0
            self.add_btn.config(state="normal")
            self.status_label.config(text=f"Faltan {self.max_edges} aristas")
        except:
            messagebox.showerror("Error", "Número inválido")

    def add_node(self, node):
        if node not in self.nodes:
            n = len(self.nodes)
            total = max(6, n + 1)

            angle = 2 * math.pi * n / total
            x = 450 + 200 * math.cos(angle)
            y = 250 + 200 * math.sin(angle)

            self.nodes[node] = (x, y)

            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="yellow", outline="black")
            self.canvas.create_text(x, y, text=node, font=("Arial", 10, "bold"))

    def add_edge(self):
        if self.current_edges >= self.max_edges:
            messagebox.showinfo("Info", "Ya ingresaste todas las aristas")
            return

        n1 = self.n1.get()
        n2 = self.n2.get()
        w = self.weight.get()

        if not n1 or not n2 or not w:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        try:
            w = int(w)
        except:
            messagebox.showerror("Error", "Peso inválido")
            return

        if any((n1 == a and n2 == b) or (n1 == b and n2 == a) for a, b, _ in self.edges):
            messagebox.showwarning("Aviso", "Esa arista ya existe")
            return

        self.add_node(n1)
        self.add_node(n2)

        self.edges.append((n1, n2, w))
        self.current_edges += 1

        x1, y1 = self.nodes[n1]
        x2, y2 = self.nodes[n2]

        line = self.canvas.create_line(
            x1, y1, x2, y2,
            width=2,
            fill="black"
        )

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        text = self.canvas.create_text(
            mx, my,
            text=str(w),
            fill="blue",
            font=("Arial", 10, "bold")
        )

        bbox = self.canvas.bbox(text)
        rect = self.canvas.create_rectangle(bbox, fill="white", outline="")
        self.canvas.tag_lower(rect, text)

        key = tuple(sorted([n1, n2])) + (w,)
        self.edge_lines[key] = line

        restantes = self.max_edges - self.current_edges
        self.status_label.config(text=f"Faltan {restantes} aristas")

        if restantes == 0:
            self.add_btn.config(state="disabled")
            messagebox.showinfo("Listo", "Ya puedes ejecutar Kruskal")

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal(self):
        result = []

        edges_sorted = sorted(self.edges, key=lambda x: x[2])

        parent = {}
        rank = {}

        for node in self.nodes:
            parent[node] = node
            rank[node] = 0

        for line in self.edge_lines.values():
            self.canvas.itemconfig(line, fill="black", width=2)

        for n1, n2, w in edges_sorted:
            x = self.find(parent, n1)
            y = self.find(parent, n2)

            key = tuple(sorted([n1, n2])) + (w,)

            self.canvas.itemconfig(self.edge_lines[key], fill="orange", width=3)
            self.root.update()
            self.root.after(400)

            if x != y:
                result.append((n1, n2, w))
                self.union(parent, rank, x, y)
                self.canvas.itemconfig(self.edge_lines[key], fill="red", width=4)
            else:
                self.canvas.itemconfig(self.edge_lines[key], fill="gray", width=2)

            if len(result) == len(self.nodes) - 1:
                break

        costo = sum(w for _, _, w in result)

        messagebox.showinfo("Resultado", f"Costo mínimo: {costo}\nAristas: {result}")

    def clear(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.edge_lines.clear()

        self.max_edges = 0
        self.current_edges = 0

        self.add_btn.config(state="disabled")
        self.status_label.config(text="")

        self.n1.delete(0, tk.END)
        self.n2.delete(0, tk.END)
        self.weight.delete(0, tk.END)
        self.edge_count_entry.delete(0, tk.END)


root = tk.Tk()
app = KruskalApp(root)

root.bind("<Return>", lambda event: app.add_edge())

root.mainloop()
