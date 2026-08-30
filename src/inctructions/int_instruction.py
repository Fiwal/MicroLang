class IntInstruction:
    def __init__(self, token, ast, function):
        self.arguments == token["arguments"]
        self.line == token["line_number"]
        self.ast == ast
        self.function == function

    def parse(self):
        self.check_for_error

    def check_for_error(self):
        pass