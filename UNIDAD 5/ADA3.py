import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import csv
import time

archivo1_datos = []
archivo2_datos = []

def leer_archivo(ruta):

    datos = []

    if ruta.endswith(".txt"):

        with open(ruta, "r") as f:
            contenido = f.read()

        contenido = contenido.replace("\n", ",")

        datos = list(
            map(
                int,
                filter(None, contenido.split(","))
            )
        )

    # ==========================================
    # CSV
    # ==========================================

    elif ruta.endswith(".csv"):

        with open(ruta, newline='') as f:

            lector = csv.reader(f)

            for fila in lector:

                for valor in fila:

                    if valor.strip() != "":
                        datos.append(int(valor))

    # ==========================================
    # JSON
    # ==========================================

    elif ruta.endswith(".json"):

        with open(ruta, "r") as f:
            datos = json.load(f)

    return datos

# ==========================================
# CARGAR ARCHIVO 1
# ==========================================

def cargar_archivo1():

    global archivo1_datos

    ruta = filedialog.askopenfilename(
        title="Seleccionar Archivo 1",
        filetypes=[
            ("TXT", "*.txt"),
            ("CSV", "*.csv"),
            ("JSON", "*.json")
        ]
    )

    if not ruta:
        return

    try:

        archivo1_datos = sorted(leer_archivo(ruta))

        entrada1.delete(0, tk.END)

        entrada1.insert(
            0,
            ",".join(map(str, archivo1_datos))
        )

        messagebox.showinfo(
            "Archivo 1",
            "Archivo 1 cargado correctamente"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo cargar el archivo 1\n{e}"
        )

# ==========================================
# CARGAR ARCHIVO 2
# ==========================================

def cargar_archivo2():

    global archivo2_datos

    ruta = filedialog.askopenfilename(
        title="Seleccionar Archivo 2",
        filetypes=[
            ("TXT", "*.txt"),
            ("CSV", "*.csv"),
            ("JSON", "*.json")
        ]
    )

    if not ruta:
        return

    try:

        archivo2_datos = sorted(leer_archivo(ruta))

        entrada2.delete(0, tk.END)

        entrada2.insert(
            0,
            ",".join(map(str, archivo2_datos))
        )

        messagebox.showinfo(
            "Archivo 2",
            "Archivo 2 cargado correctamente"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo cargar el archivo 2\n{e}"
        )

# ==========================================
# GUARDAR RESULTADO
# ==========================================

def guardar_resultado(datos):

    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("TXT", "*.txt")
        ]
    )

    if archivo:

        with open(archivo, "w") as f:
            f.write(str(datos))

        messagebox.showinfo(
            "Guardado",
            "Resultado guardado correctamente"
        )

# ==========================================
# DIBUJAR BARRAS
# ==========================================

def dibujar(datos, color="skyblue"):

    canvas.delete("all")

    if not datos:
        return

    ancho_canvas = 950
    alto_canvas = 300

    ancho_barra = ancho_canvas / len(datos)

    maximo = max(datos)

    if maximo == 0:
        maximo = 1

    for i, valor in enumerate(datos):

        x1 = i * ancho_barra

        y1 = alto_canvas - (
            (valor / maximo) * 250
        )

        x2 = (i + 1) * ancho_barra - 5
        y2 = alto_canvas

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color
        )

        canvas.create_text(
            x1 + ancho_barra / 2 - 5,
            y1 - 10,
            text=str(valor),
            font=("Arial", 10, "bold")
        )

    ventana.update()
    time.sleep(0.4)

# ==========================================
# INTERCALACIÓN
# ==========================================

