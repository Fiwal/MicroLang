from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.structures.statements.base_stmt import BaseStatement


class InputStatement(BaseStatement):
    def parse(self):
        self.check_for_error()

    def check_for_error(self):
        if len(self.arguments) != 1:
            raise Error(f"Wrong number of arguments for input: expected 1, got {len(self.arguments)} - line {self.line}")
        if self.connected_tokens:
            raise Error(f"Cannot connect instructions with input - line {self.connected_tokens[0].line}")
        if check_name(self.arguments[0], self.program, self.function) not in [NameType.INT_VARIABLE]:
            raise Error(f"Wrong argument for input '{self.arguments[0]}' - line {self.line}")

    def generate_nasm_code(self):
        return (
            "mov rdi, fmt_int?\n"
            f"lea rsi, {self.arguments[0]}\n"
            "xor rax, rax\n"
            "call scanf\n")
