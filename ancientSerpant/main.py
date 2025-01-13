
from Algebra import *

if __name__ == "__main__":
    x = defineVariable("x")
    y = defineVariable("y")
    z = defineVariable("z")

    f1 = x*x - y *y
    f2 = (x -y) * (x*x*x + y*y*5+4*x)
    f3 = (x-y) * (x*x*x+7)
    d = polynomialGCD(f1, f2, f3)
    print(d)
    l = polynomialLCM(f1, f2, f3)
    print(l)