def intercalacion_real():

    resultado.delete(1.0, tk.END)

    if not archivo1_datos or not archivo2_datos:

        messagebox.showerror(
            "Error",
            "Debe cargar ambos archivos"
        )

        return

    lista1 = archivo1_datos
    lista2 = archivo2_datos

    resultado.insert(
        tk.END,
        "=========== INTERCALACIÓN ===========\n\n"
    )

    resultado.insert(
        tk.END,
        f"Archivo 1:\n{lista1}\n\n"
    )

    resultado.insert(
        tk.END,
        f"Archivo 2:\n{lista2}\n\n"
    )

    i = 0
    j = 0

    fusion = []

    while i < len(lista1) and j < len(lista2):

        resultado.insert(
            tk.END,
            f"Comparando {lista1[i]} y {lista2[j]}\n"
        )

        if lista1[i] < lista2[j]:

            fusion.append(lista1[i])

            resultado.insert(
                tk.END,
                f"Se agrega {lista1[i]} del Archivo 1\n\n"
            )

            i += 1

        else:

            fusion.append(lista2[j])

            resultado.insert(
                tk.END,
                f"Se agrega {lista2[j]} del Archivo 2\n\n"
            )

            j += 1

        dibujar(fusion, "lightgreen")

    while i < len(lista1):

        fusion.append(lista1[i])

        resultado.insert(
            tk.END,
            f"Se agrega restante {lista1[i]} del Archivo 1\n"
        )

        i += 1

        dibujar(fusion, "green")

    while j < len(lista2):

        fusion.append(lista2[j])

        resultado.insert(
            tk.END,
            f"Se agrega restante {lista2[j]} del Archivo 2\n"
        )

        j += 1

        dibujar(fusion, "green")

    resultado.insert(
        tk.END,
        "\n=========== RESULTADO FINAL ===========\n"
    )

    resultado.insert(
        tk.END,
        f"{fusion}\n"
    )

    dibujar(fusion, "blue")

    guardar_resultado(fusion)

# ==========================================
# MEZCLA DIRECTA
# ==========================================

def fusionar(izquierda, derecha):

    resultado_local = []

    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):

        if izquierda[i] < derecha[j]:

            resultado_local.append(izquierda[i])
            i += 1

        else:

            resultado_local.append(derecha[j])
            j += 1

    resultado_local.extend(izquierda[i:])
    resultado_local.extend(derecha[j:])

    resultado.insert(
        tk.END,
        f"Mezcla: {resultado_local}\n"
    )

    dibujar(resultado_local, "orange")

    return resultado_local

def merge_sort(lista):

    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2

    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])

    return fusionar(izquierda, derecha)

def mezcla_directa():

    resultado.delete(1.0, tk.END)

    if not archivo1_datos:

        messagebox.showerror(
            "Error",
            "Debe cargar el Archivo 1"
        )

        return

    resultado.insert(
        tk.END,
        "=========== MEZCLA DIRECTA ===========\n\n"
    )

    resultado.insert(
        tk.END,
        f"Datos originales:\n{archivo1_datos}\n\n"
    )

    ordenado = merge_sort(archivo1_datos)

    resultado.insert(
        tk.END,
        f"\nResultado Final:\n{ordenado}\n"
    )

    dibujar(ordenado, "red")

    guardar_resultado(ordenado)

# ==========================================
# MEZCLA EQUILIBRADA
# ==========================================

def mezcla_equilibrada():

    resultado.delete(1.0, tk.END)

    if not archivo1_datos:

        messagebox.showerror(
            "Error",
            "Debe cargar el Archivo 1"
        )

        return

    resultado.insert(
        tk.END,
        "=========== MEZCLA EQUILIBRADA ===========\n\n"
    )

    bloques = [[x] for x in archivo1_datos]

    while len(bloques) > 1:

        nuevos = []

        for i in range(0, len(bloques), 2):

            if i + 1 < len(bloques):

                fusion = sorted(
                    bloques[i] + bloques[i + 1]
                )

                resultado.insert(
                    tk.END,
                    f"{bloques[i]} + {bloques[i+1]} -> {fusion}\n"
                )

                nuevos.append(fusion)

                dibujar(fusion, "purple")

            else:

                nuevos.append(bloques[i])

        bloques = nuevos

    resultado.insert(
        tk.END,
        f"\nResultado Final:\n{bloques[0]}\n"
    )

    dibujar(bloques[0], "blue")

    guardar_resultado(bloques[0])

