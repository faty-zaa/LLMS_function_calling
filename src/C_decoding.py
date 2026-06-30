import numpy
from .Fsm import FSM, State
from .Prompt import Prompt
from llm_sdk import Small_LLM_Model
from typing import Dict, List
from .Get import Get
from .Generated import Generated, dataclass

@dataclass
class ConstrainedDecoding:

    prompt: str
    functions_data: Dict
    _i: int = -1
    _model: Small_LLM_Model = Small_LLM_Model()

    def get_valid_generated_function(self, allowed: List[List[int]], ids_obj:List[int], comma: List[int]) -> List[int]:

        generated: List[int] = []

        while True:

            logits: List[float] = self._model.get_logits_from_input_ids(ids_obj)
            logits: List[int] = numpy.array(logits)
            next_token: List[int] = []

            for function in allowed:

                if function[: len(generated)] == generated:

                    if len(generated) < len(function):

                        next_token.append(function[len(generated)])

            masked_logits = numpy.full_like(logits, -numpy.inf)

            masked_logits[next_token] = logits[next_token]

            valid_logit = numpy.argmax(masked_logits)

            generated.append(valid_logit)
            ids_obj.append(valid_logit)

            if generated in allowed:
                ids_obj.extend(comma)
                break

        return generated

    def get_valid_generated_params(self, value: str, ids_obj: List[int]) -> None:
        TYPE_MAP = {
            "int": "integer",
            "float": "number",
            "str": "string",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
        }
        if value == "number":
            Generated().generate_float(ids_obj)

        elif value == "integer":
            Generated().generate_int(ids_obj)

        elif value == "string":
            Generated().generate_str(ids_obj)

        elif value == "boolean":
            Generated().generate_bool(ids_obj)

        elif value == "array":
            Generated().generate_list(ids_obj)

        elif value == "object":
            Generated().generate_dict()

    @property
    def constrained_decoding(self) -> List:

        updated_prompt: str = Prompt(self.prompt, self.functions_data).update_prompt
        ids_obj: List[int] = self._model.encode(updated_prompt).tolist()[0]
        prompt_len = len(ids_obj)
        n_functions = len(self.functions_data)
        state_obj: State = State.START_OBJ
        comma = self._model.encode(",").tolist()[0]

        while state_obj != State.DONE:

            allowed_token_json: str = FSM.allowed_tokens(state_obj)

            if allowed_token_json == '0':
                valid_logit: List[int] = self._model.encode(
                    '"' + self.prompt + '"'
                ).tolist()[0]
                valid_logit.extend(comma)
                ids_obj.extend(valid_logit)

            elif allowed_token_json == '1':
                valid_logit = self.get_valid_generated_function(Get(self.functions_data, self._model).get_name, ids_obj, comma)
                self._i = Get(self.functions_data, self._model).get_name.index(valid_logit)

            elif allowed_token_json == '2':
                allowed = Get(self.functions_data, self._model).get_valid_params[self._i]
                valid_logit = self._model.encode("{").tolist()[0]
                comma_count = 0
                for key, value in allowed.items():
                    valid_logit.extend(self._model.encode("\""+ key + "\"" + ": ").tolist()[0])
                    # valid_logit.extend(self.get_valid_generated_params)
                    if comma_count < len(list(allowed.keys())) - 1:
                        valid_logit.extend(comma)
                        comma_count += 1
                ids_obj.extend(valid_logit)

            else:
                valid_logit: List[int] = self._model.encode(allowed_token_json).tolist()[0]
                ids_obj.extend(valid_logit)

            state_obj = FSM.next_state_for_one_prompt(state_obj)
        ids_obj = ids_obj[prompt_len:]
        return self._model.decode(ids_obj)
