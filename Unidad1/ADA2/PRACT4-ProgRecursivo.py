import time

def fibonacci_recursivo(n):

    if n <= 1:
        return n
    
    return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

def fibonacci_iterativo(n):
    a, b = 0, 1
    
    for i in range(n):
        a, b = b, a + b
    
    return a

def main():
    print("===== COMPARACIÓN FIBONACCI =====")
    n = int(input("Ingresa el valor de n: "))

    inicio_rec = time.time()
    resultado_rec = fibonacci_recursivo(n)
    fin_rec = time.time()

    tiempo_rec = fin_rec - inicio_rec

    inicio_it = time.time()
    resultado_it = fibonacci_iterativo(n)
    fin_it = time.time()

    tiempo_it = fin_it - inicio_it

    print("\n===== RESULTADOS =====")
    print(f"Fibonacci recursivo({n}) = {resultado_rec}")
    print(f"Tiempo recursivo: {tiempo_rec:.10f} segundos")

    print("\nFibonacci iterativo({}) = {}".format(n, resultado_it))
    print(f"Tiempo iterativo: {tiempo_it:.10f} segundos")

    print("\n===== COMPARACIÓN =====")
    if tiempo_rec > tiempo_it:
        print("El método ITERATIVO fue más rápido.")
    else:
        print("El método RECURSIVO fue más rápido.")

main()
