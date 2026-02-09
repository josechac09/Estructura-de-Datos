# ================== DATOS BASE ==================

meses = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

departamentos = ["Ropa", "Deportes", "Juguetería"]

ventas = [
    [12000, 8500, 6400],
    [11000, 9000, 7000],
    [13500, 9200, 7600],
    [14000, 9800, 8000],
    [15000,10500, 8500],
    [15500,11000, 9000],
    [16000,11500, 9500],
    [15800,11200, 9200],
    [14500,10800, 8800],
    [15000,11000, 9000],
    [16500,12000,10000],
    [20000,15000,14000]
]

# ================== MÉTODOS ==================

def mostrar_tabla():
    print("------------------------------------------------------------")
    print(f"{'Mes':<12} | {'Ropa':<10} | {'Deportes':<10} | {'Juguetería':<10}")
    print("------------------------------------------------------------")

    for i in range(len(meses)):
        print(f"{meses[i]:<12} | {ventas[i][0]:<10} | {ventas[i][1]:<10} | {ventas[i][2]:<10}")

    print("------------------------------------------------------------")


def insertar_venta():
    mes = input("Mes: ")
    departamento = input("Departamento: ")
    monto = float(input("Monto de la venta: "))

    fila = meses.index(mes)
    columna = departamentos.index(departamento)
    ventas[fila][columna] = monto
    print("Venta insertada correctamente.")


def buscar_venta():
    mes = input("Mes: ")
    departamento = input("Departamento: ")

    fila = meses.index(mes)
    columna = departamentos.index(departamento)
    print("Venta encontrada:", ventas[fila][columna])


def eliminar_venta():
    mes = input("Mes: ")
    departamento = input("Departamento: ")

    fila = meses.index(mes)
    columna = departamentos.index(departamento)
    ventas[fila][columna] = 0
    print("Venta eliminada correctamente.")

# ================== MENÚ ==================

while True:
    print("\nMENÚ")
    print("1. Mostrar tabla de ventas")
    print("2. Insertar venta")
    print("3. Buscar venta")
    print("4. Eliminar venta")
    print("5. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        mostrar_tabla()
    elif opcion == "2":
        insertar_venta()
    elif opcion == "3":
        buscar_venta()
    elif opcion == "4":
        eliminar_venta()
    elif opcion == "5":
        print("Programa finalizado.")
        break
    else:
        print("Opción no válida.")
