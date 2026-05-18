import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import random
import os
import json
import pandas as pd

TEMAS = {

    "Midnight": {
        "bg": "#0F172A",
        "bg2": "#1E293B",
        "bg3": "#334155",
        "accent": "#38BDF8",
        "text": "#F8FAFC",
        "bar": "#0EA5E9",
        "bar_active": "#F43F5E",
        "bar_done": "#22C55E"
    },

    "Lavanda": {
        "bg": "#2B1B3F",
        "bg2": "#3D2C5A",
        "bg3": "#5B4B8A",
        "accent": "#C084FC",
        "text": "#F3E8FF",
        "bar": "#8B5CF6",
        "bar_active": "#F472B6",
        "bar_done": "#34D399"
    },

    "Aurora": {
        "bg": "#051923",
        "bg2": "#003554",
        "bg3": "#006494",
        "accent": "#00A6FB",
        "text": "#E0FBFC",
        "bar": "#0582CA",
        "bar_active": "#FFB703",
        "bar_done": "#8ECAE6"
    },

    "RetroWave": {
        "bg": "#1A1A2E",
        "bg2": "#16213E",
        "bg3": "#0F3460",
        "accent": "#E94560",
        "text": "#F1F1F1",
        "bar": "#533483",
        "bar_active": "#FFD369",
        "bar_done": "#00ADB5"
    }
}

FONT_TIT = ("Montserrat", 20, "bold")
FONT_BTN = ("Poppins", 10, "bold")
FONT_SM = ("Poppins", 9)

# ==========================================================
# LÓGICA DE ALGORITMOS
# ==========================================================

def intercalacion_pasos(a, b):
    pasos, resultado = [], []
    i = j = 0
    a_sort, b_sort = sorted(a), sorted(b)

    while i < len(a_sort) and j < len(b_sort):
        pasos.append(("cmp", list(resultado), i, j))

        if a_sort[i] <= b_sort[j]:
            resultado.append(a_sort[i])
            i += 1
        else:
            resultado.append(b_sort[j])
            j += 1

        pasos.append(("add", list(resultado), i, j))

    while i < len(a_sort):
        resultado.append(a_sort[i])
        i += 1
        pasos.append(("add", list(resultado), i, j))

    while j < len(b_sort):
        resultado.append(b_sort[j])
        j += 1
        pasos.append(("add", list(resultado), i, j))

    return resultado, pasos


def mezcla_directa_pasos(lista):

    pasos = []

    def merge_sort(a):
        if len(a) <= 1:
            return a

        m = len(a) // 2

        L = merge_sort(a[:m])
        R = merge_sort(a[m:])

        return merge(L, R)

    def merge(L, R):

        res = []
        i = j = 0

        while i < len(L) and j < len(R):

            if L[i] <= R[j]:
                res.append(L[i])
                i += 1
            else:
                res.append(R[j])
                j += 1

            pasos.append(list(res) + L[i:] + R[j:])

        res += L[i:] + R[j:]
        pasos.append(list(res))

        return res

    resultado = merge_sort(list(lista))

    return resultado, pasos


def mezcla_equilibrada_pasos(lista, k=3):

    pasos = []

    sublistas = [[] for _ in range(k)]

    for idx, el in enumerate(lista):
        sublistas[idx % k].append(el)

    sublistas = [sorted(s) for s in sublistas if s]

    pasos.append(("split", [item for s in sublistas for item in s]))

    def merge2(a, b):

        res = []
        i = j = 0

        while i < len(a) and j < len(b):

            if a[i] <= b[j]:
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1

        return res + a[i:] + b[j:]

    while len(sublistas) > 1:

        nueva = []

        for i in range(0, len(sublistas), 2):

            if i + 1 < len(sublistas):
                nueva.append(merge2(sublistas[i], sublistas[i + 1]))
            else:
                nueva.append(sublistas[i])

        sublistas = nueva

        pasos.append(
            (
                "merge",
                sublistas[0]
                if len(sublistas) == 1
                else [x for s in sublistas for x in s]
            )
        )

    return sublistas[0], pasos


