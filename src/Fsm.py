from enum import Enum, auto
from typing import Dict


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


class FSM:

    @classmethod
    def allowed_tokens(cls, state):
        allowed: str = ""

        if state == State.START_ARR:
            allowed = "["

        if state == State.START_OBJ:
            allowed = "{"

        if state == State.NAME:
            allowed = "name"

        if state == State.PROMPT:
            allowed = "prompt"

        if state == State.PARAM:
            allowed = "parameters"

        if state == State.COLON:
            allowed = ":"

        if state == State.COMMA:
            allowed = ","

        if state == State.END_ARR:
            allowed = "]"

        if state == State.END_OBJ:
            allowed = "}"

        return allowed

    @classmethod
    def next_state_for_one_prompt(cls, state):

        if state == State.START_OBJ:
            state = State.PROMPT

        if state in [State.PROMPT, State.NAME, State.PARAM]:
            state = State.COLON

        if state == State.END_OBJ:
            state = State.DONE

        return state

    @classmethod
    def json_state(cls, state):
        if state == State.START_ARR:
            state = State.OBJ

        if state == State.OBJ:
            state = State.COMMA

        if state == State.COMMA:
            state = State.OBJ

        if state == State.DONE:
            state = State.END_ARR

        if state == State.END_ARR:
            state = State.RETURN
