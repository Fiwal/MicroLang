from src.structures.statements.operation_statements.operation_statement import OperationStatement

class AddStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov rax, {self.arguments[1]}\n"
            f"add {self.arguments[0]}, rax\n")