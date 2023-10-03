

from contextlib import nullcontext


class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    head = None

    def add(self, data):
        if self.head == None:
            self.head = data
            return
        current = self.head
        while current.next != None:
            current = current.next
        current.next = data

    def insert(self, index, data):
        if index < 0:
            return
        if index == 0:
            data.next = self.head
            self.head = data
            return
        current = self.head
        for i in range(index-1):
            current = current.next
            if current == None:
                return
        data.next = current.next
        current.next = data

    def remove(self, data):

        if self.head == None:
            return
        if self.head.next == None:
            if self.head.data == data:
                head = None
            return
        previous = self.head
        current = self.head.next

        while current != None:
            if (current.data == data):

                previous.next = current.next
                return
            current = current.next
            previous = previous.next

    def output(self):
        current = self.head
        while current != None:
            print(current.data)
            current = current.next


ll = LinkedList()
ll.add(Node(7))
ll.add(Node(3))
ll.add(Node(6))
ll.add(Node(5))
ll.insert(5, Node(8))

ll.output()
