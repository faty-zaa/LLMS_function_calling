from enum import Enum, auto
from typing import Optional


class State(Enum):
    START_ARR = auto()
    OBJ = auto()
    END_ARR = auto()
    START_OBJ = auto()
    NAME = auto()
    PROMPT = auto()
    PARAM = auto()
    COLON = auto()
    COMMA = auto()
    END_OBJ = auto()
    DONE = auto()
    RETURN = auto()
    FUN_NAME = auto()
    USER_PROMT = auto()
    PARAMS = auto()


class FSM:

    @classmethod
    def allowed_tokens(cls, state: State) -> Optional[str | None]:
        allowed: Optional[str | None] = None

        if state == State.START_ARR:
            allowed = "["

        elif state == State.START_OBJ:
            allowed = "{"

        elif state == State.NAME:
            allowed = '"name": '

        elif state == State.PROMPT:
            allowed = '"prompt": '

        elif state == State.USER_PROMT:
            allowed = "user_prompt"

        elif state == State.FUN_NAME:
            allowed = "fn_name"

        elif state == State.PARAMS:
            allowed = "params"

        elif state == State.PARAM:
            allowed = '"parameters": '

        elif state == State.COLON:
            allowed = ":"

        elif state == State.COMMA:
            allowed = ","

        elif state == State.OBJ:
            allowed = "obj"

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
            state = State.USER_PROMT

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

        elif state == State.END_ARR:
            state = State.RETURN

        return state
