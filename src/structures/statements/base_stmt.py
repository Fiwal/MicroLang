from src.utils import KEYWORDS, COMPARISON_JUMPS


class BaseStatement:
    def __init__(self, token, program, function):
        self.arguments = token.arguments
        self.connected_tokens = token.connected_tokens
        self.line = token.line
        self.program = program
        self.function = function

    def add_dollar_sign(self):
        def add_dollar_sign_to_argument(argument):
            if isinstance(argument, str) and not argument in KEYWORDS and not argument in COMPARISON_JUMPS:
                return argument + "$"
            return argument
        for i in range(len(self.arguments)):
            self.arguments[i] = add_dollar_sign_to_argument(self.arguments[i])
        for token in self.connected_tokens:
            for i in range(len(token.arguments)):
                token.arguments[i] = add_dollar_sign_to_argument(token.arguments[i])
