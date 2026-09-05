from src.exceptions.error import Error
from src.enums.name_type import NameType
from src.utils.name_resolver import check_name_type as check_name
from src.structures.statements.base_statement import BaseStatement


class PrintIntStatement(BaseStatement):
    def parse(self):
        self.check_for_error()

    def check_for_error(self):
        if len(self.arguments) != 1:
            raise Error(f"Wrong number of arguments for print_int: expected 1, got {len(self.arguments)} - line {self.line}")
        if check_name(self.arguments[0], self.program, self.function) not in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
            raise Error(f"Wrong argument '{self.arguments[0]}' - line {self.line}")

    def generate_nasm_code(self):
        return (
            "mov rdi, fmt_int?\n"
            f"mov rsi, {self.arguments[0]}\n"
            "xor rax, rax\n"
            "call printf\n")
