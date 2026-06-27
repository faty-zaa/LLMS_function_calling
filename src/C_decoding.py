from .Fsm import FSM, State
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from .Prompt import Prompt
import numpy
from typing import Dict


@dataclass
class Constrained:
    prompt: str
    functions: Dict
    _model = Small_LLM_Model()

    # why we don't just inject the token directly into the obj instead
    def get_valid_token(self, allowed, logits):
        logits = numpy.array(logits)
        allowed = self._model.encode(allowed).tolist()[0]
        masked_logits = numpy.full_like(logits, -numpy.inf)
        masked_logits[allowed] = logits[allowed]
        return numpy.argmax(masked_logits)

    @property
    def constrained_decoding(self):

        updated_prompt = Prompt(self.prompt, self.functions).update_prompt
        print(updated_prompt)
        # encoded prompt as []
        ids_obj = self._model.encode(updated_prompt).tolist()[0]
        # get the logits
        logits = self._model.get_logits_from_input_ids(ids_obj)
        state_obj = State.START_OBJ
        json_file = []
        obj = []
        string = ""
        i = 0

        while state_obj != State.DONE:
            allowed_token_json = FSM.allowed_tokens(state_obj)  # {
            if allowed_token_json is None:
                valid_logit = [int(numpy.argmax(logits))]

            else:
                valid_logit = self._model.encode(allowed_token_json).tolist()[0]
            # get the string version to print it in the console
            decoded = self._model.decode([valid_logit])

            obj.append(decoded)

            # string += decoded
            
            ids_obj.extend(valid_logit)

            logits = self._model.get_logits_from_input_ids(ids_obj)

            state_obj, i = FSM.next_state_for_one_prompt(state_obj, i)

            if obj != None:
                print(obj)
