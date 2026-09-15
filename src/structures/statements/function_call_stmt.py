from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.structures.statements.base_stmt import BaseStatement


class FunctionCallStatement(BaseStatement):
    argument_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.name = token.name

    def parse(self):
        self.check_for_error()
        self.check_for_error_in_connected_tokens()

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

    def check_for_error_in_connected_tokens(self):
        if len(self.connected_tokens) not in [0, 1]:
            raise Error(f"Too many connected instructions with {self.name}, expected 0 or 1 got {len(self.connected_tokens)} - line {self.connected_tokens[0].line}")
        if self.connected_tokens:
            connected_token = self.connected_tokens[0]
            if connected_token.name != "get":
                raise Error(f"Wrong connected instruction name {connected_token.name} - line {connected_token.line}")
            if len(connected_token.arguments) != 1:
                raise Error(f"Wrong number of arguments for {connected_token.name}: expected 1, got {len(connected_token.arguments)} - line {self.line}")
            if check_name(connected_token.arguments[0], self.program, self.function) not in [NameType.INT_VARIABLE, NameType.PARAMETER]:
                raise Error(f"Wrong argument for {connected_token.name} '{connected_token.arguments[0]}' - line {self.line}")

    def generate_nasm_code(self):
        nasm_code = ""
        if len(self.arguments) <= 6:
            for i in range(len(self.arguments)):
                nasm_code += f"mov {self.argument_registers[i]}, {self.arguments[i]}\n"
            nasm_code += f"call {self.name}\n"
        else:
            for i in range(6):
                nasm_code += f"mov {self.argument_registers[i]}, {self.arguments[i]}\n"
            if len(self.arguments) % 2 != 0:
                nasm_code += f"sub rsp, 8\n"
            for i in range(len(self.arguments) - 1, 5, -1):
                nasm_code += f"push {self.arguments[i]}\n"
            nasm_code += (
                f"call {self.name}\n"
                f"add rsp, {(len(self.arguments) - 6) * 8 + 8 * (len(self.arguments) % 2)}\n")
        if self.connected_tokens:
            return nasm_code + f"mov {self.connected_tokens[0].arguments[0]}, rax\n"
        return nasm_code

    def add_dollar_sign(self):
        super().add_dollar_sign()
        if self.name != "main":
            self.name += "$"

