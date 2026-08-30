from enum import Enum

class NameType(Enum):
    FUNCTION = 1
    INT_VARIABLE = 2
    INT_NUM = 3
    STRING_VARIABLE = 4
    PARAMETER = 5
    RETURN_VALUE = 6
    NOT_FOUND = 7