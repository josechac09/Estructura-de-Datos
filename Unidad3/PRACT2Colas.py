class Order:

    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def print(self):
        print("     Customer:", self.customer)
        print("     Quantity:", self.qtty)
        print("     ------------")

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer

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

    
    def size(self):
        return self.count

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

    def printInfo(self):

        print("\n********* QUEUE DUMP *********")
        print("   Size:", self.size())

        node = self.top
        i = 1

        while node != None:

            print("   ** Element", i)

            order = node.getInfo()
            order.print()

            node = node.getNext()
            i += 1

        print("******************************")

    def getNth(self, pos):

        if pos <= 0 or pos > self.size():
            return None

        node = self.top
        i = 1

        while node != None:

            if i == pos:
                return node.getInfo()

            node = node.getNext()
            i += 1

        return None


def main():

    queue = Queue()

    order1 = Order(20, "cust1")
    order2 = Order(30, "cust2")
    order3 = Order(40, "cust3")
    order4 = Order(50, "cust4")

    print("Insertando pedidos...")
    queue.enqueue(order1)
    queue.printInfo()

    queue.enqueue(order2)
    queue.printInfo()

    queue.enqueue(order3)
    queue.printInfo()

    queue.enqueue(order4)
    queue.printInfo()

    print("\nPrimer elemento (front):")
    front = queue.front()
    if front:
        front.print()

    print("\nEliminando primer elemento (dequeue):")
    removed = queue.dequeue()
    if removed:
        removed.print()

    queue.printInfo()

    print("\nObteniendo el 3er elemento:")
    third = queue.getNth(3)

    if third:
        third.print()
    else:
        print("Posición no válida")

main()
