import tkinter as tk

ANCHO = 600
ALTO = 350

class Pila:                                                                                                                                     
    def __init__(self):
        self.items = []

    def push(self, x):                                                                                                                            
        self.items.append(x)

    def pop(self):                                                                                                                              
        return self.items.pop()

    def peek(self):                                                                                                                           
        return self.items[-1]

    def size(self):                                                                                                                            
        return len(self.items)


class HanoiGUI:                                                                                                                                 

    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi - Pila")

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#f0f0f0")
        self.canvas.pack()

        self.boton = tk.Button(root, text="Iniciar", command=self.animar)
        self.boton.pack(pady=10)

        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=5)
        self.labelA = tk.Label(self.info_frame, text="A: []")
        self.labelA.grid(row=0, column=0, padx=10)
        self.labelB = tk.Label(self.info_frame, text="B: []")
        self.labelB.grid(row=0, column=1, padx=10)
        self.labelC = tk.Label(self.info_frame, text="C: []")
        self.labelC.grid(row=0, column=2, padx=10)

        self.reset()

    def reset(self):

        self.A = Pila()
        self.B = Pila()
        self.C = Pila()

        self.discos = 3

        for i in range(self.discos,0,-1):
            self.A.push(i)

        self.torres = [self.A.items, self.B.items, self.C.items]

        self.movimientos = []
        self.hanoi(self.discos,0,1,2)

        self.dibujar()
        self.actualizar_etiquetas()

    def hanoi(self,n,origen,aux,dest):

        if n == 1:
            self.movimientos.append((origen,dest))
        else:
            self.hanoi(n-1,origen,dest,aux)
            self.movimientos.append((origen,dest))
            self.hanoi(n-1,aux,origen,dest)

    def mover(self,origen,dest):

        pilas = [self.A,self.B,self.C]

        disco = pilas[origen].pop()
        pilas[dest].push(disco)

        self.torres = [self.A.items,self.B.items,self.C.items]
        self.actualizar_etiquetas()

    def dibujar(self):
        self.canvas.delete("all")

        posiciones = [100,300,500]
        base_y = 300

        self.canvas.create_rectangle(40,base_y,ANCHO-40,base_y+15,
                                     fill="#8b5a2b",outline="")

        for x in posiciones:
            self.canvas.create_rectangle(x-6,120,x+6,base_y,
                                         fill="#8b5a2b",outline="")

        colores = ["#ff9999","#33cc33","#009999"]

        for i,torre in enumerate(self.torres):
            x = posiciones[i]

            for j,disco in enumerate(torre):

                y = base_y - j*24
                ancho = 40 + disco*18

                self.canvas.create_rectangle(
                    x-ancho,y-20,
                    x+ancho,y,
                    fill=colores[disco-1],
                    outline="black",
                    width=2
                )

    def actualizar_etiquetas(self):
        self.labelA.config(text=f"A: {self.A.items}")
        self.labelB.config(text=f"B: {self.B.items}")
        self.labelC.config(text=f"C: {self.C.items}")

    def animar(self):

        if self.movimientos:

            o,d = self.movimientos.pop(0)

            self.mover(o,d)

            self.dibujar()
            self.actualizar_etiquetas()

            self.root.after(700,self.animar)


root = tk.Tk()
app = HanoiGUI(root)
root.mainloop()
