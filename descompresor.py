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


def read_file(file_path, encoding=None):
    with open(file_path, "rb") as f:
        tree_length = int.from_bytes(f.read(4), byteorder='big')
        tree_data = f.read(tree_length)
        tree = pickle.loads(tree_data)

        content = f.read()
        content = format(int.from_bytes(content, byteorder='big'), f"0{len(content) * 8}b")

    return content, tree


def huffman_decode(encoded_text, tree):
    decoded_text = []
    node = tree

    for bit in encoded_text:
        node = node.left if bit == '0' else node.right

        if node.char:
            decoded_text.append(node.char)
            node = tree

    return ''.join(decoded_text)


def write_file(file_path, content, encoding="ISO-8859-1"):
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)


def main():
    
    compressed_file = "comprimido.elmejorprofesor"
    decompressed_file = "descomprimido-elmejorprofesor.txt"

    # Read data and tree
    encoded_data, tree = read_file(compressed_file, encoding=None)

    # Decode data
    start_time = time.time()
    decoded_data = huffman_decode(encoded_data, tree)
    write_file(decompressed_file, decoded_data, encoding="ISO-8859-1")
    end_time = time.time()

    print("Decompression time:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
