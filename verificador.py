import sys

def main():
    input_file = sys.argv[1]
    decompressed_file = "descomprimido-elmejorprofesor.txt"

    with open(input_file, "r", encoding="ISO-8859-1") as f:
        original_data = f.read()

    with open(decompressed_file, "r", encoding="ISO-8859-1") as f:
        decompressed_data = f.read()

    if original_data == decompressed_data:
        print("ok")
    else:
        print("nok")

if __name__ == "__main__":
    main()
