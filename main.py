from src.compiler import Compiler
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter file path: ")
    if os.path.isfile(input_file):
        Compiler(input_file, "program").compile()
    else:
        print(f"File '{input_file}' not found")

#880 lines of code