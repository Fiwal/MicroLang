from src.structures.statements.operation_statements.operation_stmt import OperationStatement

class ModStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            "mov r15, rax\n"
            f"mov r11, {self.arguments[1]}\n"
            f"mov rax, {self.arguments[0]}\n"
            "cqo\n"
            "idiv r11\n"
            f"mov {self.arguments[0]}, rdx\n"
            "mov rax, r15\n")
