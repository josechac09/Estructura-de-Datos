import heapq
from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk, scrolledtext

ESTADOS = [
    "CDMX",
    "Jalisco",
    "Nuevo Leon",
    "Yucatan",
    "Veracruz",
    "Oaxaca",
    "Puebla"
]

CONEXIONES = [
    ("CDMX","Jalisco",350),
    ("CDMX","Nuevo Leon",800),
    ("CDMX","Veracruz",320),
    ("CDMX","Puebla",130),
    ("CDMX","Oaxaca",480),

    ("Jalisco","Nuevo Leon",700),
    ("Jalisco","Veracruz",550),
    ("Jalisco","Puebla",400),

    ("Nuevo Leon","Veracruz",900),
    ("Nuevo Leon","Yucatan",1800),

    ("Yucatan","Veracruz",450),
    ("Yucatan","Oaxaca",560),

    ("Veracruz","Oaxaca",380),
    ("Veracruz","Puebla",260),

    ("Oaxaca","Puebla",200),
]

N = len(ESTADOS)
indice = {e:i for i,e in enumerate(ESTADOS)}
GRAFO = {i:[] for i in range(N)}

for a,b,c in CONEXIONES:
    i,j = indice[a], indice[b]
    GRAFO[i].append((j,c))
    GRAFO[j].append((i,c))

def dijkstra(origen):
    dist = [float("inf")] * N
    dist[origen] = 0
    pq = [(0, origen)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, c in GRAFO[u]:
            if dist[u] + c < dist[v]:
                dist[v] = dist[u] + c
                heapq.heappush(pq, (dist[v], v))

    return dist

def recorrido_A(inicio):
    nodos = list(range(N))
    nodos.remove(inicio)

    mejor = float("inf")
    mejor_ruta = None

    for perm in permutations(nodos):
        ruta = [inicio] + list(perm)

        costo = 0
        valido = True

        for i in range(len(ruta)-1):
            dist = dijkstra(ruta[i])

            if dist[ruta[i+1]] == float("inf"):
                valido = False
                break

            costo += dist[ruta[i+1]]

        if valido and costo < mejor:
            mejor = costo
            mejor_ruta = ruta

    return mejor_ruta, mejor

def recorrido_B(inicio):
    ruta, costoA = recorrido_A(inicio)

    ultimo = ruta[-1]
    dist = dijkstra(ultimo)

    menor = float("inf")
    nodo_repetido = None

    for i in range(N):
        if i != ultimo and dist[i] < menor:
            menor = dist[i]
            nodo_repetido = i

    rutaB = ruta + [nodo_repetido]
    costoB = costoA + menor

    return rutaB, costoB

def matriz():
    M = [[0]*N for _ in range(N)]

    for i in GRAFO:
        for j,c in GRAFO[i]:
            M[i][j] = c

    texto = "MATRIZ DE ADYACENCIA\n\n"
    texto += "     "

    for e in ESTADOS:
        texto += f"{e[:3]:>6}"

    texto += "\n"

    for i in range(N):
        texto += f"{ESTADOS[i][:3]:>6}"
        for j in range(N):
            texto += f"{M[i][j]:>6}"
        texto += "\n"

    return texto

def dibujar(ruta=None, titulo="GRAFO"):
    G = nx.Graph()

    for i in range(N):
        G.add_node(i, label=ESTADOS[i])

    for u in GRAFO:
        for v,c in GRAFO[u]:
            if u < v:
                G.add_edge(u,v,weight=c)

    pos = nx.spring_layout(G, seed=7)

    plt.figure(figsize=(7,6))

    edges = G.edges()
    colores = "gray"
    ancho = 1.5

    if ruta:
        aristas_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        colores = ["red" if (e in aristas_ruta or (e[1],e[0]) in aristas_ruta) else "gray" for e in edges]
        ancho = [3 if (e in aristas_ruta or (e[1],e[0]) in aristas_ruta) else 1 for e in edges]

    nx.draw(G, pos, with_labels=True,
            labels={i:ESTADOS[i] for i in range(N)},
            node_color="lightblue",
            node_size=2000)

    nx.draw_networkx_edges(G, pos, edge_color=colores, width=ancho)

    etiquetas = {(u,v):d["weight"] for u,v,d in G.edges(data=True)}

    u = indice["CDMX"]
    v = indice["Jalisco"]

    etiquetas_filtradas = {
        (a,b):w for (a,b),w in etiquetas.items()
        if not ((a==u and b==v) or (a==v and b==u))
    }

    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_filtradas)

    x1, y1 = pos[u]
    x2, y2 = pos[v]

    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2

    plt.text(
        xm + 0.08,  
        ym,
        "350",
        fontsize=9,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
    )

    plt.title(titulo)
    plt.show()

def mostrar(ruta, costo):
    nombres = [ESTADOS[i] for i in ruta]
    return " -> ".join(nombres) + f"\nCosto total: {costo}"

class GrafoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafos - Estados de México")
        self.root.geometry("900x700")

        frame = tk.Frame(root)
        frame.pack()

        botones = [
            ("Ver Conexiones", self.ver_conexiones),
            ("Matriz", self.ver_matriz),
            ("Recorrido A", self.recorrido_a),
            ("Recorrido B", self.recorrido_b),
            ("Grafo", self.ver_grafo)
        ]

        for i,(txt,cmd) in enumerate(botones):
            tk.Button(frame,text=txt,command=cmd,width=20).grid(row=i,column=0,pady=5)

        self.combo = ttk.Combobox(root, values=ESTADOS)
        self.combo.set(ESTADOS[0])
        self.combo.pack(pady=10)

        self.texto = scrolledtext.ScrolledText(root,width=100,height=25)
        self.texto.pack()

    def mostrar(self, txt):
        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.END, txt)

    def ver_conexiones(self):
        txt = ""
        for i in GRAFO:
            txt += f"\n{ESTADOS[i]}:\n"
            for j,c in GRAFO[i]:
                txt += f" -> {ESTADOS[j]} ({c})\n"
        self.mostrar(txt)

    def ver_matriz(self):
        self.mostrar(matriz())

    def recorrido_a(self):
        inicio = indice[self.combo.get()]
        ruta,costo = recorrido_A(inicio)
        self.mostrar("RECORRIDO A\n" + mostrar(ruta,costo))
        dibujar(ruta,"Recorrido A")

    def recorrido_b(self):
        inicio = indice[self.combo.get()]
        ruta,costo = recorrido_B(inicio)
        self.mostrar("RECORRIDO B\n" + mostrar(ruta,costo))
        dibujar(ruta,"Recorrido B")

    def ver_grafo(self):
        dibujar()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoGUI(root)
    root.mainloop()
