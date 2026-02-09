import random
import time  

inicio = time.time()

matriz = []

for alumno in range(500):
    fila = []
    for materia in range(6):
        calificacion = random.randint(1, 10)
        fila.append(calificacion)
    matriz.append(fila)

print("+" + "-" * 73 + "+")
print("| Alumno    | Materia1 | Materia2 | Materia3 | Materia4 | Materia5 | Materia6 |")
print("+" + "-" * 73 + "+")

for i in range(500):
    print(f"| Alumno{i+1:3} ", end="")
    for j in range(6):
        print(f"| {matriz[i][j]:7} ", end="")
    print("|")

print("+" + "-" * 73 + "+")

print("\n" + "="*75)
print("BÚSQUEDA DE CALIFICACIÓN")
print("="*75)

try:
    num_alumno = int(input("Ingresa el número del alumno (1-500): "))
    num_materia = int(input("Ingresa el número de la materia (1-6): "))

    if 1 <= num_alumno <= 500 and 1 <= num_materia <= 6:
        calificacion = matriz[num_alumno - 1][num_materia - 1]
        print("\n" + "="*75)
        print(f"Alumno {num_alumno} - Materia {num_materia} = {calificacion}")
        print("="*75)
    else:
        print("\nError: Alumno debe estar entre 1-500 y Materia entre 1-6")
except ValueError:
    print("\nError: Debes ingresar números válidos")

fin = time.time()

print(f"\nTiempo de ejecución del programa: {fin - inicio:.4f} segundos")
