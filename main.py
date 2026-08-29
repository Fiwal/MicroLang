from src.lexer import Lexer
from src.parser import Parser
from src.compiler import Compiler


def main():
    lexer = Lexer("code.txt")
    try:
        parser = Parser(lexer.tokenize())
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return
    compiler = Compiler(parser.parse())
    compiler.compile()

if __name__ == "__main__":
    main()