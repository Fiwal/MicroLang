from src.exceptions.error import Error
from src.enums.name_type import NameType
from src.utils.name_resolver import check_name_type as check_name
from src.structures.statements.base_statement import BaseStatement


class PrintStatement(BaseStatement):
    def parse(self):
        self.check_for_error()

    def check_for_error(self):
        if len(self.arguments) != 1:
            raise Error(f"Wrong number of arguments for print: expected 1, got {len(self.arguments)} - line {self.line}")

        if check_name(self.arguments[0], self.parsed_program, self.function) != NameType.STRING_VARIABLE:
            raise Error(f"Wrong argument for print '{self.arguments[0]}', it must be a string variable - line {self.line}")

    def generate_nasm_code(self):
        return (
            f"mov rdi, {self.arguments[0]}\n"
            "xor rax, rax\n"
            "call printf\n")
