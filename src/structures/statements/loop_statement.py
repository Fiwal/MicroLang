#TODO

from src.exceptions.error import Error
from src.structures.statements.base_statement import BaseStatement


class LoopStatement(BaseStatement):
    def parse(self):
        self.check_for_error()
        self.arguments.append(self.function.loop_counter)
        self.function.loop_stack.push({"id": self.function.loop_counter})
        self.function.loop_counter += 1
        self.function.if_and_loop_stack.push("loop")

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for LOOP: expected 0, got {len(self.arguments)} - line {self.line}")
    def generate_nasm_code(self):
        return f".loop_{self.arguments[0]}:\n"
