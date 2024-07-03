import copy
from itertools import combinations
from typing import Type
from Fields import RationalNumber
from Fields import GaloisField
from .polynomial import Polynomial
from .monomial import Monomial
from Ideals import polynomialReduce, getGroebnerBasis, Ideal, lexOrder, gradedLexOrder, leadingCoefficient
from NumberTheory import integerLCM, integerGCD

SUPPORTED_FIELDS = [RationalNumber, float, complex, GaloisField]
ZERO = Polynomial({}, None)


def one(field: Type, prime: int = None):
    """
    Returns
    -------
    The multiplicative identity of the given field.

    Raises
    ------
    ValueError: If the field is not supported.
    """
    if field == GaloisField:
        return GaloisField(1, prime)
    elif field == RationalNumber:
        return RationalNumber(1)
    elif field == float or field == complex:
        return 1
    else:
        raise ValueError("The field is not supported.")
    

def zero(field: Type, prime: int = None):
    """
    Returns
    -------
    The additive identity of the given field.

    Raises
    ------
    ValueError: If the field is not supported.
    """
    if field == GaloisField:
        return GaloisField(0, prime)
    elif field == RationalNumber:
        return RationalNumber(0)
    elif field == float or field == complex:
        return 0
    else:
        raise ValueError("The field is not supported.")


def defineVariable(var: str, field: Type = RationalNumber, prime: int = None):
    """
    Define a variable with the given name and field. If using GaloisField add prime.

    Raises
    ------
    ValueError: If the field is not supported.
    """
    if field not in SUPPORTED_FIELDS:
        raise ValueError("The field is not supported.")
    elif var not in Monomial.VARIABLES and var != Monomial.DUMMY:
        raise ValueError("The variable is not supported.")
    elif field == GaloisField and prime is None:
        raise ValueError("The prime must be given for GaloisField.")
    else:
        return Polynomial({Monomial({var: 1}): one(field, prime)}, field)
    

def elementarySymetricPolynomial(degree: int, variables: list[str], field: Type = RationalNumber, prime: int = None) -> Polynomial:
    """
    Returns
    -------
    Elementary symetric polynomial of given degree in variables. Note that e0 = 0 and ek = 0 for k > n.

    Raises
    ------
    ValueError: If the field is not supported.
    """
    if field not in SUPPORTED_FIELDS:
        raise ValueError("The field is not supported.")
    
    numberOfVariables = len(variables)
    if degree <= 0 or degree > numberOfVariables:
        return ZERO
        
    coefficients = {}
    subsets = list(combinations(list(range(numberOfVariables)), degree))
    binarySubsets = []

    for subset in subsets:
        binaryRepresentation = [1 if i in subset else 0 for i in range(numberOfVariables)]
        binarySubsets.append(tuple(binaryRepresentation))
        
    for binarySubset in binarySubsets:
        coefficients[Monomial.makeFromTuples(binarySubset, variables)] = one(field, prime)
        
    return Polynomial(coefficients, field)


def powerSumPolynomial(degree: int, variables: list[str], field: Type = RationalNumber, prime: int = None) -> Polynomial:
    """
    Returns
    -------
    Power sum polynomial of given degree pk = x1^k + x2^k + ... + xn^k
        
    Raises
    ------
    ValueError: If degree is non-positive or the field is not supported.
    """
    if field not in SUPPORTED_FIELDS:
        raise ValueError("The field is not supported.")
    elif degree <= 0:
        raise ValueError("Degree of power sum polynomial must be positive")
        
    result = {}
    for var in variables:
        exponent = Monomial({var: degree})
        result[exponent] = one(field, prime)
        
    return Polynomial(result, field)



def derivative(f: Polynomial, variable: str, order: int = 1) -> Polynomial:
    """
    Returns
    -------
    Order-th formal derivative of the polynomial f with respect to the variable.
        
    Raises
    ------
    ValueError: If order is negative.
    """
    if order < 0:
        raise ValueError("Order of derivative must be non-negative")
    elif f.isZeroPolynomial() or variable not in f.getVariables:
        return ZERO
    elif order == 0:
        return f
        
    def differentiate(g: Polynomial, variable: str) -> Polynomial:
        result = {}
        for monomial, coefficient in g.coefficients.items():
            if variable not in monomial.exponent:
                continue
            else:
                newCoefficient = coefficient * monomial.exponent[variable]
                newMonomial = copy.deepcopy(monomial)
                newMonomial.exponent[variable] -= 1
                if newMonomial.exponent[variable] == 0:
                    del newMonomial.exponent[variable]
                result[newMonomial] = newCoefficient

        return Polynomial(result, g.field)

    h = copy.deepcopy(f)
    while order > 0:
        h = differentiate(h, variable)
        order -= 1
    return h


