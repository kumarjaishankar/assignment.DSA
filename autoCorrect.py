from collections import Counter
from itertools import product
from string import ascii_lowercase

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end_of_word

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,
                d[(i, j - 1)] + 1,
                d[(i - 1, j - 1)] + cost,
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)

    return d[lenstr1 - 1, lenstr2 - 1]

def get_suggestions(word, real_words, autocomplete=False):
    node = trie.root
    for char in word:
        if char not in node.children:
            return []

        node = node.children[char]

    suggestions = []

    def traverse(node, current_word):
        if node.end_of_word:
            suggestions.append(current_word)

        for char, child_node in node.children.items():
            traverse(child_node, current_word + char)

    traverse(node, word)

    if autocomplete:
        return suggestions

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in ascii_lowercase]
    inserts = [L + c + R for L, R in splits for c in ascii_lowercase]
    possible_words = set(deletes + transposes + replaces + inserts)

    edit_distance_suggestions = [(c, damerau_levenshtein_distance(word, c)) for c in possible_words if c in real_words]
    edit_distance_suggestions.sort(key=lambda tup: tup[1])

    return edit_distance_suggestions

def main():
    dictionary = ["the", "thy", "tar", "thru", "hr", "thor", "tur", "thar", "tor", "hell", "helly", "hello", "help", "hells", "sapa", "supa", "swa", "swap", "spa", "project", "coffee", "coffret", "coffer", "coffea"]  # Add your list of words here
    real_words = Counter(dictionary)
    global trie
    trie = Trie()
    for word in real_words:
        trie.insert(word)

    while True:
        word = input("Enter a word (or 'q' to quit): ")
        if word == 'q':
            break
        if not trie.search(word):
            suggestions = get_suggestions(word, real_words)
            autocomplete_suggestions = get_suggestions(word, real_words, autocomplete=True)
            print("Did you mean:", suggestions)
            print("Autocomplete suggestions:", autocomplete_suggestions)
        else:
            print(word, "is a valid word.")

if __name__ == "__main__":
    main()
