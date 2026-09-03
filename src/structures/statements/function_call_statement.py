#TODO

from src.exceptions.error import Error
from src.enums.name_type import NameType
from src.utils.name_resolver import check_name_type as check_name
from src.structures.statements.base_statement import BaseStatement


class FunctionCallStatement(BaseStatement):
    argument_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

    def parse(self):
        self.check_for_error()

    def check_for_error(self):
        if check_name(self.token.name, self.parsed_program, self.function) != NameType.FUNCTION:
            raise Error(f"Function '{self.token.name}' not found - line {self.line}")
        called_function = next(function for function in self.parsed_program["functions"] if function.name == self.token.name)
        if len(self.arguments) != called_function.parameter_count:
            raise Error(f"Wrong number of arguments for {self.token.name}: expected {called_function.parameter_count}, got {len(self.arguments)} - line {self.line}")
        valid_types = [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]
        for argument in self.arguments:
            if check_name(argument, self.parsed_program, self.function) not in valid_types:
                raise Error(f"Wrong argument for {self.token.name} '{argument}' - line {self.line}")

    def generate_nasm_code(self):
        return "".join(f"mov {register}, {argument}\n" for register, argument in zip(self.argument_registers, self.arguments)) + f"call {self.token.name}\n"
