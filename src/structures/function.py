from src.utils import Stack
from src.structures.statements import *


class Function:
    statements = {"int": IntStatement, "set": SetStatement, "add": AddStatement,
      "sub": SubStatement, "mul": MulStatement, "div": DivStatement,
      "mod": ModStatement, "print_int": PrintIntStatement,
      "input_int": InputIntStatement, "print": PrintStatement,
      "return": ReturnStatement, "IF": IfStatement, "ELSE": ElseStatement,
      "ENDIF": EndifStatement, "LOOP": LoopStatement, "break": BreakStatement,
      "ENDLOOP": EndloopStatement, "name_parameter": NameParameterStatement}

    def __init__(self, name, parameters_num):
        self.name = name
        self.parameter_count = parameters_num
        self.tokens = []
        self.local_variables = []
        self.parameters = []
        self.parameters_with_names = []
        self.if_counter = 0
        self.if_stack = Stack()
        self.loop_counter = 0
        self.loop_stack = Stack()
        self.if_and_loop_stack = Stack()
        self.statements_list = []

    def parse_function(self, program):
        for token in self.tokens:
            if token.name in self.statements:
                self.statements_list.append(self.statements[token.name](token, program, self))
            else:
                self.statements_list.append(FunctionCallStatement(token, program, self))
            self.statements_list[-1].parse()
