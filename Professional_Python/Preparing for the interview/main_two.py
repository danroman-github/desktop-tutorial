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

def is_balanced(brackets):
    """Функция для проверки сбалансированности скобок."""
    stack = Stack()
    dictionary_brackets = {')': '(', ']': '[', '}': '{'}
    opening_brackets = set(dictionary_brackets.values())

    for char in brackets:
        if char in opening_brackets:
            stack.push(char)
        elif char in dictionary_brackets:
            if stack.is_empty() or stack.pop() != dictionary_brackets[char]:
                return "Несбалансированно"
        else:
            continue

    return "Сбалансированно" if stack.is_empty() else "Несбалансированно"

if __name__ == "__main__":
    test_strings = [
        "(((([{}]))))",
        "[([])((([[[]]])))]{()}",
        "{{[()]}}",
        "}{",
        "{{[(])]}}",
        "[[{())}]"
    ]

    for string in test_strings:
        print(f"{string}: {is_balanced(string)}")