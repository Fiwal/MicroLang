from src.utils import Stack
from src.structures.statements import *
from src.exceptions import Error


class Function:
    statements = {"int": IntStatement, "set": SetStatement, "add": AddStatement,
      "sub": SubStatement, "mul": MulStatement, "div": DivStatement,
      "mod": ModStatement,
      "input": InputStatement, "print": PrintStatement,
      "return": ReturnStatement, "if": IfStatement, "else": ElseStatement,
      "endif": EndifStatement, "loop": LoopStatement, "break": BreakStatement,
      "endloop": EndloopStatement, "name_parameter": NameParameterStatement}

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
        if not self.if_stack.is_empty():
            raise Error(f"Unclosed if in function '{self.name}'")
        if not self.loop_stack.is_empty():
            raise Error(f"Unclosed loop in function '{self.name}'")

    def add_dollar_signs(self):
        for statement in self.statements_list:
            statement.add_dollar_sign()
        for i in range(len(self.parameters)):
            self.parameters[i] += "$"
        for i in range(len(self.local_variables)):
            self.local_variables[i] += "$"
        if self.name != "main":
            self.name += "$"