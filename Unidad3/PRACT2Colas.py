
class Order:
    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer

    def __str__(self):
        return f"{self.customer} ({self.qtty})"


class Node:
    def __init__(self, info):
        self.info = info
        self.next = None

    def getNext(self):
        return self.next

    def setNext(self, next):
        self.next = next

    def getInfo(self):
        return self.info

class Queue:
    def __init__(self):
        self.top = None
        self.tail = None
        self.count = 0

    def isEmpty(self):
        return self.count == 0

    def front(self):
        if self.isEmpty():
            return None
        return self.top.getInfo()

    def enqueue(self, info):
        newNode = Node(info)
        if self.isEmpty():
            self.top = newNode
            self.tail = newNode
        else:
            self.tail.setNext(newNode)
            self.tail = newNode
        self.count += 1

    def dequeue(self):
        if self.isEmpty():
            return None
        temp = self.top
        self.top = self.top.getNext()
        self.count -= 1
        if self.top is None:
            self.tail = None
        return temp.getInfo()

    def getAll(self):
        node = self.top
        data = []
        while node:
            data.append(node.getInfo())
            node = node.getNext()
        return data


# -----------------------------
# Programa principal con historial
# -----------------------------
def main():
    queue = Queue()
    history = []

    while True:
        print("\n===== MENU =====")
        print("1. Agregar pedido")
        print("2. Eliminar pedido")
        print("3. Mostrar cola actual")
        print("4. Ver primer pedido")
        print("5. Mostrar historial")
        print("6. Salir")

        op = input("Seleccione una opción: ")

        if op == "1":
            customer = input("Nombre del cliente: ")
            qtty = input("Cantidad: ")
            if customer == "" or qtty == "":
                print("Ingrese todos los datos")
                continue
            order = Order(int(qtty), customer)
            queue.enqueue(order)
            history.append(f"Pedido agregado -> {order}")
            print(f"Pedido agregado: {order}")

        elif op == "2":
            removed = queue.dequeue()
            if removed:
                history.append(f"Pedido atendido -> {removed}")
                print(f"Pedido eliminado: {removed}")
            else:
                print("La cola está vacía")

        elif op == "3":
            orders = queue.getAll()
            if not orders:
                print("La cola está vacía")
            else:
                print("Cola actual:")
                for i, o in enumerate(orders, 1):
                    print(f"{i}. {o}")

        elif op == "4":
            front = queue.front()
            if front:
                print(f"Primer pedido: {front}")
            else:
                print("La cola está vacía")

        elif op == "5":
            if not history:
                print("Historial vacío")
            else:
                print("Historial de operaciones:")
                for h in history:
                    print(h)

        elif op == "6":
            print("Saliendo...")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
