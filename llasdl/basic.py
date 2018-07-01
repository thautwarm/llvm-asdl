from Redy.ADT.Core import data
from Redy.ADT import traits
from Redy.Magic.Classic import record


@data
class Constant(traits.Im, traits.ConsInd, traits.Dense):
    i1: lambda _: ('i1', _)
    i8: lambda _: ('i8', _)

    # unicode representation:  type { i32*, i64 }
    i32: lambda _: ('i32', _)

    i64: lambda _: ('i64', _)
    f32: lambda _: ('float', _)
    f64: lambda _: ('double', _)
    f128: lambda _: ('fp128', _)

    void: ('void',) *2


    def __str__(self):
        _, (ty, value) = self
        return f'{ty} {value}'

    def __repr__(self):
        _, (ty, value) = self
        return f'{ty}<{value}>'


class BooleanCompare:
    @data
    class Floating(traits.Im):
        """
        fcmp
        https://llvm.org/docs/LangRef.html#fcmp-instruction
        """
        OrderedEqual: 'oeq'
        OrderedGreaterThan: 'ogt'
        OrderedGreaterThanOrEqual: 'oge'
        OrderedLessThan: 'olt'
        OrderedLessThanOrEqual: 'ole'
        OrderedNotEqual: 'one'
        Ordered: 'ord'

        UnorderedEqual: 'ueq'
        UnorderedGreaterThan: 'ugt'
        UnorderedGreaterThanOrEqual: 'uge'
        UnorderedLessThan: 'ult'
        UnorderedLessThanOrEqual: 'ule'
        UnorderedNotEqual: 'une'
        Unordered: 'uno'

        def __str__(self):
            return f'fcmp {self.__inst_str__}'

    @data
    class Integral(traits.Im):
        """
        icmp
        https://llvm.org/docs/LangRef.html#icmp-instruction
        """
        Equal: 'eq'
        NotEqual: 'ne'
        UnsignedGreaterThan: 'ugt'
        UnsignedGreaterThanEqual: 'uge'
        UnsignedLessThan: 'ult'
        UnsignedLessThanEqual: 'ule'
        SignedGreaterThan: 'sgl'
        SignedGreaterThanEqual: 'sge'
        SignedLessThan: 'slt'
        SignedLessThanEqual: 'sle'

        def __str__(self):
            return f'icmp {self.__inst_str__}'


@data
class Other:
    """
    https://llvm.org/docs/LangRef.html#phi-instruction
    <result> = phi <ty> [ <val0>, <label0>], ...

    https://llvm.org/docs/LangRef.html#select-instruction
    <result> = select selty <cond>, <ty> <val1>, <ty> <val2>

    https://llvm.org/docs/LangRef.html#call-instruction
    <result> = [tail | musttail | notail ]
                call
                [fast-math flags]
                [cconv]
                [ret attrs]
                <ty>|<fnty>
                <fnptrval>(<function args>)
                [fn attrs]
                [ operand bundles ]
    """
    Phi: 'phi'
    Select: 'select'
    Call: 'casll'


@data
class Conversion(traits.Im):
    """
    See cast operations at http://llvm.org/docs/LangRef.html#constant-expressions
    """

    Truncating: 'trunc'
    ZeroExtending: 'zext'
    SignExtending: 'sext'
    FloatingTruncating: 'fptrunc'
    FloatingPointExtending: 'fpext'
    SignedIntToFloatingPoint: 'sitofp'
    FloatingPointToSignedInt: 'fptosi'
    FloatingPointToUnsignedInt: 'fptoui'
    PointerToInteger: 'ptrtoint'
    IntegerToPointer: 'inttoptr'
    Bitwise: 'bitcast'
    AddressSpace: 'addrspacecast'


class Vector:
    """
    https://llvm.org/docs/LangRef.html#vector-operations
    """
    @data
    class Manipulate(traits.Im):
        ExtractElement: 'extractelement'
        InsertElement: 'insertelement'
        ShuffleVector: 'shufflevector'


class Aggregate:
    """
    https://llvm.org/docs/LangRef.html#aggregate-operations
    """
    @data
    class Manipulate(traits.Im):
        ExtractValue: 'extractvalue'
        InsertValue: 'insertvalue'


@data
class Binary:
    """
    https://llvm.org/docs/LangRef.html#binary-operations
    """
    Add: 'add'
    FloatingAdd: 'fadd'
    Sub: 'sub'
    FloatingSub: 'fsub'
    Mul: 'mul'
    FloatingMul: 'fmul'

    UnsignedDiv: 'udiv'
    SignedDiv: 'sdiv'
    FloatingDiv: 'fdiv'

    UnsignedRemainder: 'urem'
    SignedRemmainder: 'srem'
    FloatingRemainder: 'frem'

    # """
    # https://llvm.org/docs/LangRef.html#bitwise-binary-operations
    # """
    ShiftLeft: 'shl'
    LeftShiftRight: 'lshr'
    ArithmeticShiftRight: 'ashr'

    And: 'and'
    Or: 'or'

    Xor: 'xor'




@data
class MemoryAccessAddressing(traits.Im):
    """
    missing supports:
        `LLVM Atomic Instructions and Concurrency`:
            https://llvm.org/docs/Atomics.html#llvm-atomic-instructions-and-concurrency-guide

    """

    Allocation: 'alloca'
    Load: 'load'
    Store: 'store'
    GEP: 'getelementptr'
    CompareExchange: 'cmpxchg'
    # guide: a ? predicate = value
    # monad could be applied here:
    #   let >>= monad predicate
    #      a >>= (changeTo value)

    BlockAddress: 'blockaddress'
    # blockaddress(@function, %block)
    # this is crucial to implement `yield` semantics.

    # howto:
    #   1. implement a struct {i8* address, T current_produced_item}
    #                   address is initialized as the head of generator function
    #   2. mark the address of block branches into the state.
    #       each branch indicates `yield` statement.
    #       each branch change the address to that of next branch.

    # pseudo code:
    #     type GeneratorState<T>{ Address adr,  T value }
    #     def f(GeneratorState<int> s):
    #             ; indirectbr i8* %2, [ label %.branch1, label %.branch2, label %.branch3, label %.done]

    #             ; .branch1:
    #             ; set s.adr = addressof(.branch2)
    #         yield 1  # s.value = 1
    #             ; goto .end
    #
    #             ; .branch2
    #             ; set s.addr = address_of(.branch3)
    #         yield 2  # s.value = 2
    #             ; goto end
    #
    #             ; .branch3
    #             ; set s.addr = address_of(.done)
    #         yield 3  # s.value = 3
    #             ; goto end
    #             ; .done
    #             ; raise err
    #             ; .end
    #             ; ret void


@data
class Terminator(traits.Im):
    """
    https://llvm.org/docs/LangRef.html#terminator-instructions
    """
    Return: 'ret'

    Branch: 'br'

    Switch: 'switch'

    IndirectBranch: 'indirectbr'

    Invoke: 'invoke'
    # invoke can handle exceptions !!!!
    #  if function invoking goes well, after that the state goes to branch `normal`
    #  else the state goes to branch 'exception'

    # and the call instruction is expected with no interruption.

    Resume: 'resume'

    LandingPad: 'landingpad'

    Unreachable: 'unreachable'

