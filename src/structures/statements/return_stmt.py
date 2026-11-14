from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.structures.statements.base_stmt import BaseStatement


class ReturnStatement(BaseStatement):
    def parse(self):
        if len(self.arguments) not in [0, 1]:
            raise Error(f"Wrong number of arguments for return: expected 0 or 1, got {len(self.arguments)} - line {self.line}")
        if self.connected_tokens:
            raise Error(f"Cannot connect instructions with return - line {self.connected_tokens[0].line}")
        if self.arguments and check_name(self.arguments[0], self.program, self.function) not in [NameType.INT_VARIABLE, NameType.RETURN_VALUE, NameType.INT_NUM]:
            raise Error(f"Wrong argument for return '{self.arguments[0]}' - line {self.line}")

    def generate_nasm_code(self):
        code = ""
        if len(self.arguments) == 1:
            code += f"mov rax, {self.arguments[0]}\n"
        else:
            code += f"mov rax, 0\n"
        return code + "jmp .end\n"
