import numpy
from .Fsm import FSM, State
from .Prompt import Prompt
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from typing import Dict, List, Any
from .functions import Functions

@dataclass
class Constrained:

    prompt: str
    functions_data: Dict
    _model: Small_LLM_Model = Small_LLM_Model()

    def get_valid_function(self, allowed: List[List[int]], ids_obj:List[int], comma: List[int]) -> List[int]:

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

    @property
    def get_valid_fun_name(self) -> List[str]:
        fun_names = [
            self._model.encode(Functions(self.functions_data[i]).name).tolist()[0]
            for i in range(len(self.functions_data))
            ]
        return fun_names

    @property
    def get_valid_params(self):
        fun_params = [
            Functions(self.functions_data[i]).parameters
            for i in range(len(self.functions_data))
        ]
        return fun_params

    @property
    def get_description(self):
        fun_desc = [
            self._model.encode(Functions(self.functions_data[i]).description).tolist()[0]
            for i in range(len(self.functions_data))
        ]
        return fun_desc

    @property
    def constrained_decoding(self) -> List:

        updated_prompt: str = Prompt(self.prompt, self.functions_data).update_prompt
        ids_obj: List[int] = self._model.encode(updated_prompt).tolist()[0]
        prompt_len = len(ids_obj)
        state_obj: State = State.START_OBJ
        obj: List[str, Any] = []
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
                valid_logit = self.get_valid_function(self.get_valid_fun_name, ids_obj, comma)
            # elif allowed_token_json == '2':
                

            else:
                valid_logit: List[int] = self._model.encode(allowed_token_json).tolist()[0]
                ids_obj.extend(valid_logit)

            state_obj = FSM.next_state_for_one_prompt(state_obj)
        ids_obj = ids_obj[prompt_len:]
        return self._model.decode(ids_obj)
