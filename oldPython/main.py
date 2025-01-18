
from Algebra import *

if __name__ == "__main__":
    x = defineVariable("x")
    y = defineVariable("y")
    z = defineVariable("z")

    f1 = x + y + z - 9
    f2 = x**2 + y**2 + z**2  - 35
    f3 = x**3 + y**3 + z**3  - 153
    F = [f1, f2, f3]
    X = solveSystem(F)
    print(X)

