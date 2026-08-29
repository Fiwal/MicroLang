from enum import Enum
from src.stack import Stack
from src.utils import is_valid_name


class Function:
    def __init__(self, name, parameters_num):
        self.name = name
        self.parameter_count = parameters_num
        self.local_variables = []
        self.parameters = []
        self.tokens = []
        self.if_counter = 0
        self.if_stack = Stack()
        self.loop_counter = 0
        self.loop_stack = Stack()
        self.if_and_loop_stack = Stack()

    class NameType(Enum):
        FUNCTION = 1
        INT_VARIABLE = 2
        INT_NUM = 3
        STRING_VARIABLE = 4
        PARAMETER = 5
        RETURN_VALUE = 6
        NOT_FOUND = 7

    def parse_function(self, program):
        for token in self.tokens:
            match token["instruction"]:
                case "int":
                    if not len(token["arguments"]) in [1, 2]:
                        raise SyntaxError(f"Wrong number of arguments for int: expected 1 or 2, got {len(token['arguments'])} - line {token['line_number']}")

                    if not is_valid_name(token["arguments"][0]):
                        raise SyntaxError(f"Wrong variable name '{token["arguments"][0]}' - line {token['line_number']}")

                    if not self.check_name(token["arguments"][0], program) == self.NameType.NOT_FOUND:
                        raise SyntaxError(f"Multiple name '{token["arguments"][0]}' - line {token['line_number']}")

                    if len(token["arguments"]) == 2 and not self.check_name(token["arguments"][1], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong second argument for int '{token["arguments"][1]}' - line {token['line_number']}")

                    self.local_variables.append(token["arguments"][0])
                    token["arguments"].append(len(self.local_variables))

                case "set" | "add" | "sub" | "mul"| "div" | "mod":
                    if len(token["arguments"]) != 2:
                        raise SyntaxError(f"Wrong number of arguments for {token["instruction"]}: expected 2, got {len(token['arguments'])} - line {token['line_number']}")

                    if not self.check_name(token["arguments"][0], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER]:
                        raise SyntaxError(f"Wrong first argument for {token["instruction"]} '{token["arguments"][0]}' - line {token['line_number']}")

                    if not self.check_name(token["arguments"][1], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong argument '{token["arguments"][1]}' - line {token['line_number']}")

                case "print_int" | "input_int":
                    if not len(token["arguments"]) == 1:
                        raise SyntaxError(f"Wrong number of arguments for {token["instruction"]}: expected 1, got {len(token['arguments'])} - line {token['line_number']}")

                    name_type = self.check_name(token["arguments"][0], program)

                    if not name_type in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong argument '{token["arguments"][0]}' - line {token['line_number']}")

                    if token["instruction"] == "input_int" and name_type not in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER]:
                        raise SyntaxError(f"Wrong argument '{token["arguments"][0]}' - line {token['line_number']}")

                case "print":
                    if not len(token["arguments"]) == 1:
                        raise SyntaxError(f"Wrong number of arguments for print: expected 1, got {len(token['arguments'])} - line {token['line_number']}")

                    if not self.check_name(token["arguments"][0], program) == self.NameType.STRING_VARIABLE:
                        raise SyntaxError(f"Wrong argument for print '{token["arguments"][0]}', it must be a string variable - line {token['line_number']}")

                case "return":
                    if not len(token["arguments"]) in [0, 1]:
                        raise SyntaxError(f"Wrong number of arguments for return: expected 0 or 1, got {len(token['arguments'])} - line {token['line_number']}")

                    if not len(token["arguments"]) == 0 and not self.check_name(token["arguments"][0], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong argument '{token["arguments"][0]}' - line {token['line_number']}")

                case "IF":
                    if not len(token["arguments"]) == 3:
                        raise SyntaxError(f"Wrong number of arguments for IF: expected 3, got {len(token['arguments'])} - line {token['line_number']}")

                    if not self.check_name(token["arguments"][0], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong first argument for IF '{token["arguments"][0]}' - line {token['line_number']}")

                    if not token["arguments"][1] in ["==", "!=", "<", ">", "<=", ">="]:
                        raise SyntaxError(f"Wrong second argument for IF '{token["arguments"][1]}', it must be a comparison operator - line {token['line_number']}")

                    if not self.check_name(token["arguments"][2], program) in [self.NameType.INT_VARIABLE, self.NameType.PARAMETER, self.NameType.RETURN_VALUE, self.NameType.INT_NUM]:
                        raise SyntaxError(f"Wrong third argument for IF '{token["arguments"][2]}' - line {token['line_number']}")

                    self.if_stack.push({"else": False, "id": self.if_counter})
                    token["arguments"].append(self.if_counter)

                    self.if_counter += 1
                    self.if_and_loop_stack.push("if")

                case "ELSE":
                    if not len(token["arguments"]) == 0:
                        raise SyntaxError(f"Wrong number of arguments for ELSE: expected 0, got {len(token['arguments'])} - line {token['line_number']}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "loop":
                        raise SyntaxError(f"ELSE without matching IF - line {token['line_number']}")

                    current_if = self.if_stack.pop()
                    if current_if["else"]:
                        raise SyntaxError(f"Duplicate ELSE for the same IF - line {token['line_number']}")
                    current_if["else"] = True
                    token["arguments"].append(current_if["id"])

                    self.if_stack.push(current_if)

                case "ENDIF":
                    if not len(token["arguments"]) == 0:
                        raise SyntaxError(f"Wrong number of arguments for ENDIF: expected 0, got {len(token['arguments'])} - line {token['line_number']}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "loop":
                        raise SyntaxError(f"ENDIF without matching IF - line {token['line_number']}")

                    current_if = self.if_stack.pop()
                    token["arguments"].append(current_if["id"])
                    if not current_if["else"]:
                        token["arguments"].append("no else")

                    self.if_and_loop_stack.pop()

                case "LOOP":
                    if not len(token["arguments"]) == 0:
                        raise SyntaxError(f"Wrong number of arguments for LOOP: expected 0, got {len(token['arguments'])} - line {token['line_number']}")

                    self.loop_stack.push({"id": self.loop_counter})
                    token["arguments"].append(self.loop_counter)

                    self.loop_counter += 1
                    self.if_and_loop_stack.push("loop")

                case "break":
                    if not len(token["arguments"]) == 0:
                        raise SyntaxError(f"Wrong number of arguments for break: expected 0, got {len(token['arguments'])} - line {token['line_number']}")

                    if self.loop_stack.is_empty():
                        raise SyntaxError(f"break outside of LOOP - line {token['line_number']}")

                    current_loop = self.loop_stack.top()
                    token["arguments"].append(current_loop["id"])

                case "ENDLOOP":
                    if not len(token["arguments"]) == 0:
                        raise SyntaxError(f"Wrong number of arguments for ENDLOOP: expected 0, got {len(token['arguments'])} - line {token['line_number']}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "if":
                        raise SyntaxError(f"ENDLOOP without matching LOOP - line {token['line_number']}")

                    current_loop = self.loop_stack.pop()
                    token["arguments"].append(current_loop["id"])
                    self.if_and_loop_stack.pop()


                #TODO: nazwa, numer
                case "name_parameter":
                    self.parameters.append(token["arguments"][0])

                #TODO: dużo
                case _:
                    pass

    def check_name(self, name, program):
        if isinstance(name, int):
            return self.NameType.INT_NUM

        for function in program["functions"]:
            if function.name == name:
                return self.NameType.FUNCTION

        for var in program["initialized_global_variables"]:
            if var["name"] == name:
                if var["type"] == "int":
                    return self.NameType.INT_VARIABLE
                if var["type"] == "string":
                    return self.NameType.STRING_VARIABLE

        for var in program["uninitialized_global_variables"]:
            if var["name"] == name:
                if var["type"] == "int":
                    return self.NameType.INT_VARIABLE

        for var in self.local_variables:
            if var == name:
                return self.NameType.INT_VARIABLE

        for parameter in self.parameters:
            if parameter == name:
                return self.NameType.PARAMETER

        for i in range(0, 6):
            if name == f"parameter_{i}":
                return self.NameType.PARAMETER

        if name == "return_value":
            return self.NameType.RETURN_VALUE

        return self.NameType.NOT_FOUND
