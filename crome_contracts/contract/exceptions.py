from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContractException(Exception):
    message: str

    def __post_init__(self):
        header = "*** CONTRACT EXCEPTION ***"
        print(f"{header}\n{self.message}")
