import tkinter as tk
from tkinter import messagebox
import random

ANCHO = 800
ALTO = 400
VELOCIDAD = 200


# =========================
# SHELL SORT
# =========================
def shell_sort(arr, draw):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                draw(arr, [j])
                yield

            arr[j] = temp
        gap //= 2


# =========================
# QUICK SORT
# =========================
def quick_sort(arr, low, high, draw):
    if low < high:
        pi = yield from partition(arr, low, high, draw)
        yield from quick_sort(arr, low, pi - 1, draw)
        yield from quick_sort(arr, pi + 1, high, draw)


def partition(arr, low, high, draw):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw(arr, [i, j])
            yield

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw(arr, [i + 1])
    yield

    return i + 1


# =========================
# HEAP SORT
# =========================
def heapify(arr, n, i, draw):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        draw(arr, [i, largest])
        yield
        yield from heapify(arr, n, largest, draw)


def heap_sort(arr, draw):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i, draw)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        draw(arr, [i, 0])
        yield
        yield from heapify(arr, i, 0, draw)


# =========================
# RADIX SORT (CLÁSICO)
# =========================
def counting_sort(arr, exp, draw):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # contar dígitos
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        draw(arr, [i])
        yield

    # acumulado
    for i in range(1, 10):
        count[i] += count[i - 1]
        yield

    # construir salida (estable)
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

        draw(arr, [i])
        yield
        i -= 1

    # copiar al arreglo original
    for i in range(n):
        arr[i] = output[i]
        draw(arr, [i])
        yield


def radix_sort(arr, draw):
    if len(arr) == 0:
        return

    if any(x < 0 for x in arr):
        raise ValueError("Radix no acepta negativos")

    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        yield from counting_sort(arr, exp, draw)
        exp *= 10


# =========================
# INTERFAZ
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenamientos Visuales")
        self.root.geometry("900x650")

        self.data = []

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="white")
        self.canvas.pack(pady=20)

        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Cantidad:").grid(row=0, column=0)
        self.entry_cant = tk.Entry(frame, width=5)
        self.entry_cant.grid(row=0, column=1)

        tk.Label(frame, text="Números (separados por coma):").grid(row=0, column=2)
        self.entry_nums = tk.Entry(frame, width=40)
        self.entry_nums.grid(row=0, column=3)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Shell", command=lambda: self.iniciar("shell")).grid(row=0, column=0)
        tk.Button(btn_frame, text="Quick", command=lambda: self.iniciar("quick")).grid(row=0, column=1)
        tk.Button(btn_frame, text="Heap", command=lambda: self.iniciar("heap")).grid(row=0, column=2)
        tk.Button(btn_frame, text="Radix", command=lambda: self.iniciar("radix")).grid(row=0, column=3)

        tk.Button(root, text="Generar Aleatorios", command=self.generar).pack()
        tk.Button(root, text="Salir", command=root.quit).pack(pady=10)

    # =========================
    # DIBUJAR
    # =========================
    def draw(self, arr, highlight):
        self.canvas.delete("all")

        if not arr:
            return

        ancho = ANCHO / len(arr)
        max_val = max(arr)

        for i, val in enumerate(arr):
            x0 = i * ancho
            y0 = ALTO - (val / max_val) * (ALTO - 20)
            x1 = (i + 1) * ancho
            y1 = ALTO

            color = "red" if i in highlight else "skyblue"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + ancho / 2, y0 - 10, text=str(val))

        self.root.update_idletasks()

    # =========================
    # OBTENER DATOS
    # =========================
    def obtener_datos(self):
        try:
            cant = int(self.entry_cant.get())
            nums = list(map(int, self.entry_nums.get().split(",")))

            if len(nums) != cant:
                messagebox.showerror("Error", "Cantidad no coincide")
                return None

            return nums
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return None

    # =========================
    # INICIAR
    # =========================
    def iniciar(self, tipo):
        self.data = self.obtener_datos()
        if not self.data:
            return

        self.draw(self.data, [])

        if tipo == "shell":
            gen = shell_sort(self.data, self.draw)
        elif tipo == "quick":
            gen = quick_sort(self.data, 0, len(self.data) - 1, self.draw)
        elif tipo == "heap":
            gen = heap_sort(self.data, self.draw)
        elif tipo == "radix":
            try:
                gen = radix_sort(self.data, self.draw)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return

        self.animar(gen)

    # =========================
    # ANIMACIÓN
    # =========================
    def animar(self, gen):
        try:
            next(gen)
            self.root.after(VELOCIDAD, lambda: self.animar(gen))
        except StopIteration:
            self.draw(self.data, [])

    # =========================
    # GENERAR ALEATORIOS
    # =========================
    def generar(self):
        cant = random.randint(5, 15)
        nums = [random.randint(1, 100) for _ in range(cant)]

        self.entry_cant.delete(0, tk.END)
        self.entry_cant.insert(0, str(cant))

        self.entry_nums.delete(0, tk.END)
        self.entry_nums.insert(0, ",".join(map(str, nums)))

        self.draw(nums, [])


# =========================
# MAIN
# =========================
root = tk.Tk()
app = App(root)
root.mainloop()
