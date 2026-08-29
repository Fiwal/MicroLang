import time
from functools import wraps


def print_msg_and_measure_time(msg):
    def print_msg_and_measure_time_real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            start = time.perf_counter()
            return_value = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Done - {((end - start) * 1000):.5f}ms")
            return return_value
        return wrapper
    return print_msg_and_measure_time_real_decorator

KEYWORDS = ["FN", "ENDFN", "return", "name_parameter", "IF", "ELSE", "ENDIF", "LOOP", "ENDLOOP",
            "break", "int", "string", "print", "print_int", "input_int", "add", "sub", "mul",
            "div", "mod", "set", "return_value"]

def is_valid_name(name):
    return False if isinstance(name, int) or name in KEYWORDS or not name.isidentifier() else True