def _lcm(f: Polynomial, g: Polynomial) -> Polynomial:
    """
    Returns
    -------
    Leat common multiple of two polynomials.

    Raises
    ------
    ValueError: If the polynomials are not over the same field.
    """
    field = f.field
    if field != g.field:
        raise ValueError("The polynomials must be over the same field.")
    if field == GaloisField:
        prime = f.getCoefficients()[list(f.getCoefficients().keys())[0]].prime
    else:
        prime = None
        
    variables = f.getVariables + g.getVariables
    variables = list(set(variables))
    variables = [Monomial.DUMMY] + variables
    t = defineVariable(Monomial.DUMMY, field, prime)
    G = getGroebnerBasis([t * f, (1 - t) * g], variables, lexOrder)
    variables.remove(Monomial.DUMMY)
    H = Ideal.eliminationIdeal(G, variables)
    return H[0]
    

def _gcd(f: Polynomial, g: Polynomial) -> Polynomial:
    """
    Returns
    -------
    Greatest common divisor of two polynomials.

    Raises
    ------
    ValueError: If the polynomials are not over the same field.
    """
    variables = f.getVariables + g.getVariables
    variables = list(set(variables))
    Q, r = polynomialReduce(f * g, [_lcm(f, g)], variables, lexOrder)
    return Q[0]


def polynomialGCD(*args: Polynomial) -> Polynomial:
    """
    Returns
    -------
    The greates common divisor of the provided polynomials.
        
    Raises
    ------
    ValueError: If no arguments are provided or one of the arguments is not polynomial or not all polynomials are over the same field.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided.")
    if not all(isinstance(arg, Polynomial) for arg in args):
        raise ValueError("All arguments must be polynomials.")
    if not all(arg.field == args[0].field for arg in args):
        raise ValueError("All arguments must be of the same field.")
    if len(args) == 1 and isinstance(args[0], (list, set)):
        args = tuple(args[0])

    result = args[0]
    for i in range(1, len(args)):
        result = _gcd(result, args[i])
    return normalizeCoefficients(result)


def polynomialLCM(*args: Polynomial) -> Polynomial:
    """
    Returns
    ------
    The least common multiple of the provided polynomials.

    Raises
    ------
    ValueError: If no arguments are provided or one of the arguments is not polynomial or not all polynomials are over the same field.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided.")
    if not all(isinstance(arg, Polynomial) for arg in args):
        raise ValueError("All arguments must be polynomials.")
    if not all(arg.field == args[0].field for arg in args):
        raise ValueError("All arguments must be of the same field.")
    if len(args) == 1 and isinstance(args[0], (list, set)):
        args = tuple(args[0])

    result = args[0]
    newLeadingCoefficient = leadingCoefficient(result, result.getVariables, gradedLexOrder)
    for i in range(1, len(args)):
        result = _lcm(result, args[i])
        newLeadingCoefficient *= leadingCoefficient(args[i], args[i].getVariables, gradedLexOrder)
    return result * (newLeadingCoefficient / leadingCoefficient(result, result.getVariables, gradedLexOrder))


def normalizeCoefficients(f: Polynomial, toIntegers: bool = False) -> Polynomial:
    """
    Returns
    -------
    The polynomial with normalized coefficients.

    If field is RationalNumber and toInteges is set then the coefficients will be relativly prime integers. Otherwise the coefficients will be normalized so that leading term with respect to alphabetical graded lex order is 1.
    """
    if f.field == RationalNumber and toIntegers:
        l = integerLCM(*[coefficient.denominator for coefficient in f.getCoefficients.values()])
        d = integerGCD(*[coefficient.numerator for coefficient in f.getCoefficients.values()])
        return f * (l / d)
    else:
        return f * (1 / leadingCoefficient(f, f.getVariables, gradedLexOrder))
    

def implicitization(F: dict[str, Polynomial]) -> list[Polynomial]:
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


def squareFreePart(f: Polynomial) -> Polynomial:
    """
    Returns
    -------
    The square free part of the polynomial f.

    Raises
    ------
    ValueError: If the field has nonzero characteristic.
    """
    if f.field == GaloisField:
        raise ValueError("The field must have characteristic 0.")
    
    grad = [derivative(f, var) for var in f.getVariables]
    grad += [f]
    d = polynomialGCD(*grad)
    Q, _ = polynomialReduce(f, [d], f.getVariables, lexOrder)
    return normalizeCoefficients(Q[0])