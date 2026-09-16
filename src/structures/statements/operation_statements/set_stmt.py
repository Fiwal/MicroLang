from src.structures.statements.operation_statements.operation_stmt import OperationStatement


class SetStatement(OperationStatement):
    def generate_nasm_code(self):
        return (
            f"mov r10, {self.arguments[1]}\n"
            f"mov {self.arguments[0]}, r10\n")
