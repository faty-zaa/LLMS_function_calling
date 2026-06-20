from .parsing_json import Parser
from .Parse_args import ArgParse
from llm_sdk import Small_LLM_Model

if __name__ == "__main__":

    args = ArgParse().get_args

    prompt_data = Parser(args).parse_prompt_data
    funt_data = Parser(args).parse_func_definitions_data

    model = Small_LLM_Model()
    ids = model.encode("hello")
    ids_list = ids.tolist()[0]
    print(ids_list)
    logits = model.get_logits_from_input_ids(ids_list)
    max_logits = max(logits)
    print(max_logits)
    index = logits.index(max_logits)
    decode = model.decode(index)
    print(decode)
