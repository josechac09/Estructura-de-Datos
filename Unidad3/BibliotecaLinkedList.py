# Biblioteca MyLinkedList
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class MyLinkedList:

    def __init__(self):
        self.head = None


    def insert_first(self, data):

        new_node = Node(data)

        new_node.next = self.head
        self.head = new_node


    def insert_last(self, data):

        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node


    def insert_at_position(self, index, data):

        if index <= 0 or not self.head:
            self.insert_first(data)
            return

        new_node = Node(data)
        current = self.head
        pos = 0

        while current and pos < index - 1:
            current = current.next
            pos += 1

        if not current:
            self.insert_last(data)
            return

        new_node.next = current.next
        current.next = new_node


    def delete_node(self, data):
        self.delete(data)


    def delete(self, data):

        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head

        while current.next:

            if current.next.data == data:
                current.next = current.next.next
                return

            current = current.next


    def to_list(self):

        datos = []

        current = self.head

        while current:
            datos.append(current.data)
            current = current.next

        return datos

class DoublyLinkedList:

    def __init__(self):
        self.head = None


    def insert_first(self, data):

        new_node = DoubleNode(data)

        if not self.head:
            self.head = new_node
            return

        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node


    def insert_last(self, data):

        new_node = DoubleNode(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node
        new_node.prev = current


    def insert_at_position(self, index, data):

        if index <= 0 or not self.head:
            self.insert_first(data)
            return

        current = self.head
        pos = 0

        while current.next and pos < index - 1:
            current = current.next
            pos += 1

        if not current.next:
            self.insert_last(data)
            return

        new_node = DoubleNode(data)
        new_node.next = current.next
        new_node.prev = current
        current.next.prev = new_node
        current.next = new_node


    def delete_node(self, data):

        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            return

        current = self.head

        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                return
            current = current.next


    def to_list(self):

        datos = []

        current = self.head

        while current:
            datos.append(current.data)
            current = current.next

        return datos


class CircularLinkedList:

    def __init__(self):
        self.head = None


    def insert_first(self, data):

        new_node = Node(data)

        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return

        tail = self.head
        while tail.next != self.head:
            tail = tail.next

        new_node.next = self.head
        tail.next = new_node
        self.head = new_node


    def insert_last(self, data):

        new_node = Node(data)

        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return

        tail = self.head

        while tail.next != self.head:
            tail = tail.next

        tail.next = new_node
        new_node.next = self.head


    def insert_at_position(self, index, data):

        if index <= 0 or not self.head:
            self.insert_first(data)
            return

        current = self.head
        pos = 0

        while current.next != self.head and pos < index - 1:
            current = current.next
            pos += 1

        if current.next == self.head and pos < index - 1:
            self.insert_last(data)
            return

        new_node = Node(data)
        new_node.next = current.next
        current.next = new_node


    def delete_node(self, data):

        if not self.head:
            return

        if self.head.data == data:
            if self.head.next == self.head:
                self.head = None
                return
            tail = self.head
            while tail.next != self.head:
                tail = tail.next
            self.head = self.head.next
            tail.next = self.head
            return

        prev = self.head
        current = self.head.next

        while current != self.head:
            if current.data == data:
                prev.next = current.next
                return
            prev = current
            current = current.next


    def show_connection(self):

        if not self.head:
            return "[]"

        parts = []
        current = self.head

        while True:
            parts.append(str(current.data))
            current = current.next
            if current == self.head:
                break

        return " -> ".join(parts) + " -> (vuelve a inicio)"


    def to_list(self):

        datos = []

        if not self.head:
            return datos

        current = self.head

        while True:
            datos.append(current.data)
            current = current.next

            if current == self.head:
                break

        return datos
