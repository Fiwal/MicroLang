import time
from functools import wraps

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