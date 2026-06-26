from .Fsm import FSM, State
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from .Prompt import Prompt
import numpy


@dataclass
class Constrained:
    prompt: str 
    _model = Small_LLM_Model()

    def get_valid_token(self, allowed, logits):
        logits = numpy.array(logits)
        allowed = self._model.encode(allowed).tolist()[0]
        masked_logits = numpy.full_like(logits, -numpy.inf)
        masked_logits[allowed] = logits[allowed]
        return numpy.argmax(masked_logits)

    @property
    def constrained_decoding(self):

        updated_prompt = Prompt(self.prompt).update_prompt
        ids_json = self._model.encode(updated_prompt).tolist()[0]
        logits = self._model.get_logits_from_input_ids(ids_json)
        state_json = State.START_ARR
        json_file = []

        while state_json != State.RETURN:
            allowed_token_json = FSM.allowed_tokens(state_json)
            valid_logit = self.get_valid_token(allowed_token_json, logits)
            decoded = self._model.decode([valid_logit])
            json_file.append(decoded)
            
            while 
