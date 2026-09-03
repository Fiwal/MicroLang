#TODO

from src.exceptions.error import Error
from src.structures.statements.base_statement import BaseStatement


class EndLoopStatement(BaseStatement):
    def parse(self):
        self.check_for_error()
        self.arguments.append(self.function.loop_stack.pop()["id"])
        self.function.if_and_loop_stack.pop()

    def check_for_error(self):
        if self.arguments:
            raise Error(f"Wrong number of arguments for ENDLOOP: expected 0, got {len(self.arguments)} - line {self.line}")
        if self.function.if_and_loop_stack.is_empty() or self.function.if_and_loop_stack.peek() == "if":
            raise Error(f"ENDLOOP without matching LOOP - line {self.line}")

    def generate_nasm_code(self):
        return f"jmp .loop_{self.arguments[0]}\n.endloop_{self.arguments[0]}:\n"
