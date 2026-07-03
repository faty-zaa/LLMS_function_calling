from pydantic import BaseModel, ValidationError
from typing import Dict, List, Any
from dataclasses import dataclass
from .Parse_args import ArgParse
from argparse import Namespace
import json


class ValidatCalls(BaseModel):
    prompt: str


class Type(BaseModel):
    type: str


class ValidDefinitions(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Type]
    returns: Type


@dataclass
class Parser:
    args: Namespace

    @property
    def parse_prompt_data(self) -> List[Dict[str, str]]:
        with open(self.args.input, "r") as file1:
            try:
                prompt_data: List[Dict[str, str]] = json.load(file1)
                _ = [ValidatCalls.model_validate(i) for i in prompt_data]
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
                raise
            except ValidationError as e:
                print("Invalid schema:")
                print(e)
                raise
        return prompt_data

    @property
    def parse_func_definitions_data(self) -> List[Dict[str, Any]]:
        with open(self.args.functions_definition, "r") as file2:
            try:
                func_data: List[Dict[str, Any]] = json.load(file2)
                _ = [ValidDefinitions.model_validate(j) for j in func_data]
            except json.JSONDecodeError as e:
                print("Invalid JSON:", e)
                raise ValueError
        return func_data
