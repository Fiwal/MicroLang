from src.exceptions import Error
from src.utils.stack import Stack
from src.utils.name_validator import is_valid_name
from src.utils.name_resolver import check_name_type as check_name
from src.enums.name_type import NameType


class Function:
    def __init__(self, name, parameters_num):
        self.name = name
        self.parameter_count = parameters_num
        self.local_variables = []
        self.parameters = []
        self.parameters_with_names = []
        self.tokens = []
        self.if_counter = 0
        self.if_stack = Stack()
        self.loop_counter = 0
        self.loop_stack = Stack()
        self.if_and_loop_stack = Stack()

    def parse_function(self, parsed_program):
        for token in self.tokens:
            match token.name:
                case "int":
                    if not len(token.arguments) in [1, 2]:
                        raise Error(f"Wrong number of arguments for int: expected 1 or 2, got {len(token.line)} - line {token.line}")

                    if not is_valid_name(token.arguments[0]):
                        raise Error(f"Wrong variable name '{token.arguments[0]}' - line {token.line}")

                    if not check_name(token.arguments[0], parsed_program, self) == NameType.NOT_FOUND:
                        raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")

                    if len(token.arguments) == 2 and not check_name(token.arguments[1], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong second argument for int '{token.arguments[1]}' - line {token.line}")

                    self.local_variables.append(token.arguments[0])
                    token.arguments.append(len(self.local_variables))

                case "set" | "add" | "sub" | "mul"| "div" | "mod":
                    if len(token.arguments) != 2:
                        raise Error(f"Wrong number of arguments for {token.line}: expected 2, got {len(token.line)} - line {token.line}")

                    if not check_name(token.arguments[0], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER]:
                        raise Error(f"Wrong first argument for {token.line} '{token.line[0]}' - line {token.line}")

                    if not check_name(token.arguments[1], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong argument '{token.arguments[1]}' - line {token.line}")

                case "print_int" | "input_int":
                    if not len(token.arguments) == 1:
                        raise Error(f"Wrong number of arguments for {token.line}: expected 1, got {len(token.line)} - line {token.line}")

                    name_type = check_name(token.arguments[0], parsed_program, self)

                    if not name_type in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong argument '{token.arguments[0]}' - line {token.line}")

                    if token.name == "input_int" and name_type not in [NameType.INT_VARIABLE, NameType.PARAMETER]:
                        raise Error(f"Wrong argument '{token.arguments[0]}' - line {token.line}")

                case "print":
                    if not len(token.arguments) == 1:
                        raise Error(f"Wrong number of arguments for print: expected 1, got {len(token.line)} - line {token.line}")

                    if not check_name(token.arguments[0], parsed_program, self) == NameType.STRING_VARIABLE:
                        raise Error(f"Wrong argument for print '{token.arguments[0]}', it must be a string variable - line {token.line}")

                case "return":
                    if not len(token.arguments) in [0, 1]:
                        raise Error(f"Wrong number of arguments for return: expected 0 or 1, got {len(token.line)} - line {token.line}")

                    if not len(token.arguments) == 0 and not check_name(token.arguments[0], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong argument '{token.arguments[0]}' - line {token.line}")

                case "IF":
                    if not len(token.arguments) == 3:
                        raise Error(f"Wrong number of arguments for IF: expected 3, got {len(token.line)} - line {token.line}")

                    if not check_name(token.arguments[0], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong first argument for IF '{token.arguments[0]}' - line {token.line}")

                    if not token.arguments[1] in ["==", "!=", "<", ">", "<=", ">="]:
                        raise Error(f"Wrong second argument for IF '{token.arguments[1]}', it must be a comparison operator - line {token.line}")

                    if not check_name(token.arguments[2], parsed_program, self) in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                        raise Error(f"Wrong third argument for IF '{token.arguments[2]}' - line {token.line}")

                    self.if_stack.push({"else": False, "id": self.if_counter})
                    token.arguments.append(self.if_counter)

                    self.if_counter += 1
                    self.if_and_loop_stack.push("if")

                case "ELSE":
                    if not len(token.arguments) == 0:
                        raise Error(f"Wrong number of arguments for ELSE: expected 0, got {len(token.line)} - line {token.line}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "loop":
                        raise Error(f"ELSE without matching IF - line {token.line}")

                    current_if = self.if_stack.pop()
                    if current_if["else"]:
                        raise Error(f"Duplicate ELSE for the same IF - line {token.line}")
                    current_if["else"] = True
                    token.arguments.append(current_if["id"])

                    self.if_stack.push(current_if)

                case "ENDIF":
                    if not len(token.arguments) == 0:
                        raise Error(f"Wrong number of arguments for ENDIF: expected 0, got {len(token.line)} - line {token.line}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "loop":
                        raise Error(f"ENDIF without matching IF - line {token.line}")

                    current_if = self.if_stack.pop()
                    token.arguments.append(current_if["id"])
                    if not current_if["else"]:
                        token.arguments.append("no else")

                    self.if_and_loop_stack.pop()

                case "LOOP":
                    if not len(token.arguments) == 0:
                        raise Error(f"Wrong number of arguments for LOOP: expected 0, got {len(token.line)} - line {token.line}")

                    self.loop_stack.push({"id": self.loop_counter})
                    token.arguments.append(self.loop_counter)

                    self.loop_counter += 1
                    self.if_and_loop_stack.push("loop")

                case "break":
                    if not len(token.arguments) == 0:
                        raise Error(f"Wrong number of arguments for break: expected 0, got {len(token.line)} - line {token.line}")

                    if self.loop_stack.is_empty():
                        raise Error(f"break outside of LOOP - line {token.line}")

                    current_loop = self.loop_stack.top()
                    token.arguments.append(current_loop["id"])

                case "ENDLOOP":
                    if not len(token.arguments) == 0:
                        raise Error(f"Wrong number of arguments for ENDLOOP: expected 0, got {len(token.line)} - line {token.line}")

                    if self.if_and_loop_stack.is_empty() or self.if_and_loop_stack.top() == "if":
                        raise Error(f"ENDLOOP without matching LOOP - line {token.line}")

                    current_loop = self.loop_stack.pop()
                    token.arguments.append(current_loop["id"])
                    self.if_and_loop_stack.pop()

                case "name_parameter":
                    if len(token.arguments) != 2:
                        raise Error(f"Wrong number of arguments for name_parameter: expected 2, got {len(token.line)} - line {token.line}")
                    
                    if not is_valid_name(token.arguments[0]):
                        raise Error(f"Wrong parameter name '{token.arguments[0]}' - line {token.line}")

                    if not check_name(token.arguments[0], parsed_program, self) == NameType.NOT_FOUND:
                        raise Error(f"Multiple name '{token.arguments[0]}' - line {token.line}")

                    if not check_name(token.arguments[1], parsed_program, self) == NameType.INT_NUM:
                        raise Error(f"Wrong second argument for name_parameter '{token.arguments[1]}', it must be an integer - line {token.line}")

                    if token.arguments[1] < 0 or token.arguments[1] >= self.parameter_count or token.arguments[1] in self.parameters_with_names:
                        raise Error(f"Wrong second argument for name_parameter '{token.arguments[1]}' - line {token.line}")
                    
                    self.parameters.append(token.arguments[0])
                    self.parameters_with_names.append(token.arguments[1])

                case _:
                    if not check_name(token.name, parsed_program, self) == NameType.FUNCTION:
                        raise Error(f"Function '{token.name}' not found - line {token.line}")

                    for function in parsed_program["functions"]:
                        if function.name == token.name:
                            expected_num_of_arguments = function.parameter_count

                    if len(token.arguments) != expected_num_of_arguments:
                        raise Error(f"Wrong number of arguments for {token.name}: expected {expected_num_of_arguments}, got {len(token.line)} - line {token.line}")

                    for argument in token.arguments:
                        if check_name(argument, parsed_program, self) not in [NameType.INT_VARIABLE, NameType.PARAMETER, NameType.RETURN_VALUE, NameType.INT_NUM]:
                            raise Error(f"Wrong argument for {token.name} '{argument}' - line {token.line}")
