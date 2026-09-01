from src.structures.statements.operation_statements.operation_statement import OperationStatement

class ModStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov r11, {self.arguments[1]}\n"
            f"mov rax, {self.arguments[0]}\n"
            "cqo\n"
            "idiv r11\n"
            f"mov {self.arguments[0]}, rdx\n")