from functools import cmp_to_key
from Polynomials import Monomial, Polynomial
from typing import Callable

def lexOrder(alpha: Monomial, beta: Monomial, permutation: list[str]) -> bool:
    """
    Returns
    -------
    -1 : if alpha < beta
    0  : if alpha = beta
    1  : if alpha > beta
        in lexicographic order given by permutation
    """
    for var in permutation:
        a = alpha.exponent.get(var, 0)
        b = beta.exponent.get(var, 0)
        
        if a < b:
            return -1
        elif a > b:
            return 1

    return 0


def gradedLexOrder(alpha: Monomial, beta: Monomial, permutation: list[str]) -> bool:
    """
    Returns
    -------
    -1 : if alpha < beta
    0  : if alpha = beta
    1  : if alpha > beta
        in graded lexicographic order given by permutation
    """
    if alpha.degree() < beta.degree():
        return -1
    elif alpha.degree() > beta.degree():
        return 1
    else:
        return lexOrder(alpha, beta, permutation)
    

def leadingMonomial(f: Polynomial, permutation: list[str], order: Callable = lexOrder) -> Monomial:
    """
    Returns
    -------
    Leading monomial of the polynomial f with respect to the monomial order given by permutation
    """
    if not f.coefficients:
        return None

    key_function = cmp_to_key(lambda alpha, beta: order(alpha, beta, permutation))
    return max(f.coefficients.keys(), key=key_function)


def leadingCoefficient(f: Polynomial, permutation: list[str], order: Callable = lexOrder):
    """
    Returns
    -------
    Leading coefficient of the polynomial f with respect to the monomial order given by permutation
    """
    return f.coefficients.get(leadingMonomial(f, permutation, order), 0)


def monomialOrder(alpha: Monomial, beta: Monomial, permutation: list[str], order: Callable = lexOrder) -> bool:
    """
    Returns
    -------
    -1 : if alpha < beta
    0  : if alpha = beta
    1  : if alpha > beta
        in monomial order given by permutation
    """
    return order(alpha, beta, permutation)