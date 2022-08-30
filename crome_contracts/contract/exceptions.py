from __future__ import annotations

from dataclasses import dataclass

from crome_contracts.contract import Contract


@dataclass
class ContractException(Exception):
    contracts: set[Contract]

    def __post_init__(self):
        contracts_str = "\n\n".join(repr(c) for c in self.contracts)
        print(
            "*** ContractException EXCEPTION ***\n"
            f"A failure has occurred on contracts:\n {contracts_str}"
        )
