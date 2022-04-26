from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto

from crome_logic.specification.temporal import LTL
from crome_logic.specification.temporal.conflicts_manager import find_inconsistencies
from crome_logic.typeset import Typeset

from crome_contracts.contract.conflicts_manager import find_inconsistencies_operation


class Contract:
    class Operation(Enum):
        """Contract can be the result of the following operations"""

        COMPOSITION = auto()
        CONJUNCTION = auto()
        MERGING = auto()
        QUOTIENT = auto()
        SEPARATION = auto()
        REFINEMENT = auto()
        DESIGNER = auto()

    def __init__(
        self,
        guarantees: LTL,
        assumptions: LTL = LTL("TRUE"),
        unsaturated: bool = True,
        generated_from: Operation = Operation.DESIGNER,
        generators: set[Contract] | dict[str, Contract] | None = None,
    ):

        self._assumptions: LTL = deepcopy(assumptions)
        if unsaturated:
            self._saturation: LTL = deepcopy(assumptions)
        else:
            self._saturation = None
        self._guarantees: LTL = deepcopy(guarantees)

        self._generated_op: Contract.Operation = generated_from
        self._generators: set[Contract] | dict[str, Contract] | None = generators

        """Check Feasibility"""
        if not (self._assumptions & self._guarantees).is_satisfiable:
            find_inconsistencies_operation(self)

    @property
    def assumptions(self) -> LTL:
        return self._assumptions

    @assumptions.setter
    def assumptions(self, value: LTL):
        """Check Feasibility"""
        if value >= self._assumptions:
            self._assumptions = deepcopy(value)
            return
        if not (value & self._guarantees).is_satisfiable:
            find_inconsistencies({value, self._guarantees})

    @property
    def guarantees(self) -> LTL:
        """Returning saturated guarantee."""
        if self._saturation is not None:
            return self._saturation >> self._guarantees
        else:
            return self._guarantees

    @property
    def unsaturated_guarantees(self) -> LTL:
        """Returning unsaturated saturated guarantee."""
        return self._guarantees

    @property
    def typeset(self) -> Typeset:
        return self._guarantees.typeset + self._assumptions.typeset

    @property
    def generators(
        self,
    ) -> tuple[Contract.Operation, set[Contract] | dict[str, Contract] | None]:
        return self._generated_op, self._generators

    def __str__(self):
        ret = "--ASSUMPTIONS--\n"
        ret += str(self.assumptions)
        ret += "\n--GUARANTEES--\n"
        ret += str(self.guarantees)
        return ret

    """Refinement"""

    def __le__(self: Contract, other: Contract):
        """self <= other.

        True if self is a refinement of other
        """
        cond_a = self.assumptions >= other.assumptions
        cond_g = self.guarantees <= other.guarantees
        return cond_a and cond_g

    def __eq__(self: Contract, other: object):
        """self == other.

        True if self is a refinement of other and viceversa
        """
        if not isinstance(other, Contract):
            return NotImplemented
        cond_a = self <= other
        cond_g = other <= self
        return cond_a and cond_g

    def __hash__(self):
        return hash(f"{str(self.assumptions)} -> {str(self.guarantees)}")

    def __repr__(self):
        return f"{str(self.assumptions)} -> {str(self.guarantees)}"
