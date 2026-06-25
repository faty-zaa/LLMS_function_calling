from .Fsm import FSM, State
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from .Prompt import Prompt


@dataclass
class Constrained:
    prompt: str 

    @property
    def constrained_decoding(self):
    
        updated_prompt = Prompt(self.prompt).update_prompt
        model = Small_LLM_Model()
        logits_json = model.encode(updated_prompt).tolist()[0]
        state_json = State.START_ARR

        while state_json != State.RETURN:
            allowed_token_json = FSM.allowed_tokens(state_json)
            print(allowed_token_json)
            print(state_json)
            state_json = FSM.json_state(state_json)
            
