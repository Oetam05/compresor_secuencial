import heapq
import os
import sys
import time
import pickle
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"Node({self.char!r}, {self.freq})"


def write_file(file_path, content, tree, encoding=None):
    with open(file_path, "wb") as f:
        tree_data = pickle.dumps(tree)
        tree_length = len(tree_data).to_bytes(4, byteorder='big')
        f.write(tree_length)
        f.write(tree_data)

        content = int(content, 2).to_bytes((len(content) + 7) // 8, byteorder='big')
        f.write(content)


def build_huffman_tree(text):
    freqs = Counter(text)
    heap = [Node(char, freq) for char, freq in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        new_node = Node(None, lo.freq + hi.freq)
        new_node.left = lo
        new_node.right = hi

        heapq.heappush(heap, new_node)

    return heap[0]


def build_code_table(tree, prefix=''):
    if tree is None:
        return {}

    if tree.char:
        return {tree.char: prefix}

    left_codes = build_code_table(tree.left, prefix + '0')
    right_codes = build_code_table(tree.right, prefix + '1')

    return {**left_codes, **right_codes}


def huffman_encode(text, code_table):
    return ''.join(code_table[char] for char in text)


def read_file(file_path, encoding="ISO-8859-1"):
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()


def main():
    if len(sys.argv) < 2:
        print("Usage: python compresor.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    compressed_file = "comprimido.elmejorprofesor"

    # Read data
    data = read_file(input_file, encoding="ISO-8859-1")

    # Build Huffman tree and code table
    tree = build_huffman_tree(data)
    code_table = build_code_table(tree)

    # Encode data
    start_time = time.time()
    encoded_data = huffman_encode(data, code_table)
    write_file(compressed_file, encoded_data, tree, encoding=None)
    end_time = time.time()

    print("Compression time:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
