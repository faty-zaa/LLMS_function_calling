from .functions import Functions
from typing import List, Dict
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model

@dataclass
class Get:

    functions_data: Dict
    model: Small_LLM_Model

    @property
    def get_name(self) -> List[str]:
        fun_names = [
            self.model.encode(Functions(self.functions_data[i]).name).tolist()[0]
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
            Functions(self.functions_data[i]).description
            for i in range(len(self.functions_data))
        ]
        return fun_desc
