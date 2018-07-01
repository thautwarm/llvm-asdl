
from Redy.Magic.Classic import record

from Redy.ADT.Core import data
from Redy.ADT import traits
from typing import Tuple, TypeVar
T = TypeVar('T')
List = Tuple[T, ...]

class ASDL:
    pass



@data
class Expr(ASDL):
    value: ...

@record
class Symbol(ASDL):
    lineno: int
    colno: int

    name: Expr

@record
class Assign(ASDL):
    lineno: int
    colno: int

    symbol: Symbol
    value: List[Expr]

@data
class Const(ASDL, traits.Im, traits.ConsInd, traits.Dense):
    pass

@record
class FuncCall(ASDL):
    lineno: int
    colno: int

    fn: Expr
    args: List[Expr]

@record
class External(ASDL):
    lineno: int
    colno: int

    symbol: Symbol
    where: str


@record
class BinOp(ASDL):
    lineno: int
    colno: int
    op: str
    left: Expr
    right: Expr


@record
class FuncDef(ASDL):
    """
    define anonymous functions
    """
    lineno: int
    colno: int

    args: List[Expr]
    expr: Expr


@record
class ExceptionHandling(ASDL):
    """
    when applying the `entry` block,

    if any exception raised, try to use `capture_cases` blocks to handle it.
        each case has a pattern to match exception, and a block for handling
        exceptions if the pattern matched

    if there is a final block, no matter what happened above it, block of final must be handled.
    """
    lineno: int
    colno: int

    entry: Expr

    capture_cases: List[Tuple[Expr, Expr]]
    final: Expr

@record
class Declaration(ASDL):
    lineno: int
    colno: int
    name: str
    type: Type
    default_value: Expr


@record
class StructureDef(ASDL):
    """
    the fields of struct are multiple declarations.
    """
    lineno: int
    colno: int

    name: str
    fields: List[Declaration]

@record
class Block(ASDL):
    sequence: List[Expr]

@data
class Type(ASDL):
    Undecided: lambda undecided_fn: ...
    Concrete:  lambda concrete_sets: ...
    Basic: lambda _: ...
