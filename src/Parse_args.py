import argparse
from dataclasses import dataclass, field
from argparse import Namespace


@dataclass
class ArgParse:
    parser: argparse.ArgumentParser = field(
        default_factory=argparse.ArgumentParser
    )

    def __post_init__(self) -> None:
        self.parser.add_argument(
            "--functions_definition",
            dest="functions_definition",
            default="data/input/functions_definition.json",
        )

        self.parser.add_argument(
            "--input",
            dest="input",
            default="data/input/function_calling_tests.json",
        )

        self.parser.add_argument(
            "--output",
            dest="output",
            default="data/output/function_calls.json",
        )
        self.parser.add_argument(
            "--model",
            default="Qwen/Qwen3-0.6B",
            choices=[
                "Qwen/Qwen3-0.6B",
                "Qwen/Qwen3-1.7B",
                "Qwen/Qwen3-4B",
                "Qwen/Qwen3-8B",
                "Qwen/Qwen2.5-0.5B-Instruct",
                "Qwen/Qwen2.5-1.5B-Instruct",
            ],
        )

    @property
    def get_args(self) -> Namespace:
        return self.parser.parse_args()
