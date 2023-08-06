from functools import reduce, partial
from typing import Callable

__all__ = (
    'compose',
    'pipe',
    'co',
    'partial',
)


def compose(*fns: Callable):
    assert len(fns) > 1
    funcs = list(reversed(fns))

    def composed_func(*args, **kwargs):
        init_value = funcs[0](*args, **kwargs)
        return reduce(lambda r, f: f(r), funcs[1:], init_value)

    return composed_func


co = compose


def pipe(*funcs: Callable):
    return compose(*reversed(funcs))
