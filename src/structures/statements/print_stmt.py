from src.exceptions import Error
from src.enums import NameType
from src.utils import check_name_type as check_name
from src.structures.statements.base_stmt import BaseStatement
from src.structures.global_var import GlobalVar
from src.enums import VarType


class PrintStatement(BaseStatement):
    def parse(self):
        self.check_for_error()
        for i in range(len(self.arguments)):
            if isinstance(self.arguments[i], str) and (self.arguments[i].count("`") == 2) and self.arguments[i][0] == "`" and self.arguments[i][-1] == "`":
                found_var = False
                for var in self.program.initialized_global_variables:
                    if var.value == self.arguments[i]:
                        self.arguments[i] = var.name
                        found_var = True
                        break
                if not found_var:
                    auto_str_num = len(self.program.initialized_global_variables)
                    self.program.initialized_global_variables.append(GlobalVar(f"str$auto{auto_str_num}", VarType.STRING, self.arguments[i]))
                    self.arguments[i] = f"str$auto{auto_str_num}"

    def check_for_error(self):
        if len(self.arguments) < 1:
            raise Error(f"Wrong number of arguments for print: expected at least 1, got {len(self.arguments)} - line {self.line}")
        if self.connected_tokens:
            raise Error(f"Cannot connect instructions with print - line {self.connected_tokens[0].line}")
        for argument in self.arguments:
            if isinstance(argument, str) and (argument.count("`") == 2) and argument[0] == "`" and argument[-1] == "`":
                continue
            if check_name(argument, self.program, self.function) not in [NameType.INT_VARIABLE, NameType.INT_NUM, NameType.STRING_VARIABLE]:
                raise Error(f"Wrong argument for print '{argument}' - line {self.line}")

    def generate_nasm_code(self):
        nasm_code = ""
        for argument in self.arguments:
            if check_name(argument, self.program, self.function) == NameType.STRING_VARIABLE:
                nasm_code += (
                    "mov rdi, fmt_str?\n"
                    f"mov rsi, {argument}\n"
                    "xor rax, rax\n"
                    "call printf\n")
                continue
            nasm_code += (
                "mov rdi, fmt_int?\n"
                f"mov rsi, {argument}\n"
                "xor rax, rax\n"
                "call printf\n")
        return nasm_code
