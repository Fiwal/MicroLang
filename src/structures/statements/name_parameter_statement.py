#TODO

from src.exceptions.error import Error
from src.utils.name_validator import is_valid_name
from src.utils.name_resolver import check_name_type as check_name
from src.enums.name_type import NameType
from src.structures.statements.base_statement import BaseStatement


class NameParameterStatement(BaseStatement):
    def parse(self):
        self.check_for_error()
        self.function.parameters.append(self.arguments[0])
        self.function.parameters_with_names.append(self.arguments[1])

    def check_for_error(self):
        if len(self.arguments) != 2:
            raise Error(f"Wrong number of arguments for name_parameter: expected 2, got {len(self.arguments)} - line {self.line}")
        if not is_valid_name(self.arguments[0]):
            raise Error(f"Wrong parameter name '{self.arguments[0]}' - line {self.line}")
        if check_name(self.arguments[0], self.parsed_program, self.function) != NameType.NOT_FOUND:
            raise Error(f"Multiple name '{self.arguments[0]}' - line {self.line}")
        if check_name(self.arguments[1], self.parsed_program, self.function) != NameType.INT_NUM:
            raise Error(f"Wrong second argument for name_parameter '{self.arguments[1]}', it must be an integer - line {self.line}")
        if self.arguments[1] < 0 or self.arguments[1] >= self.function.parameter_count or self.arguments[1] in self.function.parameters_with_names:
            raise Error(f"Wrong second argument for name_parameter '{self.arguments[1]}' - line {self.line}")
    def generate_nasm_code(self):
        return f"%define {self.arguments[0]} parameter_{self.arguments[1]}\n"
