from pydantic import BaseModel
from typing import Dict

class ValidatCalls(BaseModel):
    prompt: str

class Type(BaseModel):
    type: str

class ValidDefinitions(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Type]
    returns: Type