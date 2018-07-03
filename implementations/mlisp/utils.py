from rbnf.Tokenizer import Tokenizer
from .asdl import *

join_str = ''.join


def try_test(f, exc):
    try:
        return f()
    except exc:
        return False


def map_value(token_seq: List[Tokenizer]):
    return map(lambda _: _.value, token_seq)


def loc(n: Tokenizer):
    return n.lineno, n.colno


def typed_num_from_token(n: Tokenizer):
    i = eval(n.value)
    ty = Symbol(-1, -1, "builtin.i64" if isinstance(i, int) else "builtin.f64")
    return Number(*loc(n), i, ty)
