from .functions import Functions
from typing import List, Dict, Any
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model


@dataclass
class Get:

    functions_data: List[Dict[str, Any]]
    model: Small_LLM_Model

    @property
    def get_name(self) -> List[List[int]]:
        fun_names = [
            self.model.encode(Functions(self.functions_data[i]).name).tolist()[
                0
            ]
            for i in range(len(self.functions_data))
        ]
        return fun_names

    @property
    def get_valid_params(self) -> List[Dict[str, str]]:
        fun_params = [
            Functions(self.functions_data[i]).parameters
            for i in range(len(self.functions_data))
        ]
        return fun_params

    @property
    def get_description(self) -> List[str]:
        fun_desc = [
            Functions(self.functions_data[i]).description
            for i in range(len(self.functions_data))
        ]
        return fun_desc
