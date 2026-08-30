import time
from functools import wraps
from src.enums.name_type import NameType


def measure_time(msg):
    def measure_time_real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            start = time.perf_counter()
            return_value = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Done - {((end - start) * 1000):.5f}ms")
            return return_value
        return wrapper
    return measure_time_real_decorator

KEYWORDS = ["FN", "ENDFN", "return", "name_parameter", "IF", "ELSE", "ENDIF", "LOOP", "ENDLOOP",
            "break", "int", "string", "print", "print_int", "input_int", "add", "sub", "mul",
            "div", "mod", "set", "return_value"]


def is_valid_name(name):
    return False if isinstance(name, int) or name in KEYWORDS or not name.isidentifier() else True


def check_name(name, ast, current_function):
    if isinstance(name, int):
        return NameType.INT_NUM

    for function in ast["functions"]:
        if function.name == name:
            return NameType.FUNCTION

    for var in ast["initialized_global_variables"]:
        if var["name"] == name:
            if var["type"] == "int":
                return NameType.INT_VARIABLE
            if var["type"] == "string":
                return NameType.STRING_VARIABLE

    for var in ast["uninitialized_global_variables"]:
        if var["name"] == name:
            if var["type"] == "int":
                return NameType.INT_VARIABLE

    for var in current_function.local_variables:
        if var == name:
            return NameType.INT_VARIABLE

    for parameter in current_function.parameters:
        if parameter == name:
            return NameType.PARAMETER

    for i in range(0, 6):
        if name == f"parameter_{i}":
            return NameType.PARAMETER

    if name == "return_value":
        return NameType.RETURN_VALUE

    return NameType.NOT_FOUND
