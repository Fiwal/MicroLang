from dataclasses import dataclass, field
from typing import Any

@dataclass
class Token:
    name: Any
    line: int
    arguments: list[Any] = field(default_factory=list)
    connected_tokens: list["Token"] = field(default_factory=list)