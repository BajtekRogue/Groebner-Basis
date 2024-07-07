
from itertools import combinations
import numpy as np
from .rational import rational
from .galoisField import GaloisField
from .polynomial import Polynomial
from NumberTheory import integerLCM, divisors


def findRoots(f: Polynomial) -> list:
    """
    Returns
    -------
    The roots of the polynomial f.

    Raises
    ------
    ValueError: If the polynomial is not univariate.
    """
    var = f.getVariables
    if len(var) > 1:
        raise ValueError("The polynomial must be univariate.")

    if f.field == rational:
        return rationalRoots(f)
    elif f.field == GaloisField:
        return galoisFieldRoots(f)
    elif f.field == float:
        return floatRoots(f)
    elif f.field == complex:
        return complexRoots(f)
    else:
        return None


def rationalRoots(f: Polynomial) -> list[rational]:
    """
    Returns
    -------
    The rational roots of the polynomial f using rational root theorem.
    """
    g = f * integerLCM([c.denominator for c in f.coefficients.values()])
    g.sortCoefficients()
    var = g.getVariables[0]
    u = int(list(g.coefficients.items())[0][1])
    v = int(list(g.coefficients.items())[-1][1])
    P = divisors(u)
    Q = divisors(v)
    positive = [rational(q, p) for q in Q for p in P]
    negative = [rational(-q, p) for q in Q for p in P]
    candidates = list(set(positive + negative)) + [rational(0)]
    print(candidates)
    return [r for r in candidates if g.evaluate({var: r})== 0]


def galoisFieldRoots(f: Polynomial) -> list[GaloisField]:
    """
    Returns
    -------
    The roots of f in finite field by brute force.
    """
    p = list(f.coefficients.items())[0][1].prime
    var = f.getVariables[0]
    roots = []
    for a in range(p):
        if f.evaluate({var: GaloisField(a, p)}) == GaloisField(0, p):
            roots.append(GaloisField(a, p))
    return roots


def floatRoots(f: Polynomial) -> list[float]:
    """
    Returns
    -------
    The real roots of f using Durand-Kerner method.
    """
    roots = complexRoots(f)
    return [root.real for root in roots if abs(root.imag) < 1e-6]


def complexRoots(f: Polynomial) -> list[complex]:
    """
    Returns
    -------
    The complex roots of f using Durand-Kerner method.
    """
    def evaluatePolynomial(f, x):
        return f.evaluate({f.getVariables[0]: x})
    
    degree = f.totalDegree()
    roots = []
    initialRoots = [complex(np.cos(2*np.pi*i/degree), np.sin(2*np.pi*i/degree)) for i in range(degree)]
    iterations = 100
    tolerance = 1e-12
    
    for _ in range(iterations):
        newRoots = []
        for i in range(degree):
            numerator = evaluatePolynomial(f, initialRoots[i])
            denominator = 1.0
            for j in range(degree):
                if j != i:
                    denominator *= (initialRoots[i] - initialRoots[j])
            newRoot = initialRoots[i] - numerator / denominator
            newRoots.append(newRoot)
        initialRoots = newRoots
        
        if all(abs(evaluatePolynomial(f, root)) < tolerance for root in initialRoots):
            break
    

    rootAtZero = any(abs(evaluatePolynomial(f, 0)) < tolerance for root in initialRoots)
    if rootAtZero:
        roots.append(0.0)
    

    for root in initialRoots:
        if abs(root.imag) > tolerance or abs(root.real) > tolerance:
            if abs(root.imag) < tolerance:
                root = complex(root.real, 0)
            if abs(root.real) < tolerance:
                root = complex(0, root.imag)
            roots.append(root)
    
    return roots
