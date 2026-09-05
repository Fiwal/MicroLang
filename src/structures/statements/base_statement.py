class BaseStatement:
    def __init__(self, token, program, function):
        self.arguments = token.arguments
        self.line = token.line
        self.program = program
        self.function = function