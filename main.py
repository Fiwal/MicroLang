import subprocess
import time
from functools import wraps


def print_msg_and_measure_time(msg):
    def print_msg_and_measure_time_real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            start = time.perf_counter()
            return_value = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Done - {((end - start) * 1000):.5f}ms")
            return return_value
        return wrapper
    return print_msg_and_measure_time_real_decorator


def is_valid_name(name):
    keywords = ["FN", "ENDFN", "return", "name_parameter", "IF", "ELSE", "ENDIF", "LOOP", "ENDLOOP",
                "break", "int", "string", "print", "print_int", "input_int", "add", "sub", "mul",
                "div", "mod", "set", "return_value"]

    if name in keywords:
        return False

    if not name.isidentifier():
        return False

    return True


class Lexer:
    def __init__(self, source_path):
        self.source_path = source_path
        self.source = open(source_path).read()
        self.buffer = ""
        self.tokens = []
        self.current_instruction_name = ""
        self.instruction_found = False
        self.instruction_start_detected = False
        self.current_arguments_list = []
        self.in_comment = False
        self.line_number = 1
        self.instruction_start_line_number = 1
        self.in_quote = False

    @print_msg_and_measure_time("Tokenizing...")
    def tokenize(self):
        for char in self.source:
            if char == "#" and not self.in_comment and not self.in_quote:
                self.in_comment = True
            elif char == "\n" and self.in_comment:
                self.in_comment = False

            if char in ["\"", "`"] and not self.in_comment:
                self.in_quote = not self.in_quote
                char = "`"

            if self.in_quote:
                if self.buffer != "" and char == "`":
                    raise SyntaxError(f"Wrong quote position - line {self.line_number}")
                self.buffer += char

            if char == "\n":
                self.line_number += 1

            if not char.isspace() and not self.in_comment and not self.in_quote:
                match char:
                    case ":":
                        self.capture_instruction_name()
                    case ",":
                        self.capture_argument()
                    case ";":
                        self.finalize_instruction()
                    case _:
                        if not self.buffer == "" and self.buffer[-1] == "`":
                            raise SyntaxError(f"Unexpected character after closing quote - line {self.line_number}")

                        if not self.instruction_start_detected:
                            self.instruction_start_line_number = self.line_number
                            self.instruction_start_detected = True

                        self.buffer += char

        if self.in_quote:
            raise SyntaxError("Unclosed quote")

        return self.tokens

    def capture_instruction_name(self):
        if self.instruction_found:
            raise SyntaxError(f"Duplicate ':' in instruction - line {self.line_number}")

        self.instruction_found = True
        self.current_instruction_name = self.buffer
        self.clear_buffer()

    def capture_argument(self):
        if not self.instruction_found:
            raise SyntaxError(f"Argument found before instruction - line {self.line_number}")

        try:
            self.current_arguments_list.append(int(self.buffer))
        except ValueError:
            try:
                self.current_arguments_list.append(float(self.buffer))
            except ValueError:
                self.current_arguments_list.append(self.buffer)
        self.clear_buffer()

    def finalize_instruction(self):

        if not self.instruction_found:
            self.capture_instruction_name()
        else:
            self.capture_argument()

        self.instruction_start_detected = False

        self.tokens.append({"instruction": self.current_instruction_name, "arguments": self.current_arguments_list,
                            "line_number": self.instruction_start_line_number})
        self.current_instruction_name = ""
        self.current_arguments_list = []
        self.instruction_found = False

    def clear_buffer(self):
        self.buffer = ""


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("pop from empty stack")

    def top(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("top from empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


class Function:
    def __init__(self, name, parameters_num):
        self.name = name
        self.parameter_count = parameters_num
        self.local_variables_names = []
        self.parameters_names = []
        self.tokens = []
        self.if_counter = 0
        self.if_stack = Stack()
        self.loop_counter = 0
        self.loop_stack = Stack()
        self.if_and_loop_stack = Stack()


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
            raise SyntaxError(f"Parameter count must be an integer- line {token['line_number']}")

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

        match token["instruction"]:
            case "IF":
                function.if_stack.push({"else": False, "id": function.if_counter})
                token["arguments"].append(function.if_counter)

                function.if_counter += 1
                function.if_and_loop_stack.push("if")

            case "ELSE":
                if function.if_and_loop_stack.is_empty() or function.if_and_loop_stack.top() == "loop":
                    raise SyntaxError(f"ELSE without matching IF - line {token['line_number']}")

                current_if = function.if_stack.pop()
                if current_if["else"]:
                    raise SyntaxError(f"Duplicate ELSE for the same IF - line {token['line_number']}")
                current_if["else"] = True
                token["arguments"].append(current_if["id"])

                function.if_stack.push(current_if)

            case "ENDIF":
                if function.if_and_loop_stack.is_empty() or function.if_and_loop_stack.top() == "loop":
                    raise SyntaxError(f"ENDIF without matching IF - line {token['line_number']}")

                current_if = function.if_stack.pop()
                token["arguments"].append(current_if["id"])
                if not current_if["else"]:
                    token["arguments"].append("no else")

                function.if_and_loop_stack.pop()

            case "LOOP":
                function.loop_stack.push({"id": function.loop_counter})
                token["arguments"].append(function.loop_counter)

                function.loop_counter += 1
                function.if_and_loop_stack.push("loop")

            case "break":
                if function.loop_stack.is_empty():
                    raise SyntaxError(f"break outside of LOOP - line {token['line_number']}")

                current_loop = function.loop_stack.top()
                token["arguments"].append(current_loop["id"])

            case "ENDLOOP":
                if function.if_and_loop_stack.is_empty() or function.if_and_loop_stack.top() == "if":
                    raise SyntaxError(f"ENDLOOP without matching LOOP - line {token['line_number']}")

                current_loop = function.loop_stack.pop()
                token["arguments"].append(current_loop["id"])
                function.if_and_loop_stack.pop()

            case "int":
                function.local_variables_names.append(token["arguments"][0])
                token["arguments"].append(len(function.local_variables_names))

            case "name_parameter":
                function.parameters_names.append(token["arguments"][0])

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

class Compiler:
    def __init__(self, program):
        self.program = program
        self.assembly_code = ""
        self.arguments_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
        self.comparison_jumps = {"==": "ne", "!=": "e", "<": "ge", "<=": "g", ">": "le", ">=": "l"}
        self.output_file = "output.asm"

    @print_msg_and_measure_time("Compiling...")
    def compile(self):
        self.section_data()
        self.section_bss()
        self.section_text()
        self.save_assembly()
        self.build_executable()

    def section_data(self):
        self.add_assembly_code("section .data\n")

        self.add_assembly_code("fmt_int? db \"%lld\", 0\n")

        for var in self.program["initialized_global_variables"]:
            if var["type"] == "int":
                self.add_assembly_code(
                    f"{var["name"]}? dq {var["value"]}\n"
                    f"%define {var["name"]} [{var["name"]}?]\n")
            if var["type"] == "string":
                self.add_assembly_code(f"{var["name"]} db {var["value"]}, 0\n")

    def section_bss(self):
        self.add_assembly_code("section .bss\n")

        for var in self.program["uninitialized_global_variables"]:
            if var["type"] == "int":
                self.add_assembly_code(
                    f"{var["name"]}? resq 1\n"
                    f"%define {var["name"]} [{var["name"]}?]\n")

    def section_text(self):
        self.add_assembly_code(
            "section .text\n"
            "global main\n"
            "extern printf\n"
            "extern scanf\n"
            "%define return_value rax\n")

        for function in self.program["functions"]:
            self.add_assembly_code(
                f"{function.name}:\n"
                "push rbp\n"
                "mov rbp, rsp\n")

            if ((len(function.local_variables_names) + function.parameter_count) * 8) % 16 == 0:
                self.add_assembly_code(f"sub rsp, {(len(function.local_variables_names) + function.parameter_count) * 8}\n")
            else:
                self.add_assembly_code(f"sub rsp, {(len(function.local_variables_names) + function.parameter_count) * 8 + 8}\n")

            for i in range(function.parameter_count):
                self.add_assembly_code(f"%define parameter_{i} [rbp-{(i+1)*8}]\n")
                self.add_assembly_code(f"mov parameter_{i}, {self.arguments_registers[i]}\n")

            for token in function.tokens:
                self.change_token_to_assembly(token, function)

            self.add_assembly_code(".end:\n")

            for i in range(function.parameter_count):
                self.add_assembly_code(f"%undef parameter_{i}\n")

            for local_var in function.local_variables_names:
                self.add_assembly_code(f"%undef {local_var}\n")

            for parameter_name in function.parameters_names:
                self.add_assembly_code(f"%undef {parameter_name}\n")

            self.add_assembly_code("mov rsp, rbp\npop rbp\nret\n")

    def change_token_to_assembly(self, token, function):
        match token["instruction"]:
            case "int":
                if len(token["arguments"]) == 2:
                    self.add_assembly_code(f"%define {token["arguments"][0]} [rbp-{(token["arguments"][1] + function.parameter_count) * 8}]\n")
                elif len(token["arguments"]) == 3:
                    self.add_assembly_code(
                        f"%define {token["arguments"][0]} [rbp-{(token["arguments"][2] + function.parameter_count) * 8}]\n"
                        f"mov rax, {token["arguments"][1]}\n"
                        f"mov {token["arguments"][0]}, rax\n")

            case "set":
                self.add_assembly_code(
                    f"mov rax, {token["arguments"][1]}\n"
                    f"mov {token["arguments"][0]}, rax\n")

            case "add":
                self.add_assembly_code(
                    f"mov rax, {token["arguments"][1]}\n"
                    f"add {token["arguments"][0]}, rax\n")

            case "sub":
                self.add_assembly_code(
                    f"mov rax, {token["arguments"][1]}\n"
                    f"sub {token["arguments"][0]}, rax\n")

            case "mul":
                self.add_assembly_code(
                    f"mov rax, {token["arguments"][0]}\n"
                    f"imul rax, {token["arguments"][1]}\n"
                    f"mov {token["arguments"][0]}, rax\n")

            case "div":
                self.add_assembly_code(
                    f"mov r11, {token["arguments"][1]}\n"
                    f"mov rax, {token["arguments"][0]}\n"
                    "cqo\n"
                    "idiv r11\n"
                    f"mov {token["arguments"][0]}, rax\n")

            case "mod":
                self.add_assembly_code(
                    f"mov r11, {token["arguments"][1]}\n"
                    f"mov rax, {token["arguments"][0]}\n"
                    "cqo\n"
                    "idiv r11\n"
                    f"mov {token["arguments"][0]}, rdx\n")

            case "print_int":
                self.add_assembly_code(
                    "mov rdi, fmt_int?\n"
                    f"mov rsi, {token["arguments"][0]}\n"
                    "xor rax, rax\n"
                    "call printf\n")

            case "input_int":
                self.add_assembly_code(
                    "mov rdi, fmt_int?\n"
                    f"lea rsi, {token["arguments"][0]}\n"
                    "xor rax, rax\n"
                    "call scanf\n")

            case "print":
                self.add_assembly_code(
                    f"mov rdi, {token["arguments"][0]}\n"
                    "xor rax, rax\n"
                    "call printf\n")

            case "return":
                if len(token["arguments"]) == 1:
                    self.add_assembly_code(f"mov rax, {token["arguments"][0]}\n")
                self.add_assembly_code("jmp .end\n")

            case "IF":
                self.add_assembly_code(
                    f"mov rax, {token["arguments"][2]}\n"
                    f"cmp {token["arguments"][0]}, rax\n"
                    f"j{self.comparison_jumps[token["arguments"][1]]} .else_{token["arguments"][3]}\n")

            case "ELSE":
                self.add_assembly_code(
                    f"jmp .endif_{token["arguments"][0]}\n"
                    f".else_{token["arguments"][0]}:\n")

            case "ENDIF":
                if len(token["arguments"]) == 2 and token["arguments"][1] == "no else":
                    self.add_assembly_code(f".else_{token["arguments"][0]}:\n")
                else:
                    self.add_assembly_code(f".endif_{token["arguments"][0]}:\n")

            case "LOOP":
                self.add_assembly_code(f".loop_{token["arguments"][0]}:\n")

            case "break":
                self.add_assembly_code(f"jmp .endloop_{token["arguments"][0]}\n")

            case "ENDLOOP":
                self.add_assembly_code(
                    f"jmp .loop_{token["arguments"][0]}\n"
                    f".endloop_{token["arguments"][0]}:\n")

            case "name_parameter":
                self.add_assembly_code(f"%define {token["arguments"][0]} parameter_{token["arguments"][1]}\n")

            case _:
                for k in range(len(token["arguments"])):
                    self.add_assembly_code(f"mov {self.arguments_registers[k]}, {token["arguments"][k]}\n")
                self.add_assembly_code(f"call {token["instruction"]}\n")

    def add_assembly_code(self, code):
        self.assembly_code += code

    def save_assembly(self):
        with open(self.output_file, "w") as file:
            file.write(self.assembly_code)

    def build_executable(self):
        subprocess.run(["nasm", "-f", "elf64", "-g", "-F", "dwarf", self.output_file, "-o", "program.o"], check=True)
        subprocess.run(["gcc", "-no-pie", "program.o", "-o", "program", "-lc"], check=True)


if __name__ == "__main__":
    lexer = Lexer("code.txt")
    try:
        parser = Parser(lexer.tokenize())
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        exit(1)
    compiler = Compiler(parser.parse())
    compiler.compile()