from src.lexer import Lexer
from src.parser import Parser
from src.code_generator import CodeGenerator
from src.builder import Builder
from src.exceptions.error import Error

class Compiler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def compile(self):
        try:
            lexer = Lexer(self.input_file)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            parsed_program = parser.parse()

            nasm_code_generator = CodeGenerator(parsed_program, "output.asm")
            nasm_code_generator.generate_nasm_code()

            builder = Builder("output.asm", self.output_file)
            builder.build_executable()

        except Error as e:
            print(f"\033[1;31mError: {e}\033[0m")
            return

