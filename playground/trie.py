DICTIONARY_FILE = "/usr/share/dict/words"


class Trie:
    def __init__(self):
        self.nodes = {}
        self.terminal = False

    def add(self, word):
        if not word:
            self.terminal = True
            return
        char = word[0].lower()
        if char not in self.nodes:
            self.nodes[char] = Trie()
        self.nodes[char].add(word[1:])

    def contains(self, word):
        if not word:
            return self.terminal
        char = word[0].lower()
        if char not in self.nodes:
            return False
        else:
            return self.nodes[char].contains(word[1:])


def build_trie(file):
    trie = Trie()
    for line in open(file, "r").readlines():
        trie.add(line.rstrip())
    return trie


def print_valid_word(trie, word):
    print(f'"{word}":', trie.contains(word))


trie = build_trie(DICTIONARY_FILE)
print_valid_word(trie, "appl")
print_valid_word(trie, "apple")
print_valid_word(trie, "applee")
print_valid_word(trie, "Apple")
print_valid_word(trie, "")
