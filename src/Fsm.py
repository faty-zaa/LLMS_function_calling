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
    COMMA_P = auto()
    COMMA = auto()
    END_OBJ = auto()
    DONE = auto()
    RETURN = auto()
    ANSWER = auto()


class FSM:

    @classmethod
    def allowed_tokens(cls, state):
        allowed: str = None

        if state == State.START_ARR:
            allowed = "["

        if state == State.START_OBJ:
            allowed = "{"

        if state == State.NAME:
            allowed = "'name'"

        if state == State.PROMPT:
            allowed = "prompt"

        if state == State.ANSWER:
            allowed = None

        if state == State.PARAM:
            allowed = "parameters"

        if state == State.COLON:
            allowed = ":"

        if state == State.COMMA_P:
            allowed = ","

        if state == State.END_ARR:
            allowed = "]"

        if state == State.END_OBJ:
            allowed = "}"

        return allowed

    @classmethod
    def next_state_for_one_prompt(cls, state, i):
        if state == State.START_OBJ:
            state = State.PROMPT

        elif state == State.NAME or state == State.PARAM or state == State.PROMPT:
            state = State.COLON

        elif state == State.COLON:
            state = State.ANSWER

        elif state == State.ANSWER:
            if i < 2:
                state = State.COMMA_P
            else:
                state = State.END_OBJ

        elif state == State.COMMA_P:
            if i == 0:
                state = State.NAME
                i += 1
            elif i == 1:
                state = State.PARAM
                i += 1

        elif state == State.END_OBJ:
            state = State.DONE

        return state, i

    @classmethod
    def json_state(cls, state):
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
