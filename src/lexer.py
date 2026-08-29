from src.utils import print_msg_and_measure_time


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
                if not self.buffer in ["", "`"] and char == "`":
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
                        if not self.buffer in ["", "`"] and self.buffer[-1] == "`":
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
