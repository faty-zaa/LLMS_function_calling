from typing import Dict, Any
from keyword import iskeyword
from dataclasses import dataclass


@dataclass
class Functions:

    data: Dict[str, Any]

    @property
    def name(self) -> Any:
        name = self.data["name"]
        if not name.isidentifier() or iskeyword(name):
            raise ValueError("Invalid function name")
        return name

    @property
    def description(self) -> Any:
        return self.data["description"]

    @property
    def parameters(self) -> Dict[str, str]:
        return {
            key: value["type"]
            for key, value in self.data["parameters"].items()
        }
