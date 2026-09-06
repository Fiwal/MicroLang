from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.structures.statements.base_statement import BaseStatement


class FunctionCallStatement(BaseStatement):
    argument_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.name = token.name

    def parse(self):
        self.check_for_error()

    def check_for_error(self):
        if not check_name(self.name, self.program, self.function) == NameType.FUNCTION:
            raise Error(f"Function '{self.name}' not found - line {self.line}")
        expected_num_of_arguments = 0
        for function in self.program.functions:
            if function.name == self.name:
                expected_num_of_arguments = function.parameter_count
        if len(self.arguments) != expected_num_of_arguments:
            raise Error(f"Wrong number of arguments for {self.name}: expected {expected_num_of_arguments}, got {len(self.arguments)} - line {self.line}")
        for argument in self.arguments:
            if check_name(argument, self.program, self.function) not in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                raise Error(f"Wrong argument for {self.name} '{argument}' - line {self.line}")

    def generate_nasm_code(self):
        nasm_code = ""
        for argument in range(len(self.arguments)):
            nasm_code += f"mov {self.argument_registers[argument]}, {self.arguments[argument]}\n"
        return nasm_code + f"call {self.name}\n"
