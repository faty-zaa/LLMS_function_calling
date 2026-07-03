import argparse
from dataclasses import dataclass, field


@dataclass
class ArgParse:
    parser: argparse.ArgumentParser = field(default_factory=argparse.ArgumentParser)

    def __post_init__(self):
        self.parser.add_argument(
            "--functions_definition",
            dest="functions_definition",
            default="data/input/functions_definition.json",
        )

        self.parser.add_argument(
            "--input", dest="input", default="data/input/function_calling_tests.json"
        )

        self.parser.add_argument(
            "--output", dest="output", default="data/output/function_calls.json"
        )

    @property
    def get_args(self):
        return self.parser.parse_args()
