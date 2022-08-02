from crome_contracts.contract import Contract


def concretization(contracts: set[Contract]) -> set[Contract]:
    if len(contracts) == 1:
        return contracts
    if len(contracts) == 0:
        raise Exception("No contract specified in the concretization")
    #TODO: to implement
    pass
