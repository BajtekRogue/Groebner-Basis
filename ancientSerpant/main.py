from Algebra import *

if __name__ == "__main__":
    x = defineVariable("x")
    y = defineVariable("y")
    z = defineVariable("z")
    a = defineVariable("a")
    b = defineVariable("b")
    c = defineVariable("c")
    d = defineVariable("d")

    f1 = (2 + a) * c 
    f2 = (2 + a) * d 
    f3 = b 
    trig1 = (a**2) + (b**2) - 1
    trig2 = (c**2) + (d**2) - 1

    G = getGroebnerBasis([f1, f2, f3, trig1, trig2], ["a", "b", "c", "d", "x", "y", "z"])
    print(G)

    # H = polynomialImplicitization({'x' : 3*u+3*u*v*v-u*u*u, 'y' : 3*v+3*u*u*v-v*v*v, 'z' : 3*u*u-3*v*v})
    # print(H)
