from src.structures.statements.operation_statements.operation_statement import OperationStatement

class MulStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov rax, {self.arguments[0]}\n"
            f"imul rax, {self.arguments[1]}\n"
            f"mov {self.arguments[0]}, rax\n")
