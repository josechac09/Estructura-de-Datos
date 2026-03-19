#  Sistema de Gestión de Postres con Listas Enlazadas

##  Descripción

Este proyecto consiste en una aplicación desarrollada en **Python utilizando Tkinter**, que permite gestionar un conjunto de postres y sus ingredientes.

Se implementa una estructura de datos donde:

- Existe un arreglo global llamado `POSTRES`
- Cada elemento es un objeto `Postre`
- Cada postre contiene una **lista enlazada de ingredientes**

Los postres se mantienen **ordenados alfabéticamente** y el sistema permite realizar operaciones completas sobre ellos.

---

##  Estructura de Datos

###  Clase `Nodo`
Representa un nodo de la lista enlazada.

- `ingrediente`: almacena el dato
- `sig`: apunta al siguiente nodo

---

###  Clase `ListaIngredientes`
Lista enlazada que gestiona los ingredientes.

**Métodos:**
- `insertar(ingrediente)` → Agrega al final
- `obtener_lista()` → Devuelve los ingredientes
- `eliminar(ingrediente)` → Elimina un ingrediente

---

###  Clase `Postre`
Representa un postre.

- `nombre`
- `ingredientes` → Lista enlazada

---

###  Arreglo `POSTRES`
Lista global donde se almacenan todos los postres.

---

##  Funcionalidades

###  Mostrar ingredientes
Permite visualizar los ingredientes de un postre.

- ✔ Si existe → muestra ingredientes  
- ❌ Si no existe → error  

---

###  Agregar ingrediente
Agrega un ingrediente a un postre existente.

- ✔ Postre válido → se agrega  
- ❌ Postre inexistente → error  

---

###  Eliminar ingrediente
Elimina un ingrediente específico.

- ✔ Existe → eliminado  
- ❌ No existe → error  

---

###  Agregar postre
Crea un nuevo postre.

- ✔ Se agrega y se ordena  
- ❌ (Programa 1) evita duplicados  

---

###  Eliminar postre
Elimina un postre junto con todos sus ingredientes.

---

##  Eliminación de elementos repetidos

Se implementó un subprograma que elimina automáticamente los postres repetidos:

```python
def eliminar_repetidos():

    nombres = []
    i = 0

    while i < len(POSTRES):

        nombre = POSTRES[i].nombre.lower()

        if nombre in nombres:
            POSTRES.pop(i)
        else:
            nombres.append(nombre)
            i += 1
