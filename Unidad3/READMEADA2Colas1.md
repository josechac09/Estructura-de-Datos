# README – Funciones principales de la estructura Cola

## Descripción

El programa utiliza una **estructura de datos tipo Cola (Queue)** implementada en Python.
Una cola funciona con el principio **FIFO (First In, First Out)**, lo que significa que **el primer elemento que entra es el primero que sale**.

En el programa se crean **tres colas**:

* **Cola A**
* **Cola B**
* **Cola Resultado**

Las colas A y B almacenan los números ingresados por el usuario, y la cola resultado almacena **la suma de los elementos correspondientes de ambas colas**.

---

# Funciones principales utilizadas en la Cola

## `enqueue(item)`

Esta función permite **insertar un elemento al final de la cola**.

```python
def enqueue(self, item):
    self.items.append(item)
```

Se utiliza cuando el usuario **agrega números a la Cola A o Cola B**.

---

## `dequeue()`

Esta función permite **eliminar y devolver el primer elemento de la cola**.

```python
def dequeue(self):
    if self.items:
        return self.items.pop(0)
```

Se utiliza cuando el programa **extrae elementos de las colas para realizar la suma**.

---

## `is_empty()`

Esta función verifica si la cola **está vacía**.

```python
def is_empty(self):
    return len(self.items) == 0
```

Se utiliza en el ciclo `while` para saber **cuando ya no quedan elementos en la cola**.

---

## `size()`

Esta función devuelve la **cantidad de elementos que contiene la cola**.

```python
def size(self):
    return len(self.items)
```

Se utiliza para **verificar que ambas colas tengan el mismo número de elementos antes de realizar la suma**.

---

# Ejemplo de procedimiento

Supongamos que el usuario ingresa los siguientes valores.

### Cola A

```
2
4
6
```

### Cola B

```
1
3
5
```

### Paso 1 – Insertar elementos

Los números se agregan a las colas usando la función `enqueue()`.

Cola A

```
[2, 4, 6]
```

Cola B

```
[1, 3, 5]
```

---

### Paso 2 – Verificar tamaño

El programa utiliza `size()` para comprobar que ambas colas tienen **la misma cantidad de elementos**.

```
ColaA.size() = 3
ColaB.size() = 3
```

Como son iguales, se puede realizar la operación.

---

### Paso 3 – Extraer elementos

El programa utiliza `dequeue()` para retirar los elementos de cada cola.

```
2 + 1 = 3
4 + 3 = 7
6 + 5 = 11
```

---

### Paso 4 – Guardar resultados

Cada resultado se inserta en la **Cola Resultado** utilizando `enqueue()`.

Cola Resultado

```
[3, 7, 11]
```

---

# Resultado final

Cola A

```
2  4  6
```

Cola B

```
1  3  5
```

Cola Resultado

```
3  7  11
```

---

# Concepto aplicado

El programa demuestra el uso de **colas FIFO**, donde:

* Los elementos se insertan con `enqueue()`.
* Los elementos se retiran con `dequeue()`.
* Se mantiene el **orden de llegada de los datos**.

Esto permite procesar los elementos de ambas colas **en el mismo orden en que fueron ingresados**.
