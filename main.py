from src.lexer import Lexer
from src.parser import Parser
from src.compiler import Compiler
from src.exceptions.error import Error


def main():
    lexer = Lexer("code.txt")
    try:
        tokens = lexer.tokenize()
    except Error as e:
        print(f"\033[1;31mError: {e}\033[0m")
        return

    parser = Parser(tokens)
    try:
        ast = parser.parse()
    except Error as e:
        print(f"\033[1;31mError: {e}\033[0m")
        return

    compiler = Compiler(ast)
    compiler.compile()

if __name__ == "__main__":
    main()
