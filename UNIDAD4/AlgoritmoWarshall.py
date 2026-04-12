import tkinter as tk
from tkinter import messagebox
import math

def warshall(matriz):
    n = len(matriz)

    w = []
    pasos = []

    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(1 if matriz[i][j] != 0 else 0)
        w.append(fila)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if w[i][j] == 0 and (w[i][k] and w[k][j]):
                    pasos.append(f"Se encontró camino: {i} → {j} pasando por {k}")
                w[i][j] = w[i][j] or (w[i][k] and w[k][j])

    return w, pasos


def crear_matriz():
    try:
        n = int(entry_n.get())
    except:
        messagebox.showerror("Error", "Número inválido")
        return

    for w in frame_matriz.winfo_children():
        w.destroy()

    global entradas
    entradas = []

    for j in range(n):
        tk.Label(frame_matriz, text=j, fg="white", bg="#1e1e1e").grid(row=0, column=j+1)

    for i in range(n):
        fila = []
        tk.Label(frame_matriz, text=i, fg="white", bg="#1e1e1e").grid(row=i+1, column=0)

        for j in range(n):
            e = tk.Entry(frame_matriz, width=5, justify="center")
            e.grid(row=i+1, column=j+1, padx=3, pady=3)
            e.insert(0, "0")
            fila.append(e)

        entradas.append(fila)


def obtener_matriz():
    matriz = []
    try:
        for fila in entradas:
            fila_val = []
            for e in fila:
                fila_val.append(int(e.get()))
            matriz.append(fila_val)
        return matriz
    except:
        messagebox.showerror("Error", "Usa solo 0 y 1")
        return None


def mostrar_matriz(matriz):
    for w in frame_resultado.winfo_children():
        w.destroy()

    n = len(matriz)

    tk.Label(frame_resultado, text="Cierre Transitivo",
             fg="yellow", bg="#1e1e1e",
             font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=n+1)

    for j in range(n):
        tk.Label(frame_resultado, text=j, fg="white", bg="#1e1e1e").grid(row=1, column=j+1)

    for i in range(n):
        tk.Label(frame_resultado, text=i, fg="white", bg="#1e1e1e").grid(row=i+2, column=0)

        for j in range(n):
            tk.Label(
                frame_resultado,
                text=str(matriz[i][j]),
                width=5,
                bg="#2e2e2e",
                fg="white",
                borderwidth=1,
                relief="solid"
            ).grid(row=i+2, column=j+1, padx=2, pady=2)


def mostrar_pasos(pasos):
    texto_pasos.delete("1.0", tk.END)

    if not pasos:
        texto_pasos.insert(tk.END, "No se encontraron caminos nuevos.")
    else:
        for p in pasos:
            texto_pasos.insert(tk.END, p + "\n")


def generar_posiciones(n):
    posiciones = {}
    radio = 180
    cx, cy = 350, 250

    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + radio * math.cos(angulo)
        y = cy + radio * math.sin(angulo)
        posiciones[i] = (x, y)

    return posiciones


def ajustar_linea(x1, y1, x2, y2, offset=25):
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


def dibujar_grafo(original, cierre):
    canvas.delete("all")

    n = len(original)
    posiciones = generar_posiciones(n)

    for i in range(n):
        for j in range(n):
            if cierre[i][j] == 1 and i != j:

                x1, y1 = posiciones[i]
                x2, y2 = posiciones[j]

                x1n, y1n, x2n, y2n = ajustar_linea(x1, y1, x2, y2)

                color = "black" if original[i][j] == 1 else "red"

                canvas.create_line(
                    x1n, y1n, x2n, y2n,
                    arrow=tk.LAST,
                    width=2,
                    fill=color
                )

    for i in range(n):
        if cierre[i][i] == 1:
            x, y = posiciones[i]
            canvas.create_oval(
                x-35, y-35, x+35, y+35,
                outline="red", width=2
            )

    for i, (x, y) in posiciones.items():
        canvas.create_oval(x-25, y-25, x+25, y+25,
                           fill="lightblue", width=2)
        canvas.create_text(x, y, text=str(i),
                           font=("Arial", 12, "bold"))


def calcular():
    matriz = obtener_matriz()
    if matriz is None:
        return
    
    resultado, pasos = warshall(matriz)

    mostrar_matriz(resultado)
    dibujar_grafo(matriz, resultado)
    mostrar_pasos(pasos)


root = tk.Tk()
root.title("Algoritmo de Warshall PRO")
root.geometry("1200x750")
root.configure(bg="#1e1e1e")

main = tk.Frame(root, bg="#1e1e1e")
main.pack(fill="both", expand=True)

left = tk.Frame(main, bg="#1e1e1e")
left.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

tk.Label(left, text="Algoritmo de Warshall",
         font=("Arial", 14, "bold"),
         fg="white", bg="#1e1e1e").pack(pady=10)

frame_top = tk.Frame(left, bg="#1e1e1e")
frame_top.pack()

tk.Label(frame_top, text="Nodos:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
entry_n = tk.Entry(frame_top, width=5)
entry_n.pack(side=tk.LEFT, padx=10)

tk.Button(frame_top, text="Crear matriz", command=crear_matriz).pack(side=tk.LEFT)

frame_matriz = tk.Frame(left, bg="#1e1e1e")
frame_matriz.pack(pady=20)

tk.Button(left, text="Calcular", command=calcular,
          bg="#4CAF50", fg="white").pack(pady=10)

frame_resultado = tk.Frame(left, bg="#1e1e1e")
frame_resultado.pack(pady=10)

texto_pasos = tk.Text(left, height=10, width=40, bg="#2e2e2e", fg="white")
texto_pasos.pack(pady=10)

right = tk.Frame(main, bg="#1e1e1e")
right.grid(row=0, column=1, sticky="nsew")

canvas = tk.Canvas(right, width=700, height=500, bg="white")
canvas.pack(fill="both", expand=True, padx=10, pady=10)

main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=1)

root.mainloop()
