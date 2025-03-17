class FlatIterator:

    def __init__(self, list_of_list):
        self.stack = list(list_of_list)

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            item = self.stack.pop(0)
            if isinstance(item, list):
                # Если item - список, добавляем его к stack
                self.stack = item + self.stack
            else:
                return item
        raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()