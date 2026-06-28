from enum import Enum, auto
from typing import Dict, Union, Optional


class State(Enum):
    START_ARR: int = auto()
    OBJ: int = auto()
    END_ARR: int = auto()
    START_OBJ: int = auto()
    NAME: int = auto()
    PROMPT: int = auto()
    PARAM: int = auto()
    COLON: int = auto()
    COMMA_P: int = auto()
    COMMA: int = auto()
    END_OBJ: int = auto()
    DONE: int = auto()
    RETURN: int = auto()
    FUN_NAME: int = auto()
    USER_PROMT: int = auto()
    PARAMS: int = auto()


class FSM:

    @classmethod
    def allowed_tokens(cls, state: State) -> Optional[str | None]:
        allowed: Optional[str | None] = None

        if state == State.START_ARR:
            allowed = "["

        elif state == State.START_OBJ:
            allowed = "{"

        elif state == State.NAME:
            allowed = "'name': "

        elif state == State.PROMPT:
            allowed = "'prompt': "

        elif state == State.USER_PROMT:
            allowed = "0"
        
        elif state == State.FUN_NAME:
            allowed = "1"
        
        elif state == State.PARAMS:
            allowed = "2"
            
        elif state == State.PARAM:
            allowed = "'parameters': "

        elif state == State.COLON:
            allowed = ":"

        elif state == State.COMMA_P:
            allowed = ","

        elif state == State.END_ARR:
            allowed = "]"

        elif state == State.END_OBJ:
            allowed = "}"

        return allowed

    @classmethod
    def next_state_for_one_prompt(cls, state: State) -> State:
        if state == State.START_OBJ:
            state = State.PROMPT

        elif state == State.PROMPT:
            state =  State.USER_PROMT
        
        elif state == State.USER_PROMT:
            state = State.NAME

        elif state == State.NAME:
            state = State.FUN_NAME

        elif state == State.FUN_NAME:
            state = State.PARAM

        elif state == State.PARAM:
            state = State.PARAMS

        elif state == State.PARAMS:
            state = State.END_OBJ

        elif state == State.END_OBJ:
            state = State.DONE

        return state

    @classmethod
    def json_state(cls, state: State) -> State:
        
        if state == State.START_ARR:
            state = State.OBJ
        elif state == State.OBJ:
            state = State.COMMA

        elif state == State.COMMA:
            state = State.OBJ

        elif state == State.DONE:
            state = State.END_ARR

        elif state == State.END_ARR:
            state = State.RETURN

        return state
