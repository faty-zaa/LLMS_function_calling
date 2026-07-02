from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from typing import List
import numpy

@dataclass
class Generated:
    model: Small_LLM_Model

    def generate_int(self, ids_obj):
        allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", ","]
        allowed_id = []
        for i in allowed:
            ids = self.model.encode(i).tolist()[0]
            allowed_id.extend(ids)
        while True:
            logits = self.model.get_logits_from_input_ids(ids_obj)
            logits: List[int] = numpy.array(logits)
            masked_logits = numpy.full_like(logits, -numpy.inf)
            masked_logits[allowed_id] = logits[allowed_id]
            valid = int(numpy.argmax(masked_logits))
            if self.model.decode(allowed_id[-1]) in self.model.decode(valid):
                break
            ids_obj.append(valid)

    def generate_float(self, ids_obj):
        allowed = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+', '.'
            ]
        allowed_id = []
        for i in allowed:
            ids = self.model.encode(i).tolist()[0]
            allowed_id.extend(ids)
        count = 2
        state = False
        while True:
            logits = self.model.get_logits_from_input_ids(ids_obj)
            logits: List[int] = numpy.array(logits)
            masked_logits = numpy.full_like(logits, -numpy.inf)
            masked_logits[allowed_id] = logits[allowed_id]
            valid = int(numpy.argmax(masked_logits))
            if self.model.decode(allowed_id[-1]) in self.model.decode(valid):
                allowed_id = allowed_id[:10]
                state = True
            elif state and count > 0:
                count -= 1
            elif count == 0:
                break
                
            ids_obj.append(valid)

    def generate_str(self, ids_obj):
        escape = self.model.encode('\\').tolist()[0][0]
        quote = self.model.encode('"').tolist()[0][0]
        ids_obj.append(quote)

        while True:
            logits = self.model.get_logits_from_input_ids(ids_obj)
            logits: List[int] = numpy.array(logits)
            valid = int(numpy.argmax(logits))
            decoded = self.model.decode(valid)
            if '"' in decoded and not ids_obj[-1] == escape:
                ids_obj.append(quote)
                break
            ids_obj.append(valid)

    def generate_bool(self, ids_obj):
        pass
