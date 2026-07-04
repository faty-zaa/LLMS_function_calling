from .parsing_json import Parser
from .Parse_args import ArgParse
import json
from .C_decoding import ConstrainedDecoding
from pathlib import Path

if __name__ == "__main__":

    args = ArgParse().get_args

    parser = Parser(args)
    prompt_data = parser.parse_prompt_data
    funt_data = parser.parse_func_definitions_data

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    result = ConstrainedDecoding(prompt_data, funt_data).json_format()

    with open(output_path, "w") as file:
        json.dump(json.loads(result), file, indent=4)
