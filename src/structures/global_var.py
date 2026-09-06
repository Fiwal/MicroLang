from dataclasses import dataclass, field
from typing import Any
from src.enums import VarType


@dataclass
class GlobalVar:
    name: str
    type: VarType
    value: Any = None
    is_initialized: bool = field(init=False)

    def __post_init__(self):
        self.is_initialized = self.value is not None