from .Fsm import FSM, State
from .Prompt import Prompt
from typing import Dict, Any
from .Get import Get
from .Generated import Generated, dataclass, Small_LLM_Model, List, numpy


@dataclass
class ConstrainedDecoding:

    prompts: List[Dict[str, Any]]
    functions_data: List[Dict[str, Any]]
    _i: int = -1
    _model: Small_LLM_Model = Small_LLM_Model()

    def get_valid_generated_function(
        self, allowed: List[List[int]], ids_obj: List[int], comma: List[int]
    ) -> List[int]:

        generated: List[int] = []
        while True:
            logits = numpy.array(
                self._model.get_logits_from_input_ids(ids_obj)
            )
            next_token: List[int] = []

            for function in allowed:

                if function[: len(generated)] == generated:

                    if len(generated) < len(function):

                        next_token.append(function[len(generated)])
                    else:
                        next_token.extend(comma)
            masked_logits = numpy.full_like(logits, -numpy.inf)

            masked_logits[next_token] = logits[next_token]

            valid_logit = int(numpy.argmax(masked_logits))

            if valid_logit in comma:
                break

            ids_obj.append(valid_logit)
            generated.append(valid_logit)
        return generated

    def get_valid_generated_params(
        self, value: str, ids_obj: List[int]
    ) -> None:

        if value == "number":
            Generated(self._model).generate_float(ids_obj)

        elif value == "integer":
            Generated(self._model).generate_int(ids_obj)

        elif value == "string":
            Generated(self._model).generate_str(ids_obj)

        elif value == "boolean":
            Generated(self._model).generate_bool(ids_obj)

    def constrained_decoding(self, prompt: str) -> List[int]:

        updated_prompt: str = Prompt(prompt, self.functions_data).update_prompt
        ids_obj: List[int] = self._model.encode(updated_prompt).tolist()[0]
        prompt_len = len(ids_obj)
        state_obj: State = State.START_OBJ
        comma = self._model.encode(",").tolist()[0]
        quote = self._model.encode('"').tolist()[0]

        while state_obj != State.DONE:

            allowed_token_json: str | None = FSM.allowed_tokens(state_obj)

            if allowed_token_json == "user_prompt":
                prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')
                valid_logit: List[int] = self._model.encode(
                    '"' + prompt + '"'
                ).tolist()[0]
                valid_logit.extend(comma)
                ids_obj.extend(valid_logit)

            elif allowed_token_json == "fn_name":
                ids_obj.extend(quote)
                valid_logit = self.get_valid_generated_function(
                    Get(self.functions_data, self._model).get_name,
                    ids_obj,
                    comma,
                )
                self._i = Get(self.functions_data, self._model).get_name.index(
                    valid_logit
                )
                ids_obj.extend(quote)
                ids_obj.extend(comma)

            elif allowed_token_json == "params":
                allowed = Get(
                    self.functions_data, self._model
                ).get_valid_params[self._i]
                ids_obj.extend(self._model.encode("{").tolist()[0])
                comma_count = 0
                for key, value in allowed.items():
                    ids_obj.extend(
                        self._model.encode('"' + key + '"' + ": ").tolist()[0]
                    )
                    self.get_valid_generated_params(value, ids_obj)

                    if comma_count < len(list(allowed.keys())) - 1:
                        ids_obj.extend(comma)
                        comma_count += 1
                ids_obj.extend(self._model.encode("}").tolist()[0])
            else:
                if allowed_token_json is not None:
                    valid_logit = self._model.encode(
                        allowed_token_json
                    ).tolist()[0]
                    ids_obj.extend(valid_logit)

            state_obj = FSM.next_state_for_one_prompt(state_obj)
        ids_obj = ids_obj[prompt_len:]
        return ids_obj

    def json_format(self) -> Any:
        state_json = State.START_ARR
        position = 0
        count = len(self.prompts)
        ids_json = []
        while state_json != State.RETURN and position < count:
            allowed = FSM.allowed_tokens(state_json)
            if state_json == State.OBJ:
                ids_json.extend(
                    self.constrained_decoding(self.prompts[position]["prompt"])
                )
                position += 1
                if position == count:
                    state_json = State.END_ARR
                    allowed = FSM.allowed_tokens(state_json)
                    if allowed is not None:
                        ids_json.extend(
                            self._model.encode(allowed).tolist()[0]
                        )
            elif allowed is not None:
                ids_json.extend(self._model.encode(allowed).tolist()[0])

            state_json = FSM.json_state(state_json)
        return self._model.decode(ids_json)
