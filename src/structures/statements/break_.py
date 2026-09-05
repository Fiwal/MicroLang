from src.exceptions.error import Error
from src.structures.statements.base_statement import BaseStatement


class BreakStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_loop = None

    def parse(self):
        self.check_for_error()
        self.serial_number_of_loop = self.function.loop_stack.peek()["id"]

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for break: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.loop_stack.is_empty():
            raise Error(f"break outside of LOOP - line {self.line}")

    def generate_nasm_code(self):
        return f"jmp .endloop_{self.serial_number_of_loop}\n"
