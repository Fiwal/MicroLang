from src.exceptions import Error
from src.structures.function import Function
from src.enums.name_type import NameType
from src.utils.decorators import measure_time
from src.utils.name_validator import is_valid_name
from src.utils.name_resolver import check_name_type


class Parser:
    def __init__(self, given_tokens):
        self.tokens = given_tokens
        self.parsed_program = {"functions": [], "uninitialized_global_variables": [], "initialized_global_variables": []}
        self.in_function_body = False

    @measure_time("Parsing...")
    def parse(self):
        for token in self.tokens:
            if token.name == "FN":
                self.start_function(token)
            elif token.name == "ENDFN":
                self.end_function(token)
            elif self.in_function_body:
                self.append_instruction(token)
            else:
                self.append_global_variables(token)

        if self.in_function_body:
            raise Error(f"Unclosed function '{self.get_current_function().name}'")

        self.parse_functions()

        return self.parsed_program

    def start_function(self, token):
        if self.in_function_body:
            raise Error(f"Function cannot be inside another function - line {token.line}")

        if len(token.arguments) != 2:
            raise Error(f"Wrong number of arguments for FN: expected 2, got {len(token.arguments)} - line {token.line}")

        if check_name_type(token.arguments[0], self.parsed_program) != NameType.NOT_FOUND:
            raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")

        if not is_valid_name(token.arguments[0]):
            raise Error(f"Wrong function name '{token.arguments[0]}' - line {token.line}")

        if not isinstance(token.arguments[1], int):
            raise Error(f"Parameter count must be an integer - line {token.line}")

        if token.arguments[1] < 0 or token.arguments[1] > 6:
            raise Error(f"Parameter count must be between 0 and 6 (inclusive) - line {token.line}")

        self.parsed_program["functions"].append(Function(token.arguments[0], token.arguments[1]))
        self.in_function_body = True

    def end_function(self, token):
        if not self.in_function_body:
            raise Error(f"ENDFN without matching FN - line {token.line}")

        if len(token.arguments) != 0:
            raise Error(f"Wrong number of arguments for ENDFN: expected 0, got {len(token.arguments)} - line {token.line}")

        function = self.get_current_function()

        if function.if_stack.size() > 0:
            raise Error(f"Unclosed IF in function '{self.parsed_program['functions'][-1].name}'")

        if function.loop_stack.size() > 0:
            raise Error(f"Unclosed LOOP in function '{self.parsed_program['functions'][-1].name}'")

        self.in_function_body = False

    def append_instruction(self, token):
        function = self.get_current_function()

        function.tokens.append(token)

    def append_global_variables(self, token):
        def check_first_argument():
            if not is_valid_name(token.arguments[0]):
                raise Error(f"Wrong variable name '{token.arguments[0]}' - line {token.line}")
            if check_name_type(token.arguments[0], self.parsed_program) != NameType.NOT_FOUND:
                raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")

        match token.name:
            case "int":
                match len(token.arguments):
                    case 1:
                        check_first_argument()
                        self.parsed_program["uninitialized_global_variables"].append({"type": "int", "name": token.arguments[0]})

                    case 2:
                        check_first_argument()
                        if not isinstance(token.arguments[1], int):
                            raise Error(f"The value of the global int variable must be an integer, not an another variable or a float - line {token.line}")

                        self.parsed_program["initialized_global_variables"].append({"type": "int", "name": token.arguments[0], "value": token.arguments[1]})

                    case _:
                        raise Error(f"Wrong number of arguments for int: expected 1 or 2, got {len(token.arguments)} - line {token.line}")

            case "string":
                if len(token.arguments) != 2:
                    raise Error(f"Wrong number of arguments for string: expected  2, got {len(token.arguments)} - line {token.line}")

                check_first_argument()
                if not isinstance(token.arguments[1], str) or (token.arguments[1].count("`") != 2) or token.arguments[1][0] != "`" or token.arguments[1][-1] != "`":
                    raise Error(f"The value of string must be in quotes, not be another variable or number - line {token.line}")

                self.parsed_program["initialized_global_variables"].append({"type": "string", "name": token.arguments[0], "value": token.arguments[1]})

            case _:
                raise Error(f"Only 'int' and 'string' instructions are allowed outside a function - line {token.line}")

    def get_current_function(self):
        return self.parsed_program["functions"][-1]

    def parse_functions(self):
        for function in self.parsed_program["functions"]:
            function.parse_function(self.parsed_program)
