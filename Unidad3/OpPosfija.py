import tkinter as tk                                                                                                                             
from tkinter import messagebox

pila = []                                                                                                                                        
pasos = []
indice_paso = 0

def push(valor):                                                                                                                                 
    pila.append(valor)
    actualizar_pila()

def pop():                                                                                                                                        
    if len(pila) == 0:
        raise Exception("Subdesbordamiento de pila")
    valor = pila.pop()
    actualizar_pila()
    return valor

def operar(a, b, op):                                                                                                                           

    if op == "+":
        return a + b

    if op == "-":
        return a - b

    if op == "*":
        return a * b

    if op == "/":
        return a / b

    raise Exception("Operador inválido")

def generar_pasos_posfija(exp):                                                                                                                

    temp_pila = []
    lista_pasos = []

    tokens = exp.split()

    for token in tokens:

        if token.isdigit():

            temp_pila.append(int(token))
            lista_pasos.append(("push", int(token), list(temp_pila)))

        else:

            b = temp_pila.pop()
            a = temp_pila.pop()

            resultado = operar(a, b, token)

            temp_pila.append(resultado)

            lista_pasos.append(("operar", f"{a} {token} {b} = {resultado}", list(temp_pila)))

    return lista_pasos, temp_pila[-1]

def ejecutar_pasos():                                                                                                                         

    global indice_paso

    if indice_paso >= len(pasos):
        return

    accion, texto, estado = pasos[indice_paso]

    pila.clear()
    pila.extend(estado)

    actualizar_pila()

    if accion == "push":
        info_label.config(text=f"Insertando {texto} en la pila")

    else:
        info_label.config(text=f"Operación: {texto}")

    indice_paso += 1

    ventana.after(1000, ejecutar_pasos)

def evaluar():

    global pasos, indice_paso

    expresion = entrada.get()
    tipo = tipo_notacion.get()

    if expresion == "":
        messagebox.showwarning("Aviso", "Escribe una expresión")
        return

    try:

        pila.clear()
        actualizar_pila()

        if tipo == "Posfija":

            pasos, resultado = generar_pasos_posfija(expresion)

        else:
            messagebox.showinfo("Aviso", "La animación está implementada para Posfija")
            return

        indice_paso = 0
        ejecutar_pasos()

        resultado_label.config(text="Resultado final: " + str(resultado))

    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_pila():

    canvas.delete("all")

    y = 300

    for elemento in reversed(pila):

        canvas.create_rectangle(
            120,
            y,
            220,
            y - 40,
            fill="#6fa8dc",
            outline="black"
        )

        canvas.create_text(
            170,
            y - 20,
            text=str(elemento),
            font=("Arial", 14, "bold")
        )

        y -= 45

    canvas.create_text(
        170,
        330,
        text="PILA",
        font=("Arial", 12, "bold")
    )

ventana = tk.Tk()
ventana.title("Evaluador con Pila")
ventana.geometry("450x500")
ventana.config(bg="#f4f4f4")

titulo = tk.Label(
    ventana,
    text="Evaluador Posfija con Pila",
    font=("Arial", 16, "bold"),
    bg="#f4f4f4"
)
titulo.pack(pady=10)

entrada = tk.Entry(
    ventana,
    font=("Arial", 14),
    width=25
)
entrada.pack(pady=10)

tipo_notacion = tk.StringVar()
tipo_notacion.set("Posfija")

menu = tk.OptionMenu(
    ventana,
    tipo_notacion,
    "Posfija",
    "Prefija"
)
menu.pack(pady=5)

boton = tk.Button(
    ventana,
    text="Evaluar Expresión",
    command=evaluar,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12)
)
boton.pack(pady=10)

info_label = tk.Label(
    ventana,
    text="Proceso:",
    font=("Arial", 12),
    bg="#f4f4f4"
)
info_label.pack()

resultado_label = tk.Label(
    ventana,
    text="Resultado:",
    font=("Arial", 14),
    bg="#f4f4f4"
)
resultado_label.pack(pady=10)

canvas = tk.Canvas(
    ventana,
    width=350,
    height=350,
    bg="white"
)
canvas.pack(pady=10)

ventana.mainloop()
