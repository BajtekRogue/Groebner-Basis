from Algebra.polynomialMethods import *
from Algebra.rationalFunction import RationalFunction
from Algebra.rational import rational
from Algebra.varieties import rationalImplicitization, polynomialImplicitization, plotVariety_2D, plotVariety_3D
from Algebra.solver import findRoots, rationalRoots



if __name__ == "__main__":
    x = defineVariable('x', GaloisField, 5)
    y = defineVariable('y', float)
    z = defineVariable('z', complex)

    f = x**3 + 4 * x 
    g = y**3 + 4 * y
    h = z**3 + 4 * z
    print(findRoots(f))
    print(findRoots(y**5+y+1))
    print(findRoots(z**5+z+1))
