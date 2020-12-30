import random


class Heap(object):
    def __init__(self, min=True):
        self.items = []
        self.size = 0
        if min:
            self.cmp = self.__class__.min_cmp
        else:
            self.cmp = self.__class__.max_cmp

    @classmethod
    def min_cmp(cls, a, b):
        return a < b

    @classmethod
    def max_cmp(cls, a, b):
        return a > b

    def insert(self, value):
        if self.size == len(self.items):
            self.items.append(value)
        else:
            self.items[self.size] = value
        self._percolate_up(self.size)
        self.size += 1

    def peek(self):
        if not self.items:
            return None
        else:
            return self.items[0]

    def delete(self):
        if self.size == 0:
            return None
        value = self.items[0]
        self.items[0] = self.items[self.size - 1]
        self.items[self.size - 1] = None
        self.size -= 1
        self._percolate_down(0)
        self.items.pop()
        return value

    def _percolate_up(self, index):
        if index == 0:
            return
        parent_index = (index + 1) // 2 - 1
        if self.cmp(self.items[index], self.items[parent_index]):
            temp = self.items[index]
            self.items[index] = self.items[parent_index]
            self.items[parent_index] = temp
            self._percolate_up(parent_index)

    def _percolate_down(self, index):
        left_index = (index + 1) * 2 - 1
        if left_index >= self.size:
            return
        right_index = left_index + 1
        if right_index >= self.size:
            child_index = left_index
        elif self.cmp(self.items[left_index], self.items[right_index]):
            child_index = left_index
        else:
            child_index = right_index
        if not self.cmp(self.items[index], self.items[child_index]):
            temp = self.items[index]
            self.items[index] = self.items[child_index]
            self.items[child_index] = temp
            self._percolate_down(child_index)


class RunningMedian(object):
    def __init__(self):
        self.upper = Heap(True)
        self.lower = Heap(False)

    def size(self):
        return self.upper.size + self.lower.size

    def add(self, val):
        if self.upper.size == 0:
            self.upper.insert(val)
        elif self.upper.size == self.lower.size:
            self.upper.insert(val)
            if self.upper.peek() < self.lower.peek():
                temp = self.upper.delete()
                self.lower.insert(temp)
                temp = self.lower.delete()
                self.upper.insert(temp)
        else:
            self.lower.insert(val)
            if self.lower.peek() > self.upper.peek():
                temp = self.lower.delete()
                self.upper.insert(temp)
                temp = self.upper.delete()
                self.lower.insert(temp)

    def median(self):
        if self.upper.size == self.lower.size:
            return (self.upper.peek() + self.lower.peek()) / 2
        else:
            return self.upper.peek()

    def __repr__(self):
        return f"UPPER: {self.upper.items}\nLOWER: {self.lower.items}"


rm = RunningMedian()
for i in range(10000):
    rm.add(random.random())

print(rm.median())
