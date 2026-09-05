from src.exceptions.error import Error
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
            raise Error(f"Wrong number of arguments for ELSE: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.if_and_loop_stack.is_empty() or self.function.if_and_loop_stack.peek() == "loop":
            raise Error(f"ELSE without matching IF - line {self.line}")
        current_if = self.function.if_stack.peek()
        if current_if["else"]:
            raise Error(f"Duplicate ELSE for the same IF - line {self.line}")

    def generate_nasm_code(self):
        return (f"jmp .endif_{self.serial_number_of_if}\n"
                f".else_{self.serial_number_of_if}:\n")
