
from .galoisField import GaloisField
from .polynomial import Polynomial
from .monomial import Monomial
from .ideal import Ideal
from .monomialOrders import lexOrder
from .groebnerBasis import getGroebnerBasis
from .rationalFunction import RationalFunction
from .polynomialMethods import defineVariable, normalizeCoefficients, ZERO
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

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


def plotVariety_2D(f: Polynomial) -> None:
    """
    Plots the variety defined by the polynomial f in 2D plane. Needs f field to be float
    """
    if f.field != float:
        raise ValueError("The polynomial must have float coefficients.")
    
    def evaluatePolynomial(f, x, y):
        shape = x.shape
        z = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                z[i, j] = f.evaluate({'x': x[i, j], 'y': y[i, j]})
        return z
    
    x = np.linspace(-3, 3, 400)
    y = np.linspace(-3, 3, 400)
    X, Y = np.meshgrid(x, y)
    Z = evaluatePolynomial(f, X, Y)

    plt.contour(X, Y, Z, levels=[0], colors='blue')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Plot of {f}$ = 0$')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def plotVariety_3D(f: Polynomial, bbox = (-2.5, 2.5)) -> None:
    """
    Plots the variety defined by the polynomial f in 3D space. Needs f field to be float
    """
    if f.field != float:
        raise ValueError("The polynomial must have float coefficients.")
    
    def evaluatePolynomial(f, x, y, z):
        return f.evaluate({'x': x, 'y': y, 'z': z})

    xmin, xmax, ymin, ymax, zmin, zmax = bbox * 3
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    A = np.linspace(xmin, xmax, 100)
    B = np.linspace(xmin, xmax, 15)
    A1, A2 = np.meshgrid(A, A)

    for z in B:  # Plot contours in the XY plane
        X, Y = A1, A2
        Z = evaluatePolynomial(f, X, Y, z)
        cset = ax.contour(X, Y, Z+z, [z], zdir='z', colors='b')

    for y in B:  # Plot contours in the XZ plane
        X, Z = A1, A2
        Y = evaluatePolynomial(f, X, y, Z)
        cset = ax.contour(X, Y+y, Z, [y], zdir='y', colors='b')

    for x in B:  # Plot contours in the YZ plane
        Y, Z = A1, A2
        X = evaluatePolynomial(f, x, Y, Z)
        cset = ax.contour(X+x, Y, Z, [x], zdir='x', colors='b')

    # Set plot limits to encompass the entire surface
    ax.set_zlim3d(zmin, zmax)
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylim3d(ymin, ymax)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Plot of {f}$ = 0$')

    plt.show()