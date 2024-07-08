
import itertools
import numpy as np
from .polynomialMethods import embed
from .monomialOrders import lexOrder
from .rational import rational
from .galoisField import GaloisField
from .polynomial import Polynomial
from NumberTheory import integerLCM, divisors
from .groebnerBasis import getGroebnerBasis

def findRoots(f: Polynomial) -> list:
    """
    Returns
    -------
    The roots of the polynomial f.

    Raises
    ------
    ValueError: If the polynomial is not univariate.
    """
    if len(f.getVariables) > 1:
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
    P = divisors(abs(u))
    Q = divisors(abs(v))
    positive = [rational(q, p) for q in Q for p in P]
    negative = [rational(-q, p) for q in Q for p in P]
    candidates = list(set(positive + negative)) + [rational(0)]
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
    for a in GaloisField.getAllElements(p):
        if f.evaluate({var: a}) == GaloisField(0, p):
            roots.append(a)
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
    iterations = 1000
    tolerance = 1e-6
    
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


def solveSystem(F: list[Polynomial], field = None, prime = None) -> list[tuple]:
    """
    Returns
    -------
    The solutions of the system of polynomials F over field

    Raises
    ------
    ValueError: If polynomials are over different fields.
    """
    if field is None:
        field = F[0].field

    
    variables = sorted(list(set(sum([f.getVariables for f in F], []))))
    G = getGroebnerBasis(F, variables, order=lexOrder)
    if field != F[0].field:
        G = [embed(g, field, prime) for g in G]

    # check is solutions exist using hilbert nullstellensatz
    if len(G) == 1 and (G[0] - 1).isZeroPolynomial():
        return "System is inconsistent." 
    
    if field == GaloisField: 
        solutions = bruteForceGaloisField(G)
        result = []
        for solution in solutions:
            result.append({variables[i]: solution[i] for i in range(len(variables))})
        return result
    else: 
        solutions = recursiveSolver(G) 
        if solutions == "There are infinitely many solutions.":
            return "There are infinitely many solutions."
        elif solutions == "No solutions found.":
            return []
        for i in range(len(solutions)):
            solutions[i] = dict(sorted(solutions[i].items(), key=lambda x: x[0]))
    return solutions


def bruteForceGaloisField(F: list[Polynomial]) -> list[tuple]:
    """
    Returns
    -------
    The solutions of the system of polynomials F over finite field by brute force.
    """
    p = list(F[0].coefficients.items())[0][1].prime
    variables = sorted(list(set(sum([f.getVariables for f in F], []))))
    solutions = []
    points = list(itertools.product(GaloisField.getAllElements(p), repeat=len(variables)))
    
    for point in points:
        if all(f.evaluate({var: point[i] for i, var in enumerate(variables)}) == GaloisField(0, p) for f in F):
            solutions.append(point)
    return solutions


def recursiveSolver(F: list[Polynomial]) -> list[tuple]:
    """
    Returns
    -------
    The solutions of the system of polynomials F over infinite field.
    """
    # print(f"Enter called with {F}")
    if len(F) == 0:
        print("empty set\n")
        return []
    
    univariate = [f for f in F if len(f.getVariables) == 1]
    constants = [f for f in F if len(f.getVariables) == 0 and not f.isZeroPolynomial()]
    if len(constants) > 0:
        # print(f'No solutions found for {F}\n')
        return "No solutions found."
    elif len(univariate) == 0:
        return "There are infinitely many solutions."
    
    f = univariate[0]
    var = f.getVariables[0]
    univariate.remove(f)
    roots = findRoots(f)
    if len(roots) == 0:
        return "No solutions found."
    # print(f"Roots found: {roots} for variable {var} and polynomial {f}")
    solutions = []
    for root in roots:
        solution = {var: root}
        G = []
        for f in F:
            try:
                result = f.substitute(var, root)
                G.append(result)
            except:
                G.append(f)
        H = [g for g in G if not g.isZeroPolynomial()]
        if len(H) == 0:
            solutions.append(solution)
        else:
            # print(f'Calling recursiveSolver with {H} after substituting {solution}')
            extendedSolution = recursiveSolver(H)
            if extendedSolution == "No solutions found.":
                # print(f"No solutions found for {H}\n")
                continue
            elif extendedSolution == "There are infinitely many solutions.":
                return "There are infinitely many solutions."
            else:
                solutions.extend([{**solution, **s} for s in extendedSolution])
    # print(f'Exit called with {F} and solutions {solutions}\n')
    return solutions


def characteristicEquations(F: list[Polynomial]) -> dict[str, Polynomial]:
    """
    Returns
    -------
    For system of equations F returns the characteristic equations for each variable.
    """
    variables = sorted(list(set(sum([f.getVariables for f in F], []))))
    result = {}
    for var in variables:
        newPermutation = [v for v in variables if v != var]
        newPermutation += [var]
        G = getGroebnerBasis(F, newPermutation, order=lexOrder)
        H = [g for g in G if g.getVariables == [var]]
        if len(H) == 0:
            return "Characteristic equations do not exist."
        result[var] = H[0]
    return result