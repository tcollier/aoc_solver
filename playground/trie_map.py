import timeit


class TrieMap:
    value = None

    def __init__(self):
        self.nodes = {}

    def __setitem__(self, word, value):
        if not word:
            self.value = value
            return
        if word[0] not in self.nodes:
            self.nodes[word[0]] = TrieMap()
        self.nodes[word[0]][word[1:]] = value

    def __getitem__(self, word):
        if not word:
            return self.value
        if word[0] not in self.nodes:
            return None
        else:
            return self.nodes[word[0]][word[1:]]

    def keys(self, prefix=""):
        if self.value is not None:
            yield prefix
        for char, node in self.nodes.items():
            for key in node.keys(prefix + char):
                yield key

    def values(self):
        if self.value is not None:
            yield self.value
        for node in self.nodes.values():
            for value in node.values():
                yield value

    def items(self, prefix=""):
        if self.value is not None:
            yield prefix, self.value
        for char, node in self.nodes.items():
            for key, value in node.items(prefix + char):
                yield key, value


map = TrieMap()
map["apple"] = 1
map["aa"] = 2
map["a"] = 3
map[""] = 0

print([k for k in map.keys()])

print([v for v in map.values()])

for key, value in map.items():
    print(key, value)
