from src.exceptions.error import Error
from src.structures.statements.base_statement import BaseStatement


class EndifStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_if = None
        self.is_else_after_if = False

    def parse(self):
        self.check_for_error()
        current_if = self.function.if_stack.pop()
        self.serial_number_of_if = current_if["id"]
        if not current_if["else"]:
            self.is_else_after_if = True
        self.function.if_and_loop_stack.pop()

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for ENDIF: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.if_and_loop_stack.is_empty() or self.function.if_and_loop_stack.peek() == "loop":
            raise Error(f"ENDIF without matching IF - line {self.line}")

    def generate_nasm_code(self):
        if self.is_else_after_if:
            return f".else_{self.serial_number_of_if}:\n"
        return f".endif_{self.serial_number_of_if}:\n"
