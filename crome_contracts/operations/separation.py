from crome_contracts.contract import Contract


def separation(dividend: Contract, divisor: Contract) -> Contract:
    if dividend is None:
        raise Exception("No dividend specified in the separation")
    if divisor is None:
        raise Exception("No divisor specified in the separation")

    c = dividend
    a = c.assumptions
    g = c.guarantees

    c1 = divisor
    a1 = c1.assumptions
    g1 = c1.guarantees

    a2 = a & g1 | ~(g & a1)
    g2 = g & a1

    return Contract(
        guarantees=g2,
        assumptions=a2,
        unsaturated=False,
        generated_from=Contract.Operation.SEPARATION,
        generators={"dividend": dividend, "divisor": divisor},
    )
