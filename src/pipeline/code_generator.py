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

            for statement in function.statements_list:
                self.add_assembly_code(statement.generate_nasm_code())

            self.add_assembly_code(".end:\n")

            for i in range(function.parameter_count):
                self.add_assembly_code(f"%undef parameter_{i}\n")

            for local_var in function.local_variables:
                self.add_assembly_code(f"%undef {local_var}\n")

            for parameter_name in function.parameters:
                self.add_assembly_code(f"%undef {parameter_name}\n")

            self.add_assembly_code("mov rsp, rbp\npop rbp\nret\n")


    def add_assembly_code(self, code):
        self.nasm_code += code

    def save_assembly(self):
        with open(self.output_file, "w") as file:
            file.write(self.nasm_code)
