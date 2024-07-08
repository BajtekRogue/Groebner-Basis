from Algebra.polynomialMethods import *
from Algebra.rationalFunction import RationalFunction
from Algebra.rational import rational
from Algebra.varieties import rationalImplicitization, polynomialImplicitization, plotVariety_2D, plotVariety_3D
from Algebra.solver import findRoots, rationalRoots, solveSystem, bruteForceGaloisField, characteristicEquations



if __name__ == "__main__":
    x = defineVariable('x', rational)
    y = defineVariable('y', rational)
    z = defineVariable('z', rational)

    f = x + y + z - 6
    g = x**2 + y**2 + z**2 - 14
    h = x**3 + y**3 + z**3 - 36

    F = [f, g, h]
    print(f"System = {F}")
    print(f"Solutions = {solveSystem(F, field=rational)}")
    print(f"Characteristic equations = {characteristicEquations(F)}")

