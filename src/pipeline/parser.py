from src.exceptions import Error
from src.structures.function import Function
from src.structures.global_var import GlobalVar
from src.structures.program_struct import ProgramStruct
from src.enums import NameType, VarType
from src.utils import check_name_type, is_valid_name, measure_time


class Parser:
    def __init__(self, given_tokens):
        self.tokens = given_tokens
        self.program = ProgramStruct()
        self.in_function_body = False
        self.is_main_function = False

    @measure_time("Parsing...")
    def parse(self):
        for token in self.tokens:
            self.process_token(token)
        if self.in_function_body:
            raise Error(f"Unclosed function '{self.get_current_function().name}'")
        if not self.is_main_function:
            raise Error(f"No function 'main' in code")
        self.parse_functions()
        self.add_dollar_signs()
        return self.program

    def process_token(self, token):
        if token.name == "fn":
            self.start_function(token)
        elif token.name == "endfn":
            self.end_function(token)
        elif self.in_function_body:
            self.append_instruction(token)
        else:
            self.append_global_variables(token)

    def start_function(self, token):
        if self.in_function_body:
            raise Error(f"Function cannot be inside another function - line {token.line}")
        if len(token.arguments) != 2:
            raise Error(f"Wrong number of arguments for fn: expected 2, got {len(token.arguments)} - line {token.line}")
        if token.connected_tokens:
            raise Error(f"Cannot connect instructions with fn - line {token.connected_tokens[0].line}")
        if check_name_type(token.arguments[0], self.program) != NameType.NOT_FOUND:
            raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")
        if not is_valid_name(token.arguments[0]):
            raise Error(f"Wrong function name '{token.arguments[0]}' - line {token.line}")
        if not isinstance(token.arguments[1], int):
            raise Error(f"Parameter count must be an integer - line {token.line}")
        if token.arguments[0] == "main":
            self.is_main_function = True
        self.program.functions.append(Function(token.arguments[0], token.arguments[1]))
        self.in_function_body = True

    def end_function(self, token):
        if not self.in_function_body:
            raise Error(f"endfn without matching fn - line {token.line}")
        if len(token.arguments) != 0:
            raise Error(f"Wrong number of arguments for endfn: expected 0, got {len(token.arguments)} - line {token.line}")
        if token.connected_tokens:
            raise Error(f"Cannot connect instructions with endfn - line {token.connected_tokens[0].line}")
        self.in_function_body = False

    def append_instruction(self, token):
        self.get_current_function().tokens.append(token)

    def append_global_variables(self, token):
        match token.name:
            case "int":
                self.append_int_global_var(token)
            case "string":
                self.append_string_global_var(token)
            case _:
                raise Error(f"Only 'int' and 'string' instructions are allowed outside a function - line {token.line}")

    def append_int_global_var(self, token):
        if token.connected_tokens:
            raise Error(f"Cannot connect instructions with int - line {token.connected_tokens[0].line}")
        match len(token.arguments):
            case 1:
                self.check_first_global_var_argument(token)
                self.program.uninitialized_global_variables.append(GlobalVar(token.arguments[0], VarType.INTEGER))
            case 2:
                self.check_first_global_var_argument(token)
                if not isinstance(token.arguments[1], int):
                    raise Error(f"The value of a global int variable must be an integer, not another variable or a float - line {token.line}")
                self.program.initialized_global_variables.append(GlobalVar(token.arguments[0], VarType.INTEGER, token.arguments[1]))
            case _:
                raise Error(f"Wrong number of arguments for int: expected 1 or 2, got {len(token.arguments)} - line {token.line}")

    def append_string_global_var(self, token):
        if token.connected_tokens:
            raise Error(f"Cannot connect instructions with string - line {token.connected_tokens[0].line}")
        if len(token.arguments) != 2:
            raise Error(f"Wrong number of arguments for string: expected 2, got {len(token.arguments)} - line {token.line}")
        self.check_first_global_var_argument(token)
        if not isinstance(token.arguments[1], str) or (token.arguments[1].count("`") != 2) or token.arguments[1][0] != "`" or token.arguments[1][-1] != "`":
            raise Error(f"The value of a string variable must be a quoted string - line {token.line}")
        self.program.initialized_global_variables.append(GlobalVar(token.arguments[0], VarType.STRING, token.arguments[1]))

    def check_first_global_var_argument(self, token):
        if not is_valid_name(token.arguments[0]):
            raise Error(f"Wrong variable name '{token.arguments[0]}' - line {token.line}")
        if check_name_type(token.arguments[0], self.program) != NameType.NOT_FOUND:
            raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")

    def get_current_function(self):
        return self.program.functions[-1]

    def parse_functions(self):
        for function in self.program.functions:
            function.parse_function(self.program)

    def add_dollar_signs(self):
        for function in self.program.functions:
            function.add_dollar_signs()
        for var in self.program.initialized_global_variables:
            var.name += "$"
        for var in self.program.uninitialized_global_variables:
            var.name += "$"
