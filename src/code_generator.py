from src.utils.decorators import measure_time

class CodeGenerator:
    def __init__(self, parsed_program, output_file):
        self.parsed_program = parsed_program
        self.nasm_code = ""
        self.arguments_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
        self.comparison_jumps = {"==": "ne", "!=": "e", "<": "ge", "<=": "g", ">": "le", ">=": "l"}
        self.output_file = output_file

    @measure_time("NASM code generating...")
    def generate_nasm_code(self):
        self.section_data()
        self.section_bss()
        self.section_text()
        self.save_assembly()

    def section_data(self):
        self.add_assembly_code("section .data\n")

        self.add_assembly_code("fmt_int? db \"%lld\", 0\n")

        for var in self.parsed_program["initialized_global_variables"]:
            if var["type"] == "int":
                self.add_assembly_code(
                    f"{var["name"]}? dq {var["value"]}\n"
                    f"%define {var["name"]} [{var["name"]}?]\n")
            if var["type"] == "string":
                self.add_assembly_code(f"{var["name"]} db {var["value"]}, 0\n")

    def section_bss(self):
        self.add_assembly_code("section .bss\n")

        for var in self.parsed_program["uninitialized_global_variables"]:
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

        for function in self.parsed_program["functions"]:
            self.add_assembly_code(
                f"{function.name}:\n"
                "push rbp\n"
                "mov rbp, rsp\n")

            if ((len(function.local_variables) + function.parameter_count) * 8) % 16 == 0:
                self.add_assembly_code(f"sub rsp, {(len(function.local_variables) + function.parameter_count) * 8}\n")
            else:
                self.add_assembly_code(f"sub rsp, {(len(function.local_variables) + function.parameter_count) * 8 + 8}\n")

            for i in range(function.parameter_count):
                self.add_assembly_code(f"%define parameter_{i} [rbp-{(i+1)*8}]\n")
                self.add_assembly_code(f"mov parameter_{i}, {self.arguments_registers[i]}\n")

            for token in function.tokens:
                self.change_token_to_assembly(token, function)

            self.add_assembly_code(".end:\n")

            for i in range(function.parameter_count):
                self.add_assembly_code(f"%undef parameter_{i}\n")

            for local_var in function.local_variables:
                self.add_assembly_code(f"%undef {local_var}\n")

            for parameter_name in function.parameters:
                self.add_assembly_code(f"%undef {parameter_name}\n")

            self.add_assembly_code("mov rsp, rbp\npop rbp\nret\n")

    def change_token_to_assembly(self, token, function):
        match token.name:
            case "int":
                if len(token.arguments) == 2:
                    self.add_assembly_code(f"%define {token.arguments[0]} [rbp-{(token.arguments[1] + function.parameter_count) * 8}]\n")
                elif len(token.arguments) == 3:
                    self.add_assembly_code(
                        f"%define {token.arguments[0]} [rbp-{(token.arguments[2] + function.parameter_count) * 8}]\n"
                        f"mov rax, {token.arguments[1]}\n"
                        f"mov {token.arguments[0]}, rax\n")

            case "set":
                self.add_assembly_code(
                    f"mov rax, {token.arguments[1]}\n"
                    f"mov {token.arguments[0]}, rax\n")

            case "add":
                self.add_assembly_code(
                    f"mov rax, {token.arguments[1]}\n"
                    f"add {token.arguments[0]}, rax\n")

            case "sub":
                self.add_assembly_code(
                    f"mov rax, {token.arguments[1]}\n"
                    f"sub {token.arguments[0]}, rax\n")

            case "mul":
                self.add_assembly_code(
                    f"mov rax, {token.arguments[0]}\n"
                    f"imul rax, {token.arguments[1]}\n"
                    f"mov {token.arguments[0]}, rax\n")

            case "div":
                self.add_assembly_code(
                    f"mov r11, {token.arguments[1]}\n"
                    f"mov rax, {token.arguments[0]}\n"
                    "cqo\n"
                    "idiv r11\n"
                    f"mov {token.arguments[0]}, rax\n")

            case "mod":
                self.add_assembly_code(
                    f"mov r11, {token.arguments[1]}\n"
                    f"mov rax, {token.arguments[0]}\n"
                    "cqo\n"
                    "idiv r11\n"
                    f"mov {token.arguments[0]}, rdx\n")

            case "print_int":
                self.add_assembly_code(
                    "mov rdi, fmt_int?\n"
                    f"mov rsi, {token.arguments[0]}\n"
                    "xor rax, rax\n"
                    "call printf\n")

            case "input_int":
                self.add_assembly_code(
                    "mov rdi, fmt_int?\n"
                    f"lea rsi, {token.arguments[0]}\n"
                    "xor rax, rax\n"
                    "call scanf\n")

            case "print":
                self.add_assembly_code(
                    f"mov rdi, {token.arguments[0]}\n"
                    "xor rax, rax\n"
                    "call printf\n")

            case "return":
                if len(token.arguments) == 1:
                    self.add_assembly_code(f"mov rax, {token.arguments[0]}\n")
                self.add_assembly_code("jmp .end\n")

            case "IF":
                self.add_assembly_code(
                    f"mov r8, {token.arguments[0]}\n"
                    f"mov r9, {token.arguments[2]}\n"
                    "cmp r8, r9\n"
                    f"j{self.comparison_jumps[token.arguments[1]]} .else_{token.arguments[3]}\n")

            case "ELSE":
                self.add_assembly_code(
                    f"jmp .endif_{token.arguments[0]}\n"
                    f".else_{token.arguments[0]}:\n")

            case "ENDIF":
                if len(token.arguments) == 2 and token.arguments[1] == "no else":
                    self.add_assembly_code(f".else_{token.arguments[0]}:\n")
                else:
                    self.add_assembly_code(f".endif_{token.arguments[0]}:\n")

            case "LOOP":
                self.add_assembly_code(f".loop_{token.arguments[0]}:\n")

            case "break":
                self.add_assembly_code(f"jmp .endloop_{token.arguments[0]}\n")

            case "ENDLOOP":
                self.add_assembly_code(
                    f"jmp .loop_{token.arguments[0]}\n"
                    f".endloop_{token.arguments[0]}:\n")

            case "name_parameter":
                self.add_assembly_code(f"%define {token.arguments[0]} parameter_{token.arguments[1]}\n")

            case _:
                for k in range(len(token.arguments)):
                    self.add_assembly_code(f"mov {self.arguments_registers[k]}, {token.arguments[k]}\n")
                self.add_assembly_code(f"call {token.name}\n")

    def add_assembly_code(self, code):
        self.nasm_code += code

    def save_assembly(self):
        with open(self.output_file, "w") as file:
            file.write(self.nasm_code)
