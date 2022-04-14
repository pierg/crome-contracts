from copy import deepcopy

from crome_contracts.contract import Contract


def composition(contracts: set[Contract]) -> Contract:
    if len(contracts) == 1:
        return next(iter(contracts))
    if len(contracts) == 0:
        raise Exception("No contract specified in the composition")

    contract_list = list(contracts)
    new_assumptions = deepcopy(contract_list[0].assumptions)
    new_guarantees = deepcopy(contract_list[0].guarantees)

    for contract in contract_list[1:]:
        new_assumptions &= contract.assumptions
        new_guarantees &= contract.guarantees

    new_assumptions |= ~new_guarantees

    return Contract(
        guarantees=new_guarantees,
        assumptions=new_assumptions,
        unsaturated=False,
        generated_from=Contract.Operation.COMPOSITION,
        generators=contracts,
    )
