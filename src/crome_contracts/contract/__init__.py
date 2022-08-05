from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto

from crome_logic.src.crome_logic.specification.temporal import LTL
from crome_logic.src.crome_logic.typeset import Typeset

from crome_contracts.src.crome_contracts.contract.conflicts_manager import find_inconsistencies_operation




class ContractOperation(Enum):
    """Contract can be the result of the following operations"""

    COMPOSITION = auto()
    CONJUNCTION = auto()
    MERGING = auto()
    QUOTIENT = auto()
    SEPARATION = auto()
    REFINEMENT = auto()
    DESIGNER = auto()


@dataclass(frozen=True)
class Contract:
    _guarantees: LTL
    _assumptions: LTL = LTL("TRUE")
    _unsaturated: bool = field(repr=False, default=True)

    _generated_by: ContractOperation = field(
        init=False, repr=False, default=ContractOperation.DESIGNER
    )
    _generators: set[Contract] | dict[str, Contract] | None = field(
        init=False, repr=False, default=None
    )
    _saturation: LTL | None = field(init=False, repr=False, default=None)

    def __post_init__(self):
        if self._unsaturated and not self.assumptions.is_valid:
            object.__setattr__(self, "_saturation", deepcopy(self._assumptions))

        """Check Feasibility"""
        if not (self._assumptions & self._guarantees).is_satisfiable:
            find_inconsistencies_operation(self)

    @classmethod
    def from_operation(
        cls,
        guarantees: LTL,
        assumptions: LTL,
        generated_by: ContractOperation,
        generators: set[Contract] | dict[str, Contract],
    ) -> Contract:
        new_contract = cls(
            _guarantees=guarantees, _assumptions=assumptions, _unsaturated=False
        )
        object.__setattr__(new_contract, "_generated_by", generated_by)
        object.__setattr__(new_contract, "_generators", generators)

        return new_contract

    @property
    def assumptions(self) -> LTL:
        return self._assumptions

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
    ) -> tuple[ContractOperation, set[Contract] | dict[str, Contract] | None]:
        return self._generated_by, self._generators

    def __str__(self):
        res: list[str] = []
        if not self.assumptions.is_true_expression:
            res.append("ASSUMPTIONS")
            res.append(f"\t{str(self.assumptions)}")
        if not self.guarantees.is_true_expression:
            res.append("GUARANTEES")
            res.append(f"\t{str(self.guarantees)}")
        return "\n".join(res)

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
