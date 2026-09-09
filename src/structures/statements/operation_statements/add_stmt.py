from src.structures.statements.operation_statements.operation_stmt import OperationStatement

class AddStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov r15, {self.arguments[1]}\n"
            f"add {self.arguments[0]}, r15\n")
