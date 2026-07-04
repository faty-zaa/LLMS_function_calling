from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from typing import List
import numpy


@dataclass
class Generated:
    model: Small_LLM_Model

    def generate_int(self, ids_obj: List[int]) -> None:
        allowed = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "-",
            "+",
            ",",
        ]
        allowed_id = []
        for i in allowed:
            ids = self.model.encode(i).tolist()[0]
            allowed_id.extend(ids)
        while True:
            logits = numpy.array(self.model.get_logits_from_input_ids(ids_obj))
            masked_logits = numpy.full_like(logits, -numpy.inf)
            masked_logits[allowed_id] = logits[allowed_id]
            valid = int(numpy.argmax(masked_logits))
            if self.model.decode(allowed_id[-1]) in self.model.decode(valid):
                break
            ids_obj.append(valid)

    def generate_float(self, ids_obj: List[int]) -> None:
        allowed = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "-",
            "+",
            ".",
        ]
        allowed_id = []
        for i in allowed:
            ids = self.model.encode(i).tolist()[0]
            allowed_id.extend(ids)
        dot = self.model.encode(".").tolist()[0][0]
        count = 2
        state = False
        while True:
            logits = numpy.array(self.model.get_logits_from_input_ids(ids_obj))

            masked_logits = numpy.full_like(logits, -numpy.inf)
            masked_logits[allowed_id] = logits[allowed_id]

            valid = int(numpy.argmax(masked_logits))

            ids_obj.append(valid)

            if valid == dot:
                state = True

                if dot in allowed_id:
                    allowed_id.remove(dot)
                continue

            if state:
                count -= 1
                if count == 0:
                    break

    def generate_str(self, ids_obj: List[int]) -> None:
        escape = self.model.encode("\\").tolist()[0][0]
        quote = self.model.encode('"').tolist()[0][0]
        ids_obj.append(quote)

        while True:
            logits = numpy.array(self.model.get_logits_from_input_ids(ids_obj))
            valid = int(numpy.argmax(logits))
            decoded = self.model.decode(valid)
            if '"' in decoded and not ids_obj[-1] == escape:
                if "+" in decoded:
                    ids_obj.append(self.model.encode("+").tolist()[0][0])
                ids_obj.append(quote)
                break
            ids_obj.append(valid)

    def generate_bool(self, ids_obj: List[int]) -> None:
        true_ids = self.model.encode("true").tolist()[0]
        false_ids = self.model.encode("false").tolist()[0]

        logits = numpy.array(self.model.get_logits_from_input_ids(ids_obj))

        true_score = logits[true_ids[0]]
        false_score = logits[false_ids[0]]

        if true_score > false_score:
            ids_obj.extend(true_ids)
        else:
            ids_obj.extend(false_ids)
