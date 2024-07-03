from tqdm import tqdm
from Fields import GaloisField
from Ideals import Ideal
from Ideals import polynomialReduce, getGroebnerBasis, extendToGroebnerBasis, lexOrder, gradedLexOrder

from Polynomials.polynomialMethods import *

if __name__ == "__main__":
    x = defineVariable('x', RationalNumber)
    y = defineVariable('y', RationalNumber)
    z = defineVariable('z', RationalNumber)
    u = defineVariable('u', RationalNumber)
    v = defineVariable('v', RationalNumber)
    {'x': u * v, 'y': v, 'z': u ** 2}
    X = implicitization({'x': u * v, 'y': v, 'z': u ** 2})
    print(X)
    f = (x+4) ** 3 * (y+3) ** 2 * (z+2)
    print(f)
    print(squareFreePart(f))
    print((x+4) * (y + 3) * (z + 2))
    
