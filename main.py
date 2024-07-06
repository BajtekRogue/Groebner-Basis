from Algebra.polynomialMethods import *
from Algebra.rationalFunction import RationalFunction
from Algebra.fraction import RationalNumber
from Algebra.varieties import rationalImplicitization
if __name__ == "__main__":
    x = defineVariable('x', RationalNumber)
    y = defineVariable('y', RationalNumber)
    z = defineVariable('z', RationalNumber)
    t = defineVariable('t', RationalNumber)
    a = RationalFunction(1 + t ** 2, 1 - t ** 2)
    b = RationalFunction(2 * t, 1 - t ** 2)
    X = rationalImplicitization({"x": a, "y": b})
    print(X)