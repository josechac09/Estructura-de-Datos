# README – Funciones principales de la estructura Cola (Sistema de Turnos)

## Descripción

El programa utiliza una **estructura de datos tipo Cola (Queue)** implementada en Python.
Una cola funciona con el principio **FIFO (First In, First Out)**, lo que significa que **el primer elemento que entra es el primero que sale**.

En el programa se crean **tres colas de servicio** para una compañía de seguros:

* **Servicio 1**
* **Servicio 2**
* **Servicio 3**

Cada cola almacena los **turnos de los clientes** que llegan para ser atendidos.
Cuando el personal atiende a un cliente, se llama **al primer turno que llegó a la cola**.

---

# Funciones principales utilizadas en la Cola

## encolar(elemento)

Esta función permite **insertar un elemento al final de la cola**.

```python
def encolar(self, elemento):
    self.items.append(elemento)
```

Se utiliza cuando **llega un nuevo cliente al servicio** y se le asigna un turno.

Ejemplo de turno generado:

```
S1-1
S1-2
S2-1
```

---

## desencolar()

Esta función permite **eliminar y devolver el primer elemento de la cola**.

```python
def desencolar(self):
    if not self.esta_vacia():
        return self.items.pop(0)
```

Se utiliza cuando **el personal de atención llama al siguiente cliente**.

---

## esta_vacia()

Esta función verifica si la cola **no tiene clientes esperando**.

```python
def esta_vacia(self):
    return len(self.items) == 0
```

Se usa para evitar intentar atender clientes **cuando la cola está vacía**.

---

## mostrar()

Esta función devuelve los elementos de la cola para **poder mostrarlos en la interfaz gráfica**.

```python
def mostrar(self):
    return self.items
```

Se utiliza para **dibujar visualmente las colas en la pantalla**.

---

# Ejemplo de procedimiento

Supongamos que llegan los siguientes clientes.

### Paso 1 – Llegada de clientes

El usuario escribe los comandos:

```
C1
C1
C2
```

Significado:

* **C1** → llega un cliente al servicio 1
* **C1** → llega otro cliente al servicio 1
* **C2** → llega un cliente al servicio 2

Colas después de registrar los clientes:

Servicio 1

```
[S1-1, S1-2]
```

Servicio 2

```
[S2-1]
```

Servicio 3

```
[]
```

---

### Paso 2 – Atender cliente

El usuario escribe:

```
A1
```

Esto significa **atender al primer cliente de la cola del servicio 1**.

El sistema usa `desencolar()` y muestra:

```
Atendiendo: S1-1
```

---

### Paso 3 – Estado de las colas después de atender

Servicio 1

```
[S1-2]
```

Servicio 2

```
[S2-1]
```

Servicio 3

```
[]
```

---

# Concepto aplicado

El programa demuestra el uso de **colas FIFO**, donde:

* Los clientes **se agregan al final de la cola** con `encolar()`.
* Los clientes **se atienden desde el inicio de la cola** con `desencolar()`.
* Se respeta el **orden de llegada de los clientes**.

Este tipo de estructura se utiliza comúnmente en **sistemas de atención al cliente, bancos, hospitales y compañías de seguros**.
