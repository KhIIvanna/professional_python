from functools import wraps
from time import perf_counter
from typing import Callable, Any

def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure execution time of a function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"[BENCHMARK] {func.__name__} executed in: {elapsed:.8f} sec")
        return result
    return wrapper