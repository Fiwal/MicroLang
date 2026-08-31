class BaseStatement:
    def __init__(self, token, parsed_program, function):
        self.arguments = token.arguments
        self.line = token.line
        self.parsed_program = parsed_program
        self.function = function