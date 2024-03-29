from copy import deepcopy

from crome_contracts.contract import Contract, ContractOperation


def merging(contracts: set[Contract]) -> Contract:
    if len(contracts) == 1:
        return next(iter(contracts))
    if len(contracts) == 0:
        raise Exception("No contract specified in the merging")

    contract_list = list(contracts)
    new_assumptions = deepcopy(contract_list[0].assumptions)
    new_guarantees = deepcopy(contract_list[0].guarantees)

    for contract in contract_list[1:]:
        new_assumptions &= contract.assumptions
        new_guarantees &= contract.guarantees

    new_guarantees = new_guarantees | ~new_assumptions

    return Contract.from_operation(
        guarantees=new_guarantees,
        assumptions=new_assumptions,
        generated_by=ContractOperation.MERGING,
        generators=contracts,
    )
