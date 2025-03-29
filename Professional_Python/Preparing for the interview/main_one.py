class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        """Проверка стека на пустоту."""
        return len(self.items) == 0

    def push(self, item):
        """Добавляет новый элемент на вершину стека."""
        self.items.append(item)

    def pop(self):
        """Удаляет верхний элемент стека."""
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Стек пуст")

    def peek(self):
        """Возвращает верхний элемент стека, но не удаляет его."""
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Стек пуст")

    def size(self):
        """Возвращает количество элементов в стеке."""
        return len(self.items)


if __name__ == '__main__':
    stack = Stack()
    print(stack.is_empty())  # True

    stack.push(4)
    stack.push(3)
    stack.push(2)
    stack.push(1)

    print(stack.peek())  # 3
    print(stack.size())  # 3

    print(stack.pop())  # 3
    print(stack.pop())  # 2
    print(stack.size())  # 1
    print(stack.is_empty())  # False