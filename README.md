# About Project
This project was written both for `C++` and `Python`. It allows to manipulate multivariable polynomials in $K[x_1, ... , x_n]$ ring. Users can construct ideals, compute Gröbner bases, solve systems of equations, and more. Most of the algorithms used are based on the book `Cox, D., Little, J., & O'Shea, D. – Ideals, Varieties, and Algorithms: An Introduction to Computational Algebraic Geometry and Commutative Algebra`. More details are available below for C++ version, Python is similar.

## Classes
- `Rational` represents $\mathbb{Q}$ with any integer type
- `MonomialOrders` abstract class for monomial orders. Implemented are `LexOrder`, `GradedLexOrder`, `GradedRevLexOrder`, `WeightedOrder`
- `Monomial` represents monomials of variables
- `Polynomial` represnts polynomials in $K[x_1, ... , x_n]$
- `Ideal` represents ideals in $K[x_1, ... , x_n]$

## Methods
- `defineVariable` declares variable (as polynomial) for easier consturction of polynomials
- `polynomialImplicitization` calculates implicitization of polynomial system
- `rationalImplicitization` calculates implicitization of rational system
- `lcm` calcualtes least common multiple of polynomials
- `gcd` calculates greatest common divisor of polynomials
- `polynomialReduce` generelized division algorithm for polynomials
- `syzygy` calculates syzygy polynomials
- `calculateGroebnerBasis` calculates Gröbner basis for given set of polynomials
- `characteristicEquations` calculates characteristic equations for system of equations
- `solveSystem` solves sytem of equation