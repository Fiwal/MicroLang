from dataclasses import dataclass, field
from src.structures.function import Function
from src.structures.global_var import GlobalVar

@dataclass
class ProgramStruct:
    functions: list[Function] = field(default_factory=list)
    initialized_global_variables: list[GlobalVar] = field(default_factory=list)
    uninitialized_global_variables: list[GlobalVar] = field(default_factory=list)