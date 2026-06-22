from enum import Enum

class State(Enum):
    START_ARR: str
    OBJ_OR_END: str
    START_OBJ: str
    KEY: str
    COLON: str
    VALUE: str
    COMMA: str
    COMMA_OR_ENDOBJ: str
    COMMA_OR_ENARR: str
    END_OBJ: str
    END_ARR: str

class FSM:
    pass