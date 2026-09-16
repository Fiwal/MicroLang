from src.exceptions import Error
from src.utils import check_name_type as check_name
from src.enums import NameType
from src.structures.statements.base_stmt import BaseStatement

class OperationStatement(BaseStatement):
    def __init__(self, token, program, function):
        super().__init__(token, program, function)
        self.operation_name = token.name

    def parse(self):
        if len(self.arguments) != 2:
            raise Error(f"Wrong number of arguments for {self.operation_name}: expected 2, got {len(self.arguments)} - line {self.line}")
        if self.connected_tokens:
            raise Error(f"Cannot connect instructions with {self.operation_name} - line {self.connected_tokens[0].line}")
        if not check_name(self.arguments[0], self.program, self.function) in [NameType.INT_VARIABLE]:
            raise Error(f"Wrong first argument for {self.operation_name} '{self.arguments[0]}' - line {self.line}")
        if not check_name(self.arguments[1], self.program, self.function) in [NameType.INT_VARIABLE, NameType.INT_NUM]:
            raise Error(f"Wrong argument '{self.arguments[1]}' - line {self.line}")
