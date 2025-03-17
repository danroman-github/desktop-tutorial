# Задание «Iterators. Generators. Yield»

## Задание 1

Доработать класс FlatIterator в коде ниже. Должен получиться итератор, который принимает список списков 
и возвращает их плоское представление, т. е. последовательность, состоящую из вложенных элементов. 
Функция test в коде ниже также должна отработать без ошибок.

```python
class FlatIterator:

    def __init__(self, list_of_list):
        ...

    def __iter__(self):
        ...
        return self

    def __next__(self):
        ...
        return item


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
```

[main_one.py](/Professional_Python/Iterators.%20Generators.%20Yield/main_one.py)


## Задание 2

Импортировать функции в модуль main.py и вызывать эти функции в конструкции.

```python
if __name__ == '__main__':
```

Сами функции реализовывать не нужно. Достаточно добавить туда какой-либо вывод.

## Задание 3

Познакомиться с модулем datetime. При вызове функций модуля main.py выводить текущую дату.

## Задание 4

Найти интересный для себя пакет на pypi (выбран loguru) и в файле [requirements.txt](/Professional_Python/Import.%20Module.%20Package/requirements.txt) указать его с актуальной версией. При желании можно написать программу с этим пакетом.

## Задание 5

Создать рядом с файлом main.py модуль [dirty_main.py](/Professional_Python/Import.%20Module.%20Package/dirty_main.py) и импортировать все функции с помощью конструкции

```python
from package.module import *
```
