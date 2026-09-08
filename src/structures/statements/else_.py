from src.exceptions import Error
from src.structures.statements.base_statement import BaseStatement


class ElseStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_if = None

    def parse(self):
        self.check_for_error()
        current_if = self.function.if_stack.pop()
        current_if["else"] = True
        self.serial_number_of_if = current_if["id"]
        self.function.if_stack.push(current_if)

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for else: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.if_and_loop_stack.is_empty() or self.function.if_and_loop_stack.peek() == "loop":
            raise Error(f"else without matching if - line {self.line}")
        current_if = self.function.if_stack.peek()
        if current_if["else"]:
            raise Error(f"Duplicate else for the same if - line {self.line}")

    def generate_nasm_code(self):
        return (f"jmp .endif_{self.serial_number_of_if}\n"
                f".else_{self.serial_number_of_if}:\n")
