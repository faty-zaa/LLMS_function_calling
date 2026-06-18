import argparse
import json
from .valid_jsn import ValidatCalls, ValidDefinitions
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--functions_definition", default="data/input/functions_definition.json"
        )
        parser.add_argument("--input", default="data/input/function_calling_tests.json")
        parser.add_argument("--output", default="data/output/function_calls.json")
        args = parser.parse_args()

        with open(args.input, 'r') as file1:
            try:
                prompt_data = json.load(file1)
                prompt_validation = [ValidatCalls.model_validate(i) for i in prompt_data]
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
                raise ValueError
        with open(args.functions_definition, 'r') as file2:
            try:
                func_data = json.load(file2)
                func_validation = [ValidDefinitions.model_validate(j) for j in func_data]
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
                raise ValueError
    except Exception as e:
        print(e)
