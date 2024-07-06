
from .galoisField import GaloisField
from .polynomial import Polynomial
from .monomial import Monomial
from .ideal import Ideal
from .monomialOrders import lexOrder
from .groebnerBasis import getGroebnerBasis
from .rationalFunction import RationalFunction
from .polynomialMethods import defineVariable, normalizeCoefficients, ZERO


def polynomialImplicitization(F: dict[str, Polynomial]) -> list[Polynomial]:
    """
    Returns
    -------
    The implicit equations of the variety defined by the polynomials F. For example {'x': u * v, 'y': v, 'z': u ** 2} will return [y²z - x²]

    Raises
    ------
    ValueError: If the field has nonzero characteristic.
    """
    if F == {}:
        return [ZERO]
    if list(F.values())[0].field == GaloisField:
        raise ValueError("The field must have characteristic 0.")
    
    parameters = list(set(sum([f.getVariables for f in F.values()], [])))
    variables = list(F.keys())
    coordinates = [defineVariable(var) for var in variables]
    G = getGroebnerBasis([f - var for f, var in zip(F.values(), coordinates)], parameters + variables, lexOrder)
    H = Ideal.eliminationIdeal(G, variables)
    return [normalizeCoefficients(h, toIntegers=True) for h in H]


def rationalImplicitization(F: dict[str, RationalFunction]) -> list[RationalFunction]: 
    """
    Returns
    -------
    The implicit equations of the variety defined by the rational functions F. For example {'x': (1 - t ** 2) / (1 + t ** 2), 'y': (2t) / (1 + t ** 2)} will return [x² + y² - 1]

    Raises
    ------
    ValueError: If the field has nonzero characteristic.
    """
    if F == {}:
        return [ZERO]
    if list(F.values())[0].field == GaloisField:
        raise ValueError("The field must have characteristic 0.")
    
    parameters = list(set(sum([f.getVariables for f in F.values()], [])))
    variables = list(F.keys())
    coordinates = [defineVariable(var) for var in variables]
    y = defineVariable(Monomial.DUMMY, F[variables[0]].field)
    prod = y
    for f in F.values():
        prod *= f.denominator
    prod = 1 - prod
    G = getGroebnerBasis([f.numerator - var * f.denominator for f, var in zip(F.values(), coordinates)] + [prod], [Monomial.DUMMY] + parameters + variables, lexOrder)
    H = Ideal.eliminationIdeal(G, variables)
    return [normalizeCoefficients(h, toIntegers=True) for h in H]