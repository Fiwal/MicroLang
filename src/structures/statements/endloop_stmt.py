from src.exceptions import Error
from src.structures.statements.base_stmt import BaseStatement


class EndloopStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.serial_number_of_loop = None

    def parse(self):
        self.check_for_error()
        self.serial_number_of_loop = self.function.loop_stack.pop()["id"]
        self.function.if_and_loop_stack.pop()

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for endloop: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.if_and_loop_stack.is_empty() or self.function.if_and_loop_stack.peek() == "if":
            raise Error(f"endloop without matching loop - line {self.line}")

    def generate_nasm_code(self):
        return (f"jmp .loop_{self.serial_number_of_loop}\n"
                f".endloop_{self.serial_number_of_loop}:\n")
