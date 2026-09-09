from src.utils import KEYWORDS, COMPARISON_JUMPS
from src.utils import check_name_type
from src.enums import NameType

class BaseStatement:
    def __init__(self, token, program, function):
        self.arguments = token.arguments
        self.line = token.line
        self.program = program
        self.function = function

    def add_dollar_sign(self):
        for i in range(len(self.arguments)):
            if (isinstance(self.arguments[i], str) and not self.arguments[i] in KEYWORDS and not self.arguments[i] in COMPARISON_JUMPS
                    and not check_name_type(self.arguments[i], self.program, self.function) == NameType.PARAMETER):
                self.arguments[i] = self.arguments[i] + "$"
