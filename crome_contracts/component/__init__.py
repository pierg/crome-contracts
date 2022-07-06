from __future__ import annotations

from dataclasses import dataclass

from crome_contracts.contract import Contract
from crome_logic.typeset import Typeset


@dataclass(frozen=True)
class Component:
    _name: str
    _description: str = ""
    _inputs: Typeset
    _outputs: Typeset
    _contracts: set[Contract]

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def inputs(self) -> Typeset:
        return self._inputs

    @property
    def outputs(self) -> Typeset:
        return self._outputs

    @property
    def contracts(self) -> set[Contract]:
        return self._contracts
