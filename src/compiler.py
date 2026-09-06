from src.pipeline.lexer import Lexer
from src.pipeline.parser import Parser
from src.pipeline.code_generator import CodeGenerator
from src.pipeline.builder import Builder
from src.exceptions import Error


class Compiler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def compile(self):
        try:
            tokens = Lexer(self.input_file).tokenize()
            parsed_program = Parser(tokens).parse()
            CodeGenerator(parsed_program, "output.asm").generate_nasm_code()
            Builder("output.asm", self.output_file).build_executable()
        except Error as e:
            print(f"\033[1;31mError: {e}\033[0m")
            return
