from .parsing_json import Parser
from .Parse_args import ArgParse
import json
from .C_decoding import ConstrainedDecoding
from pathlib import Path

if __name__ == "__main__":
    try:
        args = ArgParse().get_args

        parser = Parser(args)
        prompt_data = parser.parse_prompt_data
        funt_data = parser.parse_func_definitions_data
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        result = ConstrainedDecoding(prompt_data, funt_data).json_format()

        with open(output_dir / "function_calls.json", "w") as file:
            json.dump(json.loads(result), file, indent=4)
    
    except Exception as e:
        print(e)