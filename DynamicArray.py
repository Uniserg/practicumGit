from array import array
from collections.abc import Sequence


class DynamicArray(object):
    def __init__(self, typ, arr=None):
        if arr:
            self.__items = array(typ, arr)
            self.__size = len(self.__items)
        else:
            self.items = array(typ, (i for i in range(10)))
            self.__size = 10

    def __sizeof__(self):
        return self.items.__sizeof__()

    def __str__(self):
        return f"DynamicArray[{', '.join((str(self.__items[i]) for i in range(self.__size)))}]"

    def __len__(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def __check_empty(self):
        if self.is_empty():
            raise Exception("Array is empty")

    def __check_index(self, index):
        if index >= self.__size or index < 0:
            raise Exception("Index out of range")

    def __getitem__(self, item):
        self.__check_index(item)

        return self.__items[item]

    def __iadd__(self, other):
        self.push_back_range(other)
        return self

    def find(self, item):
        for i in range(self.__size):
            if self.__items[i] == item:
                return i
        return -1

    def find_last(self, key):
        for i in range(self.__size - 1, -1, -1):
            if self.__items[i] == key:
                return i
        return -1

    def __increase_array(self, ext=1):
        new_size = len(self.__items) * 2 - 1 + ext
        new_arr = [0] * new_size
        for i in range(self.__size):
            new_arr[i] = self.__items[i]

        self.__items = new_arr

    def __need_inc(self, length=1):
        if len(self.__items) - self.__size < length:
            self.__increase_array(length)

    def append(self, item):
        self.__need_inc()

        self.__items[self.__size] = item
        self.__size += 1

    def insert(self, index, item):
        self.__check_index(index)
        self.__need_inc()

        for i in range(self.__size - 1, index - 1, -1):
            self.__items[i + 1] = self.__items[i]

        self.__items[index] = item
        self.__size += 1

    @staticmethod
    def __check_sequence(array):
        if not isinstance(array, Sequence):
            raise Exception("Bad argument (not iterable)")

    def push_back_range(self, array):
        self.__check_sequence(array)
        self.__need_inc(len(array))
        for i in range(self.__size, self.__size + len(array)):
            self.__items[i] = array[i - self.__size]

        self.__size += len(array)

    def insert_range(self, index, array):
        self.__check_sequence(array)
        l_arr = len(array)
        self.__need_inc(l_arr)

        self.__size += l_arr
        for i in range(self.__size - 1, index - 1, -1):
            self.__items[i] = self.__items[i - l_arr]

        for i in range(index, index + l_arr):
            self.__items[i] = array[i - index]

    def pop_back(self):
        self.__check_empty()
        self.__size -= 1

        return self.__items[self.__size]

    def pop(self, index=-1):
        if index == -1:
            self.__check_empty()
            self.__size -= 1

            return self.__items[self.__size]
        else:
            r = self.__items[index]
            self.remove_by_index(index)
            return r

    def remove_by_index(self, index):
        self.__check_empty()
        self.__check_index(index)

        for i in range(index + 1, self.__size):
            self.__items[i - 1] = self.__items[i]

        self.__size -= 1

    def pop_front(self):
        self.remove_by_index(0)

    def remove(self, item):
        for i in range(self.__size):
            if item == self.__items[i]:
                self.remove_by_index(i)
                return True
        return False

    def remove_all(self, item):
        new_size = 0
        for i in range(self.__size):
            if self.__items[i] != item:
                self.__items[new_size] = self.__items[i]
                new_size += 1
        r = self.__size - new_size
        self.__size = new_size
        return r
