import copy
from typing import Callable
from tqdm import tqdm
from .polynomial import Polynomial, Monomial
from .monomialOrders import lexOrder, leadingMonomial, leadingCoefficient

def polynomialReduce(f: Polynomial, G: list[Polynomial], permutation: list[str], order: Callable
= lexOrder) -> tuple[list[Polynomial], Polynomial]:
    """
    Division algorithm of f by G = [g1, g2, ..., gs] using monomial order given by permutation.

    Returns
    -------
    ([q1, q2, ..., qs], r) : q are quotients and r is not divisble by all leading terms of G.
    """
    field = f.field
    p = copy.deepcopy(f)
    r = Polynomial({}, field)
    quotients = [Polynomial({}, field) for _ in range(len(G))]
    G_monomials_list = [leadingMonomial(g, permutation, order) for g in G]
    G_leading_coefficients = [leadingCoefficient(g, permutation, order) for g in G]

    while not p.isZeroPolynomial():
        p_monomial = leadingMonomial(p, permutation, order)
        p_coefficient = leadingCoefficient(p, permutation, order)
        somethingDivided = False

        for i, g in enumerate(G):
            try:
                power = p_monomial / G_monomials_list[i]
                coefficient = p_coefficient / G_leading_coefficients[i]
                quotients[i] += Polynomial({power: coefficient}, field)
                p -= Polynomial({power: coefficient}, field) * g
                somethingDivided = True
                break  
            
            except ValueError:
                pass
        

        if not somethingDivided:
            r += Polynomial({p_monomial: p_coefficient}, field)
            p -= Polynomial({p_monomial: p_coefficient}, field)

    return quotients, r


def syzygy(f: Polynomial, g: Polynomial, permutation: list[str], order: Callable
 = lexOrder) -> Polynomial:
    """
    Returns
    -------
    S(f, g) = lcm(LT(f), LT(g)) / LT(f) * f - lcm(LT(f), LT(g)) / LT(g) * g

    lcm is least common multiple of monomials, leading terms are calcualted based on monomial order given by permutation.
    """
    f_monomial = leadingMonomial(f, permutation, order)
    f_coefficient = leadingCoefficient(f, permutation, order)
    g_monomial = leadingMonomial(g, permutation, order)
    g_coefficient = leadingCoefficient(g, permutation, order)
    m = Monomial.leastCommonMultiple(f_monomial, g_monomial)
    a = Polynomial({m / f_monomial: 1 / f_coefficient}, f.field)
    b = Polynomial({m / g_monomial: 1 / g_coefficient}, g.field)
    return a * f - b * g


def extendToGroebnerBasis(Basis: list[Polynomial], permutation = list[str], order: Callable
 = lexOrder) -> list[Polynomial]:
    """
    Returns
    -------
    Extends a given basis to a Groebner basis using Buchberger's algorithm. Monomial order is determined by permuation.
    """
    G = list(Basis)
    while True: 
        H = list(G)
        for i in range(len(G)):
            for j in range(i + 1, len(G)):
                if not lcmCriterion(leadingMonomial(G[i], permutation, order), leadingMonomial(G[j], permutation, order)) and not chainCriterion(i, j, G, permutation):
                    _, r = polynomialReduce(syzygy(G[i], G[j], permutation, order), G, permutation, order)
                    if not r.isZeroPolynomial():
                        H.append(r)

        if len(G) == len(H):
            # print(f'Groebner basis size when exiting: {len(G)}')
            return H
        else:
            G = H
            # print(f'Groebner basis size: {len(G)}')


def lcmCriterion(alpha: Monomial, beta: Monomial) -> bool:
    """
    Returns
    -------
    True if monomials are relativly prime that is their prdouct is equal to their least common multiple, False otherwise. 
    """
    return Monomial.leastCommonMultiple(alpha, beta) == alpha * beta


def chainCriterion(i: int, j: int, G: list[Polynomial], permutation: list[str], order: Callable
 = lexOrder) -> bool:
    """
    Returns
    -------
    True if the pair (i, j) , i < j is critical that is there is k not equal to i and j such LT(G[k]) | lcm(LT(G[i]), LT(G[j])), and pairs (i, k), (j, k) have been already checked in Buchberger's algorithm. False otherwise. 
    """
    for k in range(j + 1, len(G)):
        try:
            _ = Monomial.leastCommonMultiple(leadingMonomial(G[i], permutation, order), leadingMonomial(G[j], permutation)) / leadingMonomial(G[k], permutation, order)
            return True
        except ValueError:
            pass
    return False


def isInLeadingTermsIdeal(f: Polynomial, G: list[Polynomial], permutation = list[str], order: Callable
 = lexOrder) -> bool:
    """
    Returns
    -------
    True if f is in the ideal generated by leading terms of G, False otherwise.
    """
    for g in G:
        try:
            _ = leadingMonomial(f, permutation, order) / leadingMonomial(g, permutation, order)
            return True
        except ValueError:
            pass
    return False



def reduceGroebnerBasis(G: list[Polynomial], permutation: list[str], order: Callable
 = lexOrder, normalizeCoefficients: bool = True) -> list[Polynomial]:
    """
    Returns
    -------
    Reduces a Groebner basis to a minimal Groebner basis, that is:
    1. For each g in G, g is not divisible by leading terms of other polynomials in G.
    2. For each g in G, g is reduced by other polynomials in G.
    3. If normalizeCoefficients is True, each polynomial is divided by it's leading coefficient.
    """
    H = list(G)
    for g in G:
        H.remove(g)
        if not isInLeadingTermsIdeal(g, H, permutation, order):
            H.append(g)

    s = len(H)
    counter = 0
    while counter < s:

        counter = 0
        for i, h in enumerate(H):
            F = list(H)
            F.remove(h)
            _, r = polynomialReduce(h, F, permutation, order)
            H[i] = r

            if r == h:
                counter += 1

    if normalizeCoefficients:
        for i, h in enumerate(H):
            H[i] *= 1 / leadingCoefficient(h, permutation, order)

    return H


def getGroebnerBasis(G: list[Polynomial], permutation: list[str], order: Callable
 = lexOrder, normalizeCoefficients: bool = True) -> list[Polynomial]:
    """
    Returns
    -------
    The minimal Groebner basis for a given ideal generated by G using Buchberger's algorithm with respect to monomial order given by permutation.
    """
    return reduceGroebnerBasis(extendToGroebnerBasis(G, permutation, order), permutation, order, normalizeCoefficients)