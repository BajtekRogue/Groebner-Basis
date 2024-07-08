from Algebra.polynomialMethods import *
from Algebra.rationalFunction import RationalFunction
from Algebra.rational import rational
from Algebra.varieties import rationalImplicitization, polynomialImplicitization, plotVariety_2D, plotVariety_3D
from Algebra.solver import findRoots, rationalRoots, solveSystem, bruteForceGaloisField, characteristicEquations



if __name__ == "__main__":
    x = defineVariable('x', rational)
    y = defineVariable('y', rational)
    z = defineVariable('z', rational)
    w = defineVariable('w', rational)
    a = defineVariable('a', rational)
    b = defineVariable('b', rational)
    c = defineVariable('c', rational)
    d = defineVariable('d', rational)
    e = defineVariable('e', rational)
    f1 = a*b+b-a*c-a
    f2 = b*c+c-b-b*d
    f3 = c*d+d-c-c*e
    f4 = d*e+e-d-d*a
    g = a*b*c*d * e -1
    F = [f1, f2, f3, f4, g]
    # print(getGroebnerBasis(F, ['a', 'b', 'c', 'd', 'e']))
    print(f"System = {F}")
    print(f"Solutions = {solveSystem(F, field=rational)}")
    print(f"Characteristic equations = {characteristicEquations(F)}")

