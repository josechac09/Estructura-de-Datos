# ==========================================================
# UI.PY
# ==========================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import random

from inter import *
from exter import *

# ==========================================================
# TEMAS
# ==========================================================

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
    }
}

FONT_BTN = ("Poppins", 10, "bold")
FONT_TIT = ("Montserrat", 22, "bold")
FONT_SM = ("Poppins", 9)

# ==========================================================
# APP
# ==========================================================

class OrdenamientoUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Sistema de Ordenamientos")
        self.root.geometry("1450x860")
        self.root.minsize(1250, 780)

        self.tema_actual = "Midnight"
        self.c = TEMAS[self.tema_actual]

        self.animando = False
        self.datos_actuales = []

        self.archivo_inter_1 = []
        self.archivo_inter_2 = []

        self.tipo_actual = "interno"

        self.metodo_actual = "burbuja"

        self.widgets_tema = []

        self.metodos_internos = [

            ("Burbuja", "burbuja"),
            ("Inserción", "insercion"),
            ("Selección", "seleccion"),
            ("Shell", "shell"),
            ("Quick", "quick"),
            ("Heap", "heap"),
            ("Radix", "radix")
        ]

        self.metodos_externos = [

            ("Intercalación", "intercalacion"),
            ("Mezcla Directa", "directa"),
            ("Mezcla Equilibrada", "equilibrada")
        ]

        self._build_ui()

        self._aplicar_tema(self.tema_actual)

        self._mostrar_metodos()

        self._generar_aleatorios()

    # ======================================================

    def _reg_w(self, widget, t_bg="bg", t_fg="text"):

        self.widgets_tema.append((widget, t_bg, t_fg))

        return widget

    # ======================================================

    def _scroll_mouse(self, event):

        self.sidebar_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ======================================================

    def _build_ui(self):

        # ==================================================
        # HEADER
        # ==================================================

        self.header = self._reg_w(
            tk.Frame(
                self.root,
                height=90
            )
        )

        self.header.pack(fill="x")

        self.lbl_main = self._reg_w(

            tk.Label(

                self.header,

                text="◆ SISTEMA DE ORDENAMIENTOS ◆",

                font=FONT_TIT,

                pady=18
            ),

            "bg",
            "accent"
        )

        self.lbl_main.pack()

        # ==================================================
        # BODY
        # ==================================================

        self.body = self._reg_w(
            tk.Frame(self.root)
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # ==================================================
        # SIDEBAR
        # ==================================================

        sidebar_container = tk.Frame(
            self.body,
            width=340
        )

        sidebar_container.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        sidebar_container.pack_propagate(False)

        # ==================================================
        # CANVAS SCROLL
        # ==================================================

        self.sidebar_canvas = tk.Canvas(
            sidebar_container,
            highlightthickness=0,
            bd=0
        )

        scrollbar = ttk.Scrollbar(
            sidebar_container,
            orient="vertical",
            command=self.sidebar_canvas.yview
        )

        self.sidebar_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")

        self.sidebar_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # FRAME INTERNO
        # ==================================================

        self.sidebar = self._reg_w(
            tk.Frame(
                self.sidebar_canvas,
                width=320
            ),
            "bg2"
        )

        self.sidebar_window = self.sidebar_canvas.create_window(
            (0, 0),
            window=self.sidebar,
            anchor="nw"
        )

        self.sidebar.bind(
            "<Configure>",
            lambda e: self.sidebar_canvas.configure(
                scrollregion=self.sidebar_canvas.bbox("all")
            )
        )

        self.sidebar_canvas.bind(
            "<Configure>",
            self._resize_sidebar
        )

        # ==================================================
        # SCROLL MOUSE
        # ==================================================

        self.sidebar_canvas.bind_all(
            "<MouseWheel>",
            self._scroll_mouse
        )

        # ==================================================
        # PANEL
        # ==================================================

        self._reg_w(

            tk.Label(

                self.sidebar,

                text="⚙ PANEL DE CONTROL",

                font=("Montserrat", 12, "bold")
            )

        ).pack(pady=(18, 10))

        # ==================================================
        # CONFIG
        # ==================================================

        config = self._reg_w(
            tk.Frame(self.sidebar),
            "bg2"
        )

        config.pack(fill="x", padx=15)

        # Tema

        self._reg_w(
            tk.Label(config, text="Tema:", font=FONT_SM)
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.combo_tema = ttk.Combobox(

            config,

            values=list(TEMAS.keys()),

            state="readonly",

            width=18
        )

        self.combo_tema.set(self.tema_actual)

        self.combo_tema.grid(row=0, column=1)

        self.combo_tema.bind(

            "<<ComboboxSelected>>",

            lambda e: self._aplicar_tema(
                self.combo_tema.get()
            )
        )

        # ==================================================
        # K
        # ==================================================

        self._reg_w(
            tk.Label(config, text="K:", font=FONT_SM)
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.spin_k = tk.Spinbox(

            config,

            from_=2,

            to=10,

            width=10
        )

        self.spin_k.grid(row=1, column=1, sticky="w")

        self.spin_k.delete(0, "end")
        self.spin_k.insert(0, "3")

        # ==================================================
        # TIPO
        # ==================================================

        self._reg_w(

            tk.Label(

                self.sidebar,

                text="📚 TIPO DE ORDENAMIENTO",

                font=("Montserrat", 11, "bold")
            )

        ).pack(pady=(20, 8))

        frame_tipo = self._reg_w(
            tk.Frame(self.sidebar),
            "bg2"
        )

        frame_tipo.pack(fill="x", padx=15)

        self.btn_interno = tk.Button(

            frame_tipo,

            text="Internos",

            font=FONT_BTN,

            bd=0,

            pady=10,

            cursor="hand2",

            command=lambda: self._cambiar_tipo("interno")
        )

        self.btn_interno.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.btn_externo = tk.Button(

            frame_tipo,

            text="Externos",

            font=FONT_BTN,

            bd=0,

            pady=10,

            cursor="hand2",

            command=lambda: self._cambiar_tipo("externo")
        )

        self.btn_externo.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.widgets_tema.append((self.btn_interno, "bg3", "text"))
        self.widgets_tema.append((self.btn_externo, "bg3", "text"))

        # ==================================================
        # MÉTODOS
        # ==================================================

        self._reg_w(

            tk.Label(

                self.sidebar,

                text="🧠 ALGORITMOS",

                font=("Montserrat", 11, "bold")
            )

        ).pack(pady=(20, 8))

        self.frame_metodos = self._reg_w(
            tk.Frame(self.sidebar),
            "bg2"
        )

        self.frame_metodos.pack(
            fill="x",
            padx=15
        )

        self.btn_metodos = {}

        # ==================================================
        # BOTONES EXTRA
        # ==================================================

        botones = [

            ("🎲 Generar Datos", self._generar_aleatorios),
            ("📂 Cargar Archivo", self._cargar_archivo),
            ("💾 Guardar", self._guardar_archivo)
        ]

        for texto, comando in botones:

            btn = tk.Button(

                self.sidebar,

                text=texto,

                font=FONT_BTN,

                bd=0,

                pady=10,

                cursor="hand2",

                command=comando
            )

            btn.pack(fill="x", padx=15, pady=4)

            self.widgets_tema.append((btn, "bg3", "text"))

        # ==================================================
        # VELOCIDAD
        # ==================================================

        self._reg_w(

            tk.Label(

                self.sidebar,

                text="⚡ VELOCIDAD",

                font=("Montserrat", 11, "bold")
            )

        ).pack(pady=(18, 8))

        self.vel_slider = tk.Scale(

            self.sidebar,

            from_=0.01,

            to=1.0,

            resolution=0.05,

            orient="horizontal",

            bd=0,

            highlightthickness=0
        )

        self.vel_slider.set(0.2)

        self.vel_slider.pack(
            fill="x",
            padx=15
        )

        self.widgets_tema.append((self.vel_slider, "bg2", "text"))

        # ==================================================
        # EJECUTAR
        # ==================================================

        self.btn_run = tk.Button(

            self.sidebar,

            text="🚀 EJECUTAR",

            font=("Poppins", 11, "bold"),

            bd=0,

            pady=14,

            cursor="hand2",

            command=self._ejecutar
        )

        self.btn_run.pack(
            fill="x",
            padx=15,
            pady=20
        )

        self.widgets_tema.append((self.btn_run, "accent", "bg"))

        # ==================================================
        # MAIN
        # ==================================================

        self.main = self._reg_w(
            tk.Frame(self.body)
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # TITULO
        # ==================================================

        self.lbl_titulo = self._reg_w(

            tk.Label(

                self.main,

                text="Sistema listo...",

                font=("Poppins", 14, "bold"),

                anchor="w",

                pady=10
            ),

            "bg",
            "accent"
        )

        self.lbl_titulo.pack(fill="x")

        # ==================================================
        # CANVAS
        # ==================================================

        canvas_frame = self._reg_w(
            tk.Frame(self.main),
            "bg2"
        )

        canvas_frame.pack(
            fill="both",
            expand=True,
            pady=(5, 10)
        )

        self.canvas = tk.Canvas(

            canvas_frame,

            bg="#1E293B",

            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ==================================================
        # LOG
        # ==================================================

        self.log = tk.Text(

            self.main,

            height=10,

            font=("Consolas", 10),

            bd=0,

            padx=14,

            pady=14
        )

        self.log.pack(
            fill="x",
            pady=(5, 0)
        )

        self.widgets_tema.append((self.log, "bg2", "text"))

    # ======================================================

    def _resize_sidebar(self, event):

        self.sidebar_canvas.itemconfig(
            self.sidebar_window,
            width=event.width
        )

    # ======================================================

    def _mostrar_metodos(self):

        for widget in self.frame_metodos.winfo_children():
            widget.destroy()

        self.btn_metodos.clear()

        metodos = (

            self.metodos_internos

            if self.tipo_actual == "interno"

            else self.metodos_externos
        )

        for label, key in metodos:

            btn = tk.Button(

                self.frame_metodos,

                text=label,

                font=FONT_BTN,

                bd=0,

                pady=12,

                cursor="hand2",

                relief="flat",

                command=lambda k=key: self._sel_metodo(k)
            )

            btn.pack(
                fill="x",
                pady=4
            )

            self.widgets_tema.append((btn, "bg3", "text"))

            self.btn_metodos[key] = btn

        primer = metodos[0][1]

        self._sel_metodo(primer)

    # ======================================================

    def _cambiar_tipo(self, tipo):

        self.tipo_actual = tipo

        self.btn_interno.configure(

            bg=self.c["accent"]

            if tipo == "interno"

            else self.c["bg3"],

            fg=self.c["bg"]
            if tipo == "interno"
            else self.c["text"]
        )

        self.btn_externo.configure(

            bg=self.c["accent"]

            if tipo == "externo"

            else self.c["bg3"],

            fg=self.c["bg"]
            if tipo == "externo"
            else self.c["text"]
        )

        self._mostrar_metodos()

    # ======================================================

    def _aplicar_tema(self, tema):

        self.tema_actual = tema

        self.c = TEMAS[tema]

        self.root.configure(bg=self.c["bg"])

        self.canvas.configure(bg=self.c["bg2"])

        self.sidebar_canvas.configure(bg=self.c["bg2"])

        for widget, t_bg, t_fg in self.widgets_tema:

            try:

                widget.configure(
                    bg=self.c[t_bg],
                    fg=self.c[t_fg]
                )

            except:
                pass

        self._cambiar_tipo(self.tipo_actual)

        self._dibujar(self.datos_actuales)

    # ======================================================

    def _sel_metodo(self, metodo):

        self.metodo_actual = metodo

        for k, b in self.btn_metodos.items():

            b.configure(

                bg=self.c["accent"]
                if k == metodo
                else self.c["bg3"],

                fg=self.c["bg"]
                if k == metodo
                else self.c["text"]
            )

        self.lbl_titulo.config(
            text=f"ALGORITMO ACTUAL: {metodo.upper()}"
        )

    # ======================================================

    def _generar_aleatorios(self):

        self.datos_actuales = [

            random.randint(10, 100)

            for _ in range(25)
        ]

        self._dibujar(self.datos_actuales)

        self._log_msg("Datos aleatorios generados.")

    # ======================================================

    def _dibujar(self, valores, activos=[], listos=[]):

        self.canvas.delete("all")

        if not valores:
            return

        self.canvas.update()

        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()

        n = len(valores)

        ancho = max((W - 40) / n, 10)

        max_val = max(valores)

        for i, v in enumerate(valores):

            altura = (v / max_val) * (H - 80)

            x1 = 20 + i * ancho
            y1 = H - altura - 40

            x2 = x1 + ancho - 6
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

            self.canvas.create_text(

                (x1 + x2) / 2,

                y1 - 12,

                text=str(v),

                fill=self.c["text"],

                font=("Poppins", 8, "bold")
            )

    # ======================================================

    def _log_msg(self, msg):

        self.log.insert(

            tk.END,

            f"[{time.strftime('%H:%M:%S')}] {msg}\n"
        )

        self.log.see(tk.END)

    # ======================================================

    def _cargar_archivo(self):

        # ==================================================
        # INTERCALACION
        # ==================================================

        if self.metodo_actual == "intercalacion":

            ruta1 = filedialog.askopenfilename(
                title="Selecciona el PRIMER archivo",
                filetypes=[("Texto", "*.txt")]
            )

            if not ruta1:
                return

            ruta2 = filedialog.askopenfilename(
                title="Selecciona el SEGUNDO archivo",
                filetypes=[("Texto", "*.txt")]
            )

            if not ruta2:
                return

            try:

                with open(ruta1, "r") as f1:
                    contenido1 = f1.read()

                with open(ruta2, "r") as f2:
                    contenido2 = f2.read()

                self.archivo_inter_1 = list(
                    map(int, contenido1.split(","))
                )

                self.archivo_inter_2 = list(
                    map(int, contenido2.split(","))
                )

                self.datos_actuales = (
                    self.archivo_inter_1 +
                    self.archivo_inter_2
                )

                self._dibujar(self.datos_actuales)

                self._log_msg(
                    "2 archivos cargados para Intercalación."
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Uno de los archivos es inválido."
                )

            return

        # ==================================================
        # NORMAL
        # ==================================================

        ruta = filedialog.askopenfilename(

            filetypes=[
                ("Texto", "*.txt")
            ]
        )

        if not ruta:
            return

        try:

            with open(ruta, "r") as f:

                contenido = f.read()

            self.datos_actuales = list(
                map(int, contenido.split(","))
            )

            self._dibujar(self.datos_actuales)

            self._log_msg("Archivo cargado.")

        except:

            messagebox.showerror(
                "Error",
                "Archivo inválido."
            )

    # ======================================================

    def _guardar_archivo(self):

        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt"
        )

        if not ruta:
            return

        with open(ruta, "w") as f:

            f.write(
                ",".join(
                    map(str, self.datos_actuales)
                )
            )

        messagebox.showinfo(
            "Guardado",
            "Archivo guardado correctamente."
        )

    # ======================================================

    def _ejecutar(self):

        if self.animando:
            return

        self.animando = True

        delay = self.vel_slider.get()

        m = self.metodo_actual

        try:

            if m == "burbuja":
                res, pasos = burbuja_pasos(self.datos_actuales)

            elif m == "insercion":
                res, pasos = insercion_pasos(self.datos_actuales)

            elif m == "seleccion":
                res, pasos = seleccion_pasos(self.datos_actuales)

            elif m == "shell":
                res, pasos = shell_pasos(self.datos_actuales)

            elif m == "quick":
                res, pasos = quick_pasos(self.datos_actuales)

            elif m == "heap":
                res, pasos = heap_pasos(self.datos_actuales)

            elif m == "radix":
                res, pasos = radix_pasos(self.datos_actuales)

            elif m == "intercalacion":

                if not self.archivo_inter_1 or not self.archivo_inter_2:

                    messagebox.showwarning(
                        "Archivos faltantes",
                        "Debes cargar 2 archivos para Intercalación."
                    )

                    self.animando = False
                    return

                res, pasos = intercalacion_pasos(
                    self.archivo_inter_1,
                    self.archivo_inter_2
                )

            elif m == "directa":

                res, pasos = mezcla_directa_pasos(
                    self.datos_actuales
                )

            elif m == "equilibrada":

                k = int(self.spin_k.get())

                res, pasos = mezcla_equilibrada_pasos(
                    self.datos_actuales,
                    k
                )

            for estado, activos in pasos:

                self._dibujar(estado, activos)

                self.root.update()

                time.sleep(delay)

            self.datos_actuales = res

            self._dibujar(

                self.datos_actuales,

                listos=list(
                    range(len(self.datos_actuales))
                )
            )

            self._log_msg(
                "Ordenamiento finalizado."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            self.animando = False
