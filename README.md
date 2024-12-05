# Provided fields
- $\mathbb{Q}$ as rational class
- $\mathbb{R}$ as float
- $\mathbb{C}$ as complex
- $\mathbb{F}_p$ as GaloisField class
# Classes
- Monomial represeting a monomial of any variables
- Polynomial represeting a polynomial in $K[x_1, ... , x_n]$ where $K$ is one of provided fields
- RationalFunction represeting a rational function in $K(x_1, ... , x_n)$ where $K$ is one of provided fields
- Ideal represeting an ideal in $K[x_1, ... , x_n]$
# Polynomials methods
- defineVariable
- elementarySymetricPolynomial, powerSumPolynomial
- polynomialGCD, polynomialLCM, derivative, squareFreePart, embed, findIrreduciblePolynomial
- getGroebnerBasis, polynomialReduce, syzygy
- leadingCoefficient, leadingMonomial, lexOrder, gradedLexOrder
  
# Affine varieties
- polynomialImplicitization and rationalImplicitization
- plotVariety_2D and plotVariety_3D
- findRoots, solveSystem, and characteristicEquations