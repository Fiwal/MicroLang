from src.utils import print_msg_and_measure_time, is_valid_name
from src.function import Function


class Parser:
    def __init__(self, given_tokens):
        self.tokens = given_tokens
        self.program = {"functions": [], "uninitialized_global_variables": [], "initialized_global_variables": []}
        self.in_function_body = False

    @print_msg_and_measure_time("Parsing...")
    def parse(self):
        for token in self.tokens:
            if token["instruction"] == "FN":
                self.start_function(token)
            elif token["instruction"] == "ENDFN":
                self.end_function(token)
            elif self.in_function_body:
                self.append_instruction(token)
            else:
                self.append_global_variables(token)

        if self.in_function_body:
            raise SyntaxError(f"Unclosed function '{self.get_current_function().name}'")

        self.parse_functions()

        return self.program

    def start_function(self, token):
        if self.in_function_body:
            raise SyntaxError(f"Function cannot be inside another function - line {token['line_number']}")

        if len(token["arguments"]) != 2:
            raise SyntaxError(f"Wrong number of arguments for FN: expected 2, got {len(token["arguments"])} - line {token['line_number']}")

        self.check_if_multiple(token["arguments"][0], token)

        if not is_valid_name(token["arguments"][0]):
            raise SyntaxError(f"Wrong function name '{token["arguments"][0]}' - line {token['line_number']}")

        if not isinstance(token["arguments"][1], int):
            raise SyntaxError(f"Parameter count must be an integer - line {token['line_number']}")

        if token["arguments"][1] < 0 or token["arguments"][1] > 6:
            raise SyntaxError(f"Parameter count must be between 0 and 6 (inclusive) - line {token['line_number']}")

        self.program["functions"].append(Function(token["arguments"][0], token["arguments"][1]))
        self.in_function_body = True

    def end_function(self, token):
        if not self.in_function_body:
            raise SyntaxError(f"ENDFN without matching FN - line {token['line_number']}")

        if len(token["arguments"]) != 0:
            raise SyntaxError(f"Wrong number of arguments for ENDFN: expected 0, got {len(token["arguments"])} - line {token['line_number']}")

        function = self.get_current_function()

        if function.if_stack.size() > 0:
            raise SyntaxError(f"Unclosed IF in function '{self.program['functions'][-1].name}'")

        if function.loop_stack.size() > 0:
            raise SyntaxError(f"Unclosed LOOP in function '{self.program['functions'][-1].name}'")

        self.in_function_body = False

    def append_instruction(self, token):
        function = self.get_current_function()

        function.tokens.append(token)

    def append_global_variables(self, token):
        def check_first_argument():
            self.check_if_multiple(token["arguments"][0], token)
            if not is_valid_name(token["arguments"][0]):
                raise SyntaxError(f"Wrong variable name '{token["arguments"][0]}' - line {token['line_number']}")

        match token["instruction"]:
            case "int":
                match len(token["arguments"]):
                    case 1:
                        check_first_argument()
                        self.program["uninitialized_global_variables"].append({"type": "int", "name": token["arguments"][0]})

                    case 2:
                        check_first_argument()
                        if not isinstance(token["arguments"][1], int):
                            raise SyntaxError(f"The value of the global int variable must be an integer, not an another variable or a float - line {token['line_number']}")

                        self.program["initialized_global_variables"].append({"type": "int", "name": token["arguments"][0], "value": token["arguments"][1]})

                    case _:
                        raise SyntaxError(f"Wrong number of arguments for int: expected 1 or 2, got {len(token["arguments"])} - line {token['line_number']}")

            case "string":
                if len(token["arguments"]) != 2:
                    raise SyntaxError(f"Wrong number of arguments for string: expected  2, got {len(token["arguments"])} - line {token['line_number']}")

                check_first_argument()
                if (token["arguments"][1].count("`") != 2) or token["arguments"][1][0] != "`" or token["arguments"][1][-1] != "`":
                    raise SyntaxError(f"The value of string must be in quotes, not be another variable or number - line {token['line_number']}")

                self.program["initialized_global_variables"].append({"type": "string", "name": token["arguments"][0], "value": token["arguments"][1]})

            case _:
                raise SyntaxError(f"Only 'int' and 'string' instructions are allowed outside a function - line {token['line_number']}")

    def get_current_function(self):
        return self.program["functions"][-1]

    def check_if_multiple(self, name, token):
        for function in self.program["functions"]:
            if function.name == name:
                raise SyntaxError(f"Multiple name '{name}' - line {token['line_number']}")

        for var in self.program["initialized_global_variables"]:
            if var["name"] == name:
                raise SyntaxError(f"Multiple name '{name}' - line {token['line_number']}")

        for var in self.program["uninitialized_global_variables"]:
            if var["name"] == name:
                raise SyntaxError(f"Multiple name '{name}' - line {token['line_number']}")

    def parse_functions(self):
        for function in self.program["functions"]:
            function.parse_function(self.program)
