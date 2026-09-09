from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.utils import COMPARISON_JUMPS
from src.structures.statements.base_stmt import BaseStatement


class IfStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_if = None

    def parse(self):
        self.check_for_error()
        self.serial_number_of_if = self.function.if_counter
        self.function.if_stack.push({"else": False, "id": self.serial_number_of_if})
        self.function.if_counter += 1
        self.function.if_and_loop_stack.push("if")

    def check_for_error(self):
        if len(self.arguments) != 3:
            raise Error(f"Wrong number of arguments for if: expected 3, got {len(self.arguments)} - line {self.line}")
        value_types = [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]
        if check_name(self.arguments[0], self.program, self.function) not in value_types:
            raise Error(f"Wrong first argument for if '{self.arguments[0]}' - line {self.line}")
        if self.arguments[1] not in COMPARISON_JUMPS:
            raise Error(f"Wrong second argument for if '{self.arguments[1]}', it must be a comparison operator - line {self.line}")
        if check_name(self.arguments[2], self.program, self.function) not in value_types:
            raise Error(f"Wrong third argument for if '{self.arguments[2]}' - line {self.line}")

    def generate_nasm_code(self):
        return (
            f"mov r8, {self.arguments[0]}\n"
            f"mov r9, {self.arguments[2]}\n"
            "cmp r8, r9\n"
            f"j{COMPARISON_JUMPS[self.arguments[1]]} .else_{self.serial_number_of_if}\n")
