from Algebra import *

if __name__ == "__main__":
    # x = defineVariable("x")
    # y = defineVariable("y")
    # z = defineVariable("z")
    # w = defineVariable("w")

    # f = x**3 + y**3 + z**3 - 3*x*y*z
    # q1, r1 = polynomialReduce(f, [x+y+z], ['x', 'y', 'z'], order=gradedLexOrder)
    # q2, r2 = polynomialReduce(f, [x+y+z], ['x', 'z', 'y'], order=gradedLexOrder)
    # q3, r3 = polynomialReduce(f, [x+y+z], ['y', 'z', 'x'], order=gradedLexOrder)
    # q4, r4 = polynomialReduce(f, [x+y+z], ['y', 'x', 'z'], order=gradedLexOrder)
    # q5, r5 = polynomialReduce(f, [x+y+z], ['z', 'x', 'y'], order=gradedLexOrder)
    # q6, r6 = polynomialReduce(f, [x+y+z], ['z', 'y', 'x'], order=gradedLexOrder)
    # print(q1, r1)
    # print(q2, r2)
    # print(q3, r3)
    # print(q4, r4)
    # print(q5, r5)
    # print(q6, r6)
    x = defineVariable("x")
    y = defineVariable("y")
    z = defineVariable("z")
    a = defineVariable("a")    
    b = defineVariable("b")
    c = defineVariable("c")
    f1 = a**2 + 2*b*c - x**2 -2*y*z
    f2 = b**2 + 2*a*c - y**2 -2*x*z
    f3 = c**2 + 2*a*b - z**2 -2*x*y
    # G = getGroebnerBasis([f1, f2, f3], ["a", "b", "c", "x", "y", "z"])
    # print(G)
    f = x**3 * y**3 + y**3*z**3+z**3*x**3
    e1 = elementarySymetricPolynomial(1, ["x", "y", "z"])
    e2 = elementarySymetricPolynomial(2, ["x", "y", "z"])
    e3 = elementarySymetricPolynomial(3, ["x", "y", "z"])
    print((e2**3)+(3*e3**2)-(3*e1*e2*e3))
    print(e1**3-3*e1*e2+3*e3)
