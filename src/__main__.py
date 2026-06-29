from .parsing_json import Parser
from .Parse_args import ArgParse
from llm_sdk import Small_LLM_Model
from .Prompt import Prompt
import json
from .C_decoding import Constrained
from .functions import Functions

if __name__ == "__main__":

    args = ArgParse().get_args

    prompt_data = Parser(args).parse_prompt_data
    funt_data = Parser(args).parse_func_definitions_data
    # model = Small_LLM_Model()

    # prompt = Prompt("add 2 to 3", funt_data).update_prompt
    # ids = model.encode(prompt)
    # ids_list = ids.tolist()[0]
    # generated_ids = []
    # for _ in range(90):
    #     logits = model.get_logits_from_input_ids(ids_list + generated_ids)
    #     next_token_id = logits.index(max(logits))
    #     decoded_token = model.decode([next_token_id])
    #     if decoded_token == "":
    #         break
    #     generated_ids.append(next_token_id)
    #     print(decoded_token, end="", flush=True)
    # # with open("data.json", "w") as file:
    # #     json.dump(model.decode(generated_ids), file, indent=4)
    for i in range(len(prompt_data)):
        print(Constrained(prompt_data[i]['prompt'], funt_data).constrained_decoding)
