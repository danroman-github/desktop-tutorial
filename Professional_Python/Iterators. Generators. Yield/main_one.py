class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.len_lists = 0
        self.cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.len_lists < len(self.list_of_list):
            if self.cursor < len(self.list_of_list[self.len_lists]):
                item = self.list_of_list[self.len_lists][self.cursor]
                self.cursor += 1
                return item
            else:
                self.len_lists += 1
                self.cursor = 0
        raise  StopIteration


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