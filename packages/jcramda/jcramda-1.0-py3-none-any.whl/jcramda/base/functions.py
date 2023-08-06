from more_itertools import repeatfunc, zip_equal

from jcramda.core import curry, of, map_

__all__ = (
    'applyto',
    'converge',
    'juxt',
    'call_until',
    'f_digest',
    'repeat_call',
    'use_with',
    'pair_call',
    'use_with',
)


class applyto:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kw = kwargs

    def __call__(self, fn):
        return fn(*self._args, **self._kw)


def juxt(*funcs):
    """
    call some functions with a same param value.
    :param funcs:
    :return: a list with functions call result
    """
    def juxt_w(*args, **kwargs):
        return map_(applyto(*args, **kwargs), funcs)

    return juxt_w


@curry
def call_until(pred, funcs, v, *args, **kwargs):
    for func in funcs:
        r = func(v, *args, **kwargs)
        if pred(r):
            return r
    return None


def f_digest(f):
    from inspect import signature
    from pickle import dumps
    from .text import hexdigest
    return hexdigest('sha256', dumps(signature(f)))


@curry
def converge(after_f, funcs, value):
    """
    (g, [f1, f2, ... fn], value) -> g(f1(value), f2(value), ... fn(value))
    :param after_f: 最终处理函数
    :param funcs: 函数列表
    :param value: 要处理的值
    :return:
    """
    return after_f(*juxt(*funcs)(value))


repeat_call = curry(repeatfunc)


@curry
def pair_call(funcs, v, *args):
    values = of(v, args)
    return (f(*of(x)) for (f, x) in zip_equal(funcs, values))


@curry
def use_with(after_f, funcs, v, *args):
    return after_f(*pair_call(funcs, v, *args))
