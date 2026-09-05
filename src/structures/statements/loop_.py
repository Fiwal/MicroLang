from src.exceptions.error import Error
from src.structures.statements.base_statement import BaseStatement


class LoopStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_loop = None

    def parse(self):
        self.check_for_error()
        self.serial_number_of_loop = self.function.loop_counter
        self.function.loop_stack.push({"id": self.function.loop_counter})
        self.function.loop_counter += 1
        self.function.if_and_loop_stack.push("loop")

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for LOOP: expected 0, got {len(self.arguments)} - line {self.line}")

    def generate_nasm_code(self):
        return f".loop_{self.serial_number_of_loop}:\n"
