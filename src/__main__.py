import argparse
import json
from .valid_jsn import ValidatJson

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--functions_definition", default="data/input/functions_definition.json"
        )
        parser.add_argument("--input", default="data/input/function_calling_tests.json")
        parser.add_argument("--output", default="data/output/function_calls.json")
        args = parser.parse_args()

        with open(args.input, 'r') as file:
            prompt = json.load(file)
            print(prompt)

    except Exception as e:
        print(e)