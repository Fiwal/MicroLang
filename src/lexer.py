from src.exceptions.error import Error
from src.utils.decorators import measure_time
from src.structures.token import Token


class Lexer:
    QUOTES = ["\"", "`"]
    COMMENT_CHAR = "#"

    def __init__(self, source_path):
        self.source_path = source_path
        with open(source_path) as f:
            self.source = f.read()

        self.buffer = ""
        self.tokens = []
        self.current_token_name = ""
        self.current_arguments = []
        self.token_line = 1

        self.token_name_found = False
        self.token_started = False
        self.in_comment = False
        self.line_number = 1
        self.in_quote = False

    @measure_time("Tokenizing...")
    def tokenize(self):
        for char in self.source:
            self.process_char(char)

        if self.in_quote:
            raise Error("Unclosed quote")
        if self.token_started:
            raise Error("Unclosed instruction")

        return self.tokens

    def process_char(self, char):
        if char == "\n":
            self.add_line()
            if self.in_comment:
                self.in_comment = False
            return

        if char == self.COMMENT_CHAR and not self.in_comment and not self.in_quote:
            self.in_comment = True
            return

        if char in self.QUOTES and not self.in_comment:
            self.capture_quote()
            return

        if self.in_quote:
            self.capture_char_in_quotes(char)
            return

        if not char.isspace() and not self.in_comment and not self.in_quote:
            match char:
                case ":":
                    self.capture_token_name()
                case ",":
                    self.capture_argument()
                case ";":
                    self.emit_token()
                case _:
                    self.capture_character(char)

    def add_line(self):
        self.line_number += 1

    def capture_quote(self):
        if not self.in_quote and self.buffer != "":
            raise Error(f"Wrong quote position - line {self.line_number}")

        self.in_quote = not self.in_quote
        self.buffer += "`"

    def capture_char_in_quotes(self, char):
        self.buffer += char

    def capture_token_name(self):
        if self.token_name_found:
            raise Error(f"Duplicate ':' in instruction - line {self.line_number}")
        self.token_name_found = True
        self.current_token_name = self.buffer
        self.clear_buffer()

    def capture_argument(self):
        if not self.token_name_found:
            raise Error(f"Argument found before instruction name - line {self.line_number}")

        self.current_arguments.append(self.convert_argument())
        self.clear_buffer()

    def convert_argument(self):
        try:
            return int(self.buffer)
        except ValueError:
            try:
                return float(self.buffer)
            except ValueError:
                return self.buffer

    def emit_token(self):
        if not self.token_name_found:
            self.capture_token_name()
        else:
            self.capture_argument()

        self.tokens.append(Token(self.current_token_name, self.token_line, self.current_arguments))
        self.reset_token_state()

    def capture_character(self, char):
        if not self.buffer == "" and self.buffer[-1] == "`":
            raise Error(f"Unexpected character after closing quote - line {self.line_number}")

        if not self.token_started:
            self.token_line = self.line_number
            self.token_started = True

        self.buffer += char

    def clear_buffer(self):
        self.buffer = ""

    def reset_token_state(self):
        self.current_token_name = ""
        self.current_arguments = []
        self.token_name_found = False
        self.token_started = False
