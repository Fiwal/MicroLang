from src.exceptions import Error
from src.utils import check_name_type as check_name, is_valid_name
from src.enums import NameType
from src.structures.statements.base_stmt import BaseStatement


class IntStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_variable = None

    def parse(self):
        self.check_for_error()
        self.function.local_variables.append(self.arguments[0])
        self.serial_number_of_variable = len(self.function.local_variables)

    def check_for_error(self):
        if not len(self.arguments) in [1, 2]:
            raise Error(f"Wrong number of arguments for int: expected 1 or 2, got {len(self.arguments)} - line {self.line}")
        if self.connected_tokens:
            raise Error(f"Cannot connect instructions with int - line {self.connected_tokens[0].line}")
        if not is_valid_name(self.arguments[0]):
            raise Error(f"Wrong variable name '{self.arguments[0]}' - line {self.line}")
        if not check_name(self.arguments[0], self.program, self.function) == NameType.NOT_FOUND:
            raise Error(f"Multiple name '{self.arguments[0]}' - line {self.line}")
        if len(self.arguments) == 2 and not check_name(self.arguments[1], self.program, self.function) in [NameType.INT_VARIABLE, NameType.INT_NUM]:
            raise Error(f"Wrong second argument for int '{self.arguments[1]}' - line {self.line}")

    def generate_nasm_code(self):
        if len(self.arguments) == 1:
            return f"%define {self.arguments[0]} [rbp-{(self.serial_number_of_variable + self.function.parameter_count) * 8}]\n"
        else:
            return (
                f"%define {self.arguments[0]} [rbp-{(self.serial_number_of_variable + self.function.parameter_count) * 8}]\n"
                f"mov r10, {self.arguments[1]}\n"
                f"mov {self.arguments[0]}, r10\n")