# ==========================================
# EJECUTAR
# ==========================================

def ejecutar():

    opcion = combo.get()

    if opcion == "Intercalación":
        intercalacion_real()

    elif opcion == "Mezcla Directa":
        mezcla_directa()

    elif opcion == "Mezcla Equilibrada":
        mezcla_equilibrada()

# ==========================================
# VENTANA PRINCIPAL
# ==========================================

ventana = tk.Tk()

ventana.title(
    "Métodos de Ordenamiento Externo"
)

ventana.geometry("1200x850")

ventana.configure(
    bg="#202124"
)

# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="Métodos de Ordenamiento Externo",
    font=("Arial", 24, "bold"),
    bg="#202124",
    fg="white"
)

titulo.pack(pady=20)

# ==========================================
# FRAME SUPERIOR
# ==========================================

top = tk.Frame(
    ventana,
    bg="#202124"
)

top.pack(pady=10)

# ==========================================
# ENTRADA ARCHIVO 1
# ==========================================

entrada1 = tk.Entry(
    top,
    width=45,
    font=("Arial", 11)
)

entrada1.grid(
    row=0,
    column=0,
    padx=5
)

# ==========================================
# BOTÓN ARCHIVO 1
# ==========================================

btn1 = tk.Button(
    top,
    text="Cargar Archivo 1",
    command=cargar_archivo1,
    bg="#2196F3",
    fg="white",
    font=("Arial", 11, "bold")
)

btn1.grid(
    row=0,
    column=1,
    padx=5
)

# ==========================================
# ENTRADA ARCHIVO 2
# ==========================================

entrada2 = tk.Entry(
    top,
    width=45,
    font=("Arial", 11)
)

entrada2.grid(
    row=1,
    column=0,
    padx=5,
    pady=10
)

# ==========================================
# BOTÓN ARCHIVO 2
# ==========================================

btn2 = tk.Button(
    top,
    text="Cargar Archivo 2",
    command=cargar_archivo2,
    bg="#FF9800",
    fg="white",
    font=("Arial", 11, "bold")
)

btn2.grid(
    row=1,
    column=1,
    padx=5
)

# ==========================================
# COMBOBOX
# ==========================================

combo = ttk.Combobox(
    ventana,
    values=[
        "Intercalación",
        "Mezcla Directa",
        "Mezcla Equilibrada"
    ],
    state="readonly",
    width=30,
    font=("Arial", 11)
)

combo.pack(pady=10)

combo.current(0)

# ==========================================
# BOTÓN EJECUTAR
# ==========================================

btn_ejecutar = tk.Button(
    ventana,
    text="Ejecutar Método",
    command=ejecutar,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 14, "bold")
)

btn_ejecutar.pack(pady=15)

# ==========================================
# CANVAS
# ==========================================

canvas = tk.Canvas(
    ventana,
    width=950,
    height=300,
    bg="white"
)

canvas.pack(pady=20)

# ==========================================
# FRAME TEXTO
# ==========================================

frame_texto = tk.Frame(
    ventana
)

frame_texto.pack()

# ==========================================
# SCROLLBAR
# ==========================================

scroll = tk.Scrollbar(
    frame_texto
)

scroll.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

# ==========================================
# RESULTADO
# ==========================================

resultado = tk.Text(
    frame_texto,
    width=130,
    height=18,
    font=("Consolas", 11),
    yscrollcommand=scroll.set
)

resultado.pack(
    side=tk.LEFT
)

scroll.config(
    command=resultado.yview
)

# ==========================================
# INICIAR
# ==========================================

ventana.mainloop()
