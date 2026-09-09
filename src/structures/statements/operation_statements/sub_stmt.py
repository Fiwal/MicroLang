from src.structures.statements.operation_statements.operation_stmt import OperationStatement

class SubStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov rax, {self.arguments[1]}\n"
            f"sub {self.arguments[0]}, rax\n")
