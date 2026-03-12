import tkinter as tk

class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def esta_vacia(self):
        return len(self.items) == 0

    def mostrar(self):
        return self.items

class SistemaColas:

    def __init__(self, root):
        self.root = root
        self.root.title("Colas de Servicio - Seguros")

        self.colas = {
            1: Cola(),
            2: Cola(),
            3: Cola()
        }

        self.contadores = {
            1: 0,
            2: 0,
            3: 0
        }

        tk.Label(root, text="Ingrese comando (C1, A1, C2, A2...)", font=("Arial",12)).pack(pady=10)

        self.entrada = tk.Entry(root, font=("Arial",12))
        self.entrada.pack()

        tk.Button(root, text="Ejecutar", command=self.procesar).pack(pady=5)

        self.resultado = tk.Label(root, text="", font=("Arial",12), fg="blue")
        self.resultado.pack(pady=10)

        self.canvas = tk.Canvas(root, width=650, height=300, bg="white")
        self.canvas.pack()

        self.dibujar_colas()

    def procesar(self):

        comando = self.entrada.get().upper()

        if len(comando) < 2:
            return

        accion = comando[0]
        servicio = int(comando[1])

        if servicio not in self.colas:
            self.resultado.config(text="Servicio no válido")
            return

        if accion == "C":

            self.contadores[servicio] += 1
            turno = f"S{servicio}-{self.contadores[servicio]}"

            self.colas[servicio].encolar(turno)

            self.resultado.config(text=f"Turno asignado: {turno}")
            print("Turno asignado:", turno)

        elif accion == "A":

            cliente = self.colas[servicio].desencolar()

            if cliente:
                self.resultado.config(text=f"Atendiendo: {cliente}")
                print("Atendiendo:", cliente)
            else:
                self.resultado.config(text="No hay clientes en esa cola")

        self.entrada.delete(0, tk.END)
        self.dibujar_colas()

    def dibujar_colas(self):

        self.canvas.delete("all")

        posiciones = [150, 350, 550]

        for i, servicio in enumerate(self.colas):

            x = posiciones[i]

            self.canvas.create_text(x, 30, text=f"Servicio {servicio}", font=("Arial",12,"bold"))

            cola = self.colas[servicio].mostrar()

            for j, cliente in enumerate(cola):

                y = 80 + j*40

                self.canvas.create_rectangle(x-40, y-15, x+40, y+15, fill="#87CEFA")
                self.canvas.create_text(x, y, text=cliente)

root = tk.Tk()
app = SistemaColas(root)
root.mainloop()
