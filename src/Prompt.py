
from dataclasses import dataclass

@dataclass
class Prompt:
    user_prompt: str

    @property
    def update_prompt(self):
        prompt: str = ""

        