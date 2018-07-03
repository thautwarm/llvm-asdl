from Redy.Magic.Classic import record
from typing import List, Union


class ASDL:
    lineno: int
    colno: int

    def __str__(self):
        content = ','.join(
            f'{key}={getattr(self, key)}' for key in self.__annotations__.keys() if key not in ('lineno', 'colno'))
        return f'{self.__class__.__name__}({content})'


@record
class String(ASDL):
    lineno: int
    colno: int

    value: str


@record
class Number(ASDL):
    lineno: int
    colno: int

    value: Union[float, int]
    type: ASDL


@record
class Annotate(ASDL):
    lineno: int
    colno: int

    value: ASDL
    type: ASDL


@record
class Symbol(ASDL):
    lineno: int
    colno: int

    name: str


@record
class Define(ASDL):
    lineno: int
    colno: int

    name: str
    body: ASDL


@record
class Bind(ASDL):
    lineno: int
    colno: int

    name: str
    body: ASDL


@record
class Argument(ASDL):
    lineno: int
    colno: int

    name: str
    type: ASDL


@record
class Lambda(ASDL):
    lineno: int
    colno: int

    args: List[Argument]
    body: ASDL
    type: ASDL


@record
class FieldDecl(ASDL):
    lineno: int
    colno: int

    name: str
    type: ASDL


@record
class Struct(ASDL):
    lineno: int
    colno: int

    fields: List[FieldDecl]


@record
class Quote(ASDL):
    lineno: int
    colno: int

    value: ASDL


@record
class SExpr(ASDL):
    lineno: int
    colno: int

    seq: List[ASDL]
