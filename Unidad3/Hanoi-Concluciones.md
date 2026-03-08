# Simulador Torre de Hanoi

Este proyecto es un **simulador visual de la Torre de Hanoi** desarrollado en **Python usando Tkinter**.  
Permite observar cómo funciona el algoritmo recursivo moviendo los discos entre tres torres, además de mostrar el número de movimientos y el tiempo de ejecución.

---

## Métodos utilizados en el programa

El programa utiliza **8 métodos principales**:

- **dibujar_base()**  
  Dibuja la base y las tres torres en el área gráfica.

- **dibujar_discos()**  
  Dibuja los discos en las torres según la cantidad seleccionada.

- **hanoi(n, origen, auxiliar, destino)**  
  Implementa el algoritmo recursivo que genera los movimientos necesarios para resolver la Torre de Hanoi.

- **actualizar_discos(valor)**  
  Actualiza la cantidad de discos cuando se modifica la escala.

- **iniciar()**  
  Inicializa la simulación, calcula los movimientos y comienza la animación.

- **actualizar_tiempo()**  
  Funciona como cronómetro para mostrar el tiempo de ejecución.

- **animar()**  
  Ejecuta la animación de los movimientos de los discos.

- **reset()**  
  Reinicia la simulación y vuelve al estado inicial.

---

## Pruebas de ejecución

El número mínimo de movimientos necesarios para resolver la Torre de Hanoi se calcula con la fórmula:

**Movimientos = 2ⁿ - 1**

Resultados obtenidos al ejecutar el programa:

- **5 discos**  
  Movimientos mínimos: 31  
  Tiempo aproximado: menor a 1 segundo.

- **10 discos**  
  Movimientos mínimos: 1023  
  Tiempo aproximado: alrededor de 1 a 2 segundos.

- **30 discos**  
  Movimientos mínimos: 1,073,741,823  
  El tiempo de ejecución sería demasiado grande para completarse.

- **64 discos**  
  Movimientos mínimos: 18,446,744,073,709,551,615  
  Resolver completamente el problema tomaría millones de años.

---

## Conclusiones

- La Torre de Hanoi se resuelve mediante un **algoritmo recursivo**.
- La complejidad del algoritmo es **exponencial (O(2ⁿ))**.
- A medida que aumenta el número de discos, el número de movimientos crece muy rápidamente.
- Para pocos discos el problema se resuelve casi instantáneamente.
- Con una cantidad grande de discos, como **64**, el tiempo necesario para resolverlo completamente es extremadamente alto.