# ==========================================================
# APLICACIÓN PRINCIPAL
# ==========================================================

class OrdenamientoApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Metodo de Ordenamineto Externa")
        self.root.geometry("1200x820")
        self.root.resizable(False, False)

        self.tema_actual = "Midnight"
        self.c = TEMAS[self.tema_actual]

        self.animando = False
        self.datos_actuales = []
        self.metodo_actual = "directa"

        self.widgets_tema = []

        self._build_ui()
        self._aplicar_tema(self.tema_actual)
        self._generar_aleatorios()

    # ======================================================

    def _reg_w(self, widget, t_bg="bg", t_fg="text"):
        self.widgets_tema.append((widget, t_bg, t_fg))
        return widget

    # ======================================================

    def _build_ui(self):

        # HEADER

        self.hdr = self._reg_w(
            tk.Frame(
                self.root,
                pady=15
            )
        )

        self.hdr.pack(fill="x")

        self.lbl_main = self._reg_w(
            tk.Label(
                self.hdr,
                text="◆ Metodo de Ordenamineto Externa ◆",
                font=("Montserrat", 22, "bold"),
                pady=10
            ),
            "bg",
            "accent"
        )

        self.lbl_main.pack()

        # CUERPO

        body = self._reg_w(tk.Frame(self.root))
        body.pack(fill="both", expand=True, padx=18, pady=10)

        # SIDEBAR

        side = self._reg_w(
            tk.Frame(
                body,
                width=300
            ),
            "bg2"
        )

        side.pack(side="left", fill="y", padx=(0, 15))
        side.pack_propagate(False)

        # ==================================================
        # CONFIGURACIÓN
        # ==================================================

        self._reg_w(
            tk.Label(
                side,
                text="⚙ PANEL DE CONTROL",
                font=("Montserrat", 11, "bold")
            )
        ).pack(pady=(15, 8))

        frame_configs = self._reg_w(
            tk.Frame(side),
            "bg2"
        )

        frame_configs.pack(fill="x", padx=15)

        # Tema

        self._reg_w(
            tk.Label(frame_configs, text="Tema:", font=FONT_SM)
        ).grid(row=0, column=0, sticky="w")

        self.combo_tema = ttk.Combobox(
            frame_configs,
            values=list(TEMAS.keys()),
            state="readonly",
            width=16
        )

        self.combo_tema.set(self.tema_actual)

        self.combo_tema.bind(
            "<<ComboboxSelected>>",
            lambda e: self._aplicar_tema(self.combo_tema.get())
        )

        self.combo_tema.grid(row=0, column=1, pady=4)

        # K

        self._reg_w(
            tk.Label(frame_configs, text="Vías:", font=FONT_SM)
        ).grid(row=1, column=0, sticky="w")

        self.spin_k = tk.Spinbox(
            frame_configs,
            from_=2,
            to=10,
            width=6
        )

        self.spin_k.delete(0, "end")
        self.spin_k.insert(0, "3")

        self.spin_k.grid(row=1, column=1, sticky="w", pady=4)

        # Tipo de dato

        self._reg_w(
            tk.Label(frame_configs, text="Extraer:", font=FONT_SM)
        ).grid(row=2, column=0, sticky="w")

        self.combo_tipo_dato = ttk.Combobox(
            frame_configs,
            values=["Automático", "Solo Números", "Solo Texto"],
            state="readonly",
            width=16
        )

        self.combo_tipo_dato.set("Automático")
        self.combo_tipo_dato.grid(row=2, column=1, pady=4)

        # ==================================================
        # MÉTODOS
        # ==================================================

        self._reg_w(
            tk.Label(
                side,
                text="🧠 ALGORITMOS",
                font=("Montserrat", 11, "bold")
            )
        ).pack(pady=(20, 8))

        self.btn_metodos = {}

        for label, key in [

            ("Intercalación", "intercalacion"),
            ("Mezcla Directa", "directa"),
            ("Mezcla Equilibrada", "equilibrada")

        ]:

            btn = tk.Button(
                side,
                text=label,
                font=FONT_BTN,
                bd=0,
                pady=10,
                cursor="hand2",
                relief="flat",
                command=lambda k=key: self._sel_metodo(k)
            )

            btn.pack(fill="x", padx=15, pady=4)

            self.widgets_tema.append((btn, "bg3", "text"))

            self.btn_metodos[key] = btn

        # ==================================================
        # DATOS
        # ==================================================

        self._reg_w(
            tk.Label(
                side,
                text="📂 DATOS",
                font=("Montserrat", 11, "bold")
            )
        ).pack(pady=(20, 8))

        botones = [

            ("🎲 Generar Aleatorios", self._generar_aleatorios),
            ("📂 Cargar Archivo", self._cargar_archivo),
            ("💾 Guardar Resultados", self._guardar_archivo)

        ]

        for texto, comando in botones:

            btn = tk.Button(
                side,
                text=texto,
                font=FONT_BTN,
                bd=0,
                pady=10,
                cursor="hand2",
                relief="flat",
                command=comando
            )

            btn.pack(fill="x", padx=15, pady=4)

            self.widgets_tema.append((btn, "bg3", "text"))

        # ==================================================
        # VELOCIDAD
        # ==================================================

        self._reg_w(
            tk.Label(
                side,
                text="⚡ VELOCIDAD",
                font=("Montserrat", 11, "bold")
            )
        ).pack(pady=(20, 8))

        self.vel_slider = tk.Scale(
            side,
            from_=0.01,
            to=1.0,
            resolution=0.05,
            orient="horizontal",
            bd=0,
            highlightthickness=0
        )

        self.vel_slider.set(0.2)

        self.vel_slider.pack(fill="x", padx=15)

        self.widgets_tema.append((self.vel_slider, "bg2", "text"))

        # BOTÓN EJECUTAR

        self.btn_run = tk.Button(
            side,
            text="🚀 EJECUTAR PROCESO",
            font=("Poppins", 11, "bold"),
            bd=0,
            pady=14,
            cursor="hand2",
            relief="flat",
            command=self._ejecutar
        )

        self.btn_run.pack(fill="x", padx=15, pady=25)

        self.widgets_tema.append((self.btn_run, "accent", "bg"))

        # ==================================================
        # ÁREA PRINCIPAL
        # ==================================================

        main = self._reg_w(tk.Frame(body))
        main.pack(side="left", fill="both", expand=True)

        self.lbl_titulo = self._reg_w(
            tk.Label(
                main,
                text="Sistema listo para procesar datos...",
                font=("Poppins", 12, "bold"),
                anchor="w",
                pady=10
            ),
            "bg",
            "accent"
        )

        self.lbl_titulo.pack(fill="x")

        # CANVAS

        self.canvas = tk.Canvas(
            main,
            height=350,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(fill="x", pady=8)

        # LOG

        self.log = tk.Text(
            main,
            font=("JetBrains Mono", 10),
            bd=0,
            padx=14,
            pady=14,
            insertbackground="white"
        )

        self.log.pack(fill="both", expand=True)

        self.widgets_tema.append((self.log, "bg2", "text"))

    # ======================================================

    def _aplicar_tema(self, nombre_tema):

        self.tema_actual = nombre_tema
        self.c = TEMAS[nombre_tema]

        self.root.configure(bg=self.c["bg"])
        self.canvas.configure(bg=self.c["bg2"])

        for widget, t_bg, t_fg in self.widgets_tema:

            try:

                widget.configure(
                    bg=self.c[t_bg],
                    fg=self.c[t_fg]
                )

                if isinstance(widget, tk.Button):

                    widget.configure(
                        activebackground=self.c["accent"],
                        activeforeground=self.c["bg"],
                        relief="flat"
                    )

                if isinstance(widget, tk.Scale):

                    widget.configure(
                        troughcolor=self.c["bg3"]
                    )

            except:
                pass

        self._sel_metodo(self.metodo_actual)
        self._dibujar(self.datos_actuales)

    # ======================================================

    def _sel_metodo(self, metodo):

        self.metodo_actual = metodo

        for k, b in self.btn_metodos.items():

            b.configure(

                bg=self.c["accent"] if k == metodo else self.c["bg3"],

                fg=self.c["bg"] if k == metodo else self.c["text"]

            )

        tipo = type(self.datos_actuales[0]).__name__ if self.datos_actuales else "Desconocido"

        self.lbl_titulo.config(
            text=f"ALGORITMO: {self.metodo_actual.upper()}   |   Tipo: {tipo}   |   Elementos: {len(self.datos_actuales)}"
        )

    # ======================================================

    def _generar_aleatorios(self):

        preferencia = self.combo_tipo_dato.get()

        if preferencia == "Solo Números":
            opcion = "numeros"

        elif preferencia == "Solo Texto":
            opcion = "texto"

        else:
            opcion = random.choice(["numeros", "texto"])

        if opcion == "numeros":

            self.datos_actuales = [
                random.randint(1, 100)
                for _ in range(20)
            ]

        else:

            palabras = [
                "Python", "Java", "C++", "Ruby",
                "Rust", "Go", "Perl", "Lua",
                "Swift", "PHP", "Dart",
                "Kotlin", "Scala", "R"
            ]

            self.datos_actuales = [
                random.choice(palabras)
                for _ in range(15)
            ]

        self._log_msg(f"Datos aleatorios generados ({opcion}).")

        self._sel_metodo(self.metodo_actual)

        self._dibujar(self.datos_actuales)

    # ======================================================

    def _procesar_y_filtrar_datos(self, raw_data):

        numeros = []
        textos = []

        for item in raw_data:

            if pd.isna(item) or item == "":
                continue

            try:

                numeros.append(
                    float(item)
                    if '.' in str(item)
                    else int(item)
                )

            except ValueError:

                textos.append(str(item).strip())

        preferencia = self.combo_tipo_dato.get()

        if preferencia == "Solo Números":

            if not numeros:
                raise ValueError("No se encontraron números.")

            return numeros

        elif preferencia == "Solo Texto":

            if not textos:
                raise ValueError("No se encontraron textos.")

            return textos

        else:

            if len(numeros) >= len(textos) and numeros:
                return numeros

            elif textos:
                return textos

            return []

    # ======================================================

    def _cargar_archivo(self):

        ruta = filedialog.askopenfilename(
            filetypes=[
                ("Todos soportados", "*.txt *.xlsx *.xls *.json")
            ]
        )

        if not ruta:
            return

        try:

            raw = []

            ext = os.path.splitext(ruta)[1].lower()

            if ext in ['.xlsx', '.xls']:

                df = pd.read_excel(ruta, header=None)

                raw = df.values.flatten().tolist()

            elif ext == '.json':

                with open(ruta, 'r', encoding='utf-8') as f:

                    data = json.load(f)

                    raw = data if isinstance(data, list) else list(data.values())

            elif ext == '.txt':

                with open(ruta, 'r', encoding='utf-8') as f:

                    for line in f:
                        raw.extend(line.replace(',', ' ').split())

            datos_limpios = self._procesar_y_filtrar_datos(raw)

            if not datos_limpios:
                raise ValueError("Archivo vacío.")

            self.datos_actuales = datos_limpios

            self._sel_metodo(self.metodo_actual)

            self._dibujar(self.datos_actuales)

            messagebox.showinfo(
                "Éxito",
                f"Datos cargados desde {os.path.basename(ruta)}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Error al procesar archivo:\n{e}"
            )

    # ======================================================

    def _guardar_archivo(self):

        if not self.datos_actuales:

            messagebox.showwarning(
                "Atención",
                "No hay datos para guardar."
            )

            return

        ruta = filedialog.asksaveasfilename(

            defaultextension=".txt",

            filetypes=[
                ("JSON", "*.json"),
                ("Excel", "*.xlsx"),
                ("Texto", "*.txt")
            ]
        )

        if not ruta:
            return

        try:

            ext = os.path.splitext(ruta)[1].lower()

            if ext == '.json':

                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(self.datos_actuales, f)

            elif ext == '.xlsx':

                pd.DataFrame(self.datos_actuales).to_excel(
                    ruta,
                    index=False,
                    header=False
                )

            else:

                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(", ".join(map(str, self.datos_actuales)))

            self._log_msg(f"Archivo guardado en: {ruta}")

            messagebox.showinfo(
                "Guardado",
                "Resultados exportados con éxito."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Error al guardar:\n{e}"
            )

    # ======================================================

    def _dibujar(self, valores, activos=[], listos=[]):

        self.canvas.delete("all")

        if not valores:
            return

        W = int(self.canvas.winfo_width() or 800)
        H = int(self.canvas.winfo_height() or 350)

        n = len(valores)

        ancho = min((W - 40) / n, 80)

        valores_unicos = sorted(list(set(valores)))

        for i, v in enumerate(valores):

            rank = valores_unicos.index(v) + 1

            h = (
                (rank / len(valores_unicos)) * (H - 60)
                if valores_unicos
                else 100
            )

            x1 = 20 + i * ancho
            y1 = H - 30 - h

            x2 = x1 + ancho - 4
            y2 = H - 30

            color = (

                self.c["bar_done"]

                if i in listos

                else (

                    self.c["bar_active"]

                    if i in activos

                    else self.c["bar"]

                )
            )

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=""
            )

            text_disp = str(v)

            if len(text_disp) > 8:
                text_disp = text_disp[:6] + ".."

            self.canvas.create_text(
                x1 + ancho / 2,
                y1 - 15,
                text=text_disp,
                fill=self.c["text"],
                font=("Poppins", 8, "bold"),
                angle=0 if type(v) != str else 45
            )

    # ======================================================

    def _log_msg(self, msg):

        self.log.insert(
            tk.END,
            f"[{time.strftime('%H:%M:%S')}] {msg}\n"
        )

        self.log.see(tk.END)

    # ======================================================

    def _ejecutar(self):

        if self.animando or not self.datos_actuales:
            return

        self.animando = True

        delay = self.vel_slider.get()

        m = self.metodo_actual

        self.log.delete("1.0", tk.END)

        try:

            if m == "intercalacion":

                mitad = len(self.datos_actuales) // 2

                a = self.datos_actuales[:mitad]
                b = self.datos_actuales[mitad:]

                self._log_msg(
                    f"Intercalando listas ({len(a)} y {len(b)})..."
                )

                res, pasos = intercalacion_pasos(a, b)

                for p in pasos:

                    self._dibujar(
                        a + b,
                        activos=[p[2], len(a) + p[3]]
                    )

                    self.root.update()

                    time.sleep(delay)

                self.datos_actuales = res

            elif m == "directa":

                self._log_msg("Ejecutando Mezcla Directa...")

                res, pasos = mezcla_directa_pasos(self.datos_actuales)

                for p in pasos:

                    self._dibujar(p)

                    self.root.update()

                    time.sleep(delay)

                self.datos_actuales = res

            elif m == "equilibrada":

                k_val = int(self.spin_k.get())

                self._log_msg(
                    f"Ejecutando Mezcla Equilibrada (K={k_val})..."
                )

                res, pasos = mezcla_equilibrada_pasos(
                    self.datos_actuales,
                    k=k_val
                )

                for p in pasos:

                    self._dibujar(p[1])

                    self.root.update()

                    time.sleep(delay)

                self.datos_actuales = res

            self._dibujar(
                self.datos_actuales,
                listos=list(range(len(self.datos_actuales)))
            )

            self._log_msg("✅ Ordenamiento finalizado.")

        except Exception as e:

            self._log_msg(f"❌ Error: {e}")

        finally:

            self.animando = False


# ==========================================================
# INICIO
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = OrdenamientoApp(root)

    root.mainloop()
