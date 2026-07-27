import subprocess


class Lexer:
    def __init__(self, source_path):
        self.source_path = source_path
        self.source = open(source_path).read()
        self.buffer = ""
        self.tokens = []
        self.current_instruction = ""
        self.has_instruction = False
        self.current_arguments = []
        self.is_comment = False
        self.current_line = 1

    def tokenize(self):
        for char in self.source:
            if char == "#" and not self.is_comment:
                self.is_comment = True
            elif char == "\n" and self.is_comment:
                self.is_comment = False

            if char == "\n":
                self.current_line += 1

            if not char.isspace() and not self.is_comment:
                match char:
                    case ":":
                        self.capture_instruction_name()
                    case ",":
                        self.capture_argument()
                    case ";":
                        self.finalize_instruction()
                    case _:
                        self.buffer += char
        return self.tokens

    def capture_instruction_name(self):
        self.has_instruction = True
        self.current_instruction = self.buffer
        self.clear_buffer()

    def capture_argument(self):
        try:
            self.current_arguments.append(int(self.buffer))
        except ValueError:
            try:
                self.current_arguments.append(float(self.buffer))
            except ValueError:
                self.current_arguments.append(self.buffer)
        self.clear_buffer()

    def finalize_instruction(self):

        if not self.has_instruction:
            self.capture_instruction_name()
        else:
            self.capture_argument()

        self.tokens.append({"instruction": self.current_instruction, "arguments": self.current_arguments})
        self.current_instruction = ""
        self.current_arguments = []
        self.has_instruction = False

    def clear_buffer(self):
        self.buffer = ""


class Function:
    def __init__(self, name):
        self.name = name
        self.local_variables = []
        self.parameter_count = 0
        self.tokens = []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.program = {"functions": [], "uninitialized_global_variables": [], "initialized_global_variables": []}
        self.in_function_body = False

    def parse(self):
        for token in self.tokens:
            if token['instruction'] == "FN":
                self.start_function(token)
            elif token['instruction'] == "ENDFN":
                self.end_function()
            elif self.in_function_body:
                self.append_instruction(token)
            else:
                self.append_global_variables(token)

        return self.program

    def start_function(self, token):
        self.in_function_body = True
        self.program["functions"].append(Function(token['arguments'][0]))
        self.program["functions"][-1].parameter_count = token['arguments'][1]

    def end_function(self):
        self.in_function_body = False

    def append_instruction(self, token):
        self.program["functions"][-1].tokens.append(token)
        if token['instruction'] == "int":
            self.program["functions"][-1].local_variables.append(token['arguments'][0])
            token['arguments'].append(len(self.program["functions"][-1].local_variables))

    def append_global_variables(self, token):
        if token['instruction'] == "int":
            if len(token['arguments']) == 1:
                self.program["uninitialized_global_variables"].append({"type": "int", "name": token['arguments'][0]})
            elif len(token['arguments']) == 2:
                self.program["initialized_global_variables"].append({"type": "int", "name": token['arguments'][0], "value": token['arguments'][1]})

class Compiler:
    def __init__(self, program):
        self.program = program
        self.assembly_code = ""
        self.arguments_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
        self.output_file = "output.asm"

    def compile(self):
        self.section_text()
        self.save_assembly()
        self.build_executable()

    def section_text(self):
        self.add_assembly_code("section .data\n")
        self.add_assembly_code("fmt_out_int? db \"%d\", 10, 0\n")
        for var in self.program["initialized_global_variables"]:
            if var['type'] == 'int':
                self.add_assembly_code(f"{var['name']}? dq {var['value']}\n%define {var['name']} [{var['name']}?]\n")

        self.add_assembly_code("section .bss\n")
        for var in self.program["uninitialized_global_variables"]:
            if var['type'] == 'int':
                self.add_assembly_code(f"{var['name']}? resq 1\n%define {var['name']} [{var['name']}?]\n")

        self.add_assembly_code("section .text\nglobal main\nextern printf\n%define return_value rax\n")

        self.add_assembly_code("print_int:\nmov rsi, rdi\nmov rdi, fmt_out_int?\nxor rax, rax\ncall printf\nret\n")

        for i in self.program["functions"]:
            self.add_assembly_code(f"{i.name}:\npush rbp\nmov rbp, rsp\n")

            if ((len(i.local_variables) + i.parameter_count) * 8) % 16 == 0:
                self.add_assembly_code(f"sub rsp, {(len(i.local_variables) + i.parameter_count) * 8}\n")
            else:
                self.add_assembly_code(f"sub rsp, {(len(i.local_variables) + i.parameter_count) * 8 + 8}\n")

            for j in range(i.parameter_count):
                self.add_assembly_code(f"%define parameter_{j+1} [rbp-{(j+1)*8}]\n")
                self.add_assembly_code(f"mov parameter_{j+1}, {self.arguments_registers[j]}\n")

            for j in i.tokens:
                if j["instruction"] == "int":
                    if len(j['arguments']) == 2:
                        self.add_assembly_code(f"%define {j['arguments'][0]} [rbp-{(j['arguments'][1] + i.parameter_count) * 8}]\n")
                    if len(j['arguments']) == 3:
                        self.add_assembly_code(f"%define {j['arguments'][0]} [rbp-{(j['arguments'][2] + i.parameter_count) * 8}]\n")
                        self.add_assembly_code(f"mov rax, {j['arguments'][1]}\nmov {j['arguments'][0]}, rax\n")
                elif j["instruction"] == "set":
                    self.add_assembly_code(f"mov rax, {j['arguments'][1]}\nmov {j['arguments'][0]}, rax\n")
                elif j["instruction"] == "add":
                    self.add_assembly_code(f"mov rax, {j['arguments'][1]}\nadd {j['arguments'][0]}, rax\n")
                elif j["instruction"] == "sub":
                    self.add_assembly_code(f"mov rax, {j['arguments'][1]}\nsub {j['arguments'][0]}, rax\n")
                elif j["instruction"] == "mul":
                    self.add_assembly_code(f"mov rax, {j['arguments'][0]}\nimul rax, {j['arguments'][1]}\nmov {j['arguments'][0]}, rax\n")
                elif j["instruction"] == "return":
                    self.add_assembly_code(f"mov rax, {j['arguments'][0]}\njmp .end\n")
                else:
                    for k in range(len(j['arguments'])):
                        self.add_assembly_code(f"mov {self.arguments_registers[k]}, {j['arguments'][k]}\n")
                    self.add_assembly_code(f"call {j['instruction']}\n")

            self.add_assembly_code(".end:\n")

            for j in range(i.parameter_count):
                self.add_assembly_code(f"%undef parameter_{j+1}\n")

            for j in i.local_variables:
                self.add_assembly_code(f"%undef {j}\n")

            self.add_assembly_code("mov rsp, rbp\npop rbp\nret\n")

    def add_assembly_code(self, code):
        self.assembly_code += code

    def save_assembly(self):
        with open(self.output_file, "w") as file:
            file.write(self.assembly_code)

    def build_executable(self):
        subprocess.run(["nasm", "-f", "elf64", "-g", "-F", "dwarf", self.output_file, "-o", "program.o"], check=True)
        subprocess.run(["gcc", "-no-pie", "program.o", "-o", "program", "-lc"], check=True)


if __name__ == "__main__":
    print("Compiling...")
    lexer = Lexer("code.txt")
    parser = Parser(lexer.tokenize())
    compiler = Compiler(parser.parse())
    compiler.compile()
    print("Running a program...")
    subprocess.run(["./program"], check=True)
