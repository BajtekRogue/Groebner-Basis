# import copy
# from itertools import combinations
# from Fields import RationalNumber
# from Fields import GaloisField
# from .polynomial import Polynomial
# from .monomial import Monomial
# from Ideals import polynomialReduce, getGroebnerBasis, Ideal, lexOrder

# class PolynomialFactory:

#     SUPPORTED_FIELDS = [RationalNumber, float, complex, GaloisField]
#     ZERO = {RationalNumber: RationalNumber(0), float: 0.0, complex: 0 + 0j, GaloisField: 0}
#     ONE = {RationalNumber: RationalNumber(1), float: 1.0, complex: 1 + 0j, GaloisField: 1}

#     def __init__(self, field, variableNames: list[str], strict: bool = False):
#         if field not in PolynomialFactory.SUPPORTED_FIELDS:
#             raise ValueError(f"Field {field} is not supported. Supported fields are { PolynomialFactory.SUPPORTED_FIELDS}")

#         self.field = field
#         self.numberOfVariables = len(variableNames)
#         self.variableNames = variableNames
#         self.strict = strict

    
#     def addPrime(self, prime) -> None:
#         """
#         If the field is GaloisField, this method allows to chose prime it will use

#         Raises
#         ------
#         ValueError: If the field is not GaloisField or the prime is not in the list of supported primes.
#         """
#         if self.field != GaloisField:
#             raise ValueError("This method is only supported for GaloisField")
#         elif prime not in GaloisField.PRIMES:
#             raise ValueError(f"Prime {prime} is not in the list of supported primes.")
#         else:
#             self.GaloisField_prime = prime


#     def validateCoefficients(self, coefficients: dict) -> None:
#         if not all(isinstance(coeff, self.field) for coeff in coefficients.values()):
#             raise ValueError(f"All coefficients must be of type {self.field}")
#         if not all(len(monomial) == self.numberOfVariables for monomial in coefficients.keys()):
#             raise ValueError(f"Each monomial must contain {self.numberOfVariables}")
#         if not all(all(isinstance(entry, int) and entry >= 0 for entry in monomial) for monomial in coefficients.keys()):
#             raise ValueError("All powers must be natrual numbers")
        
    
#     def zeroPolynomial(self) -> Polynomial:
#         """
#         Returns
#         -------
#         Zero polynomial.
#         """
#         return Polynomial({}, self.field)
    

#     def onePolynomial(self) -> Polynomial:
#         """
#         Returns
#         -------
#         One polynomial.
#         """
#         return Polynomial({Monomial({}): PolynomialFactory.ONE[self.field]}, self.field)
    

#     def createPolynomial(self, coefficients: dict) -> Polynomial:
#         """
#         Returns
#         -------
#         Given dictionary of the form {(1, 2): 3, (2, 3): 4} returns the polynomial 3*x*y^2 + 4*x^2*y^3
#         """
#         if self.strict:
#             self.validateCoefficients(coefficients)
        
#         if self.field == RationalNumber:
#             coefficients = {power: coefficient if isinstance(coefficient, RationalNumber) else RationalNumber(coefficient) for power, coefficient in coefficients.items()}
#         elif self.field == GaloisField:
#             coefficients = {power: coefficient if isinstance(coefficient, GaloisField) else GaloisField(coefficient, self.GaloisField_prime) for power, coefficient in coefficients.items()}

#         result = {}
#         for power, coefficient in coefficients.items():
#             if Polynomial.isCoefficientZero(coefficient):
#                 continue

#             monomial = Monomial.makeFromTuples(power, self.variableNames)
#             if monomial.degree() == 0:
#                 monomial = Monomial({})

#             result[monomial] = coefficient

#         return Polynomial(result, self.field)
    

#     def elementarySymetricPolynomial(self, degree: int) -> Polynomial:
#         """
#         Returns
#         -------
#         Elementary symetric polynomial of given degree. Note that e0 = 0 and ek = 0 for k > n.
#         """
#         if degree <= 0 or degree > self.numberOfVariables:
#             return self.zeroPolynomial()
        
#         result = {}
#         subsets = list(combinations(list(range(self.numberOfVariables)), degree))
#         binarySubsets = []

#         for subset in subsets:
#             binaryRepresentation = [0] * self.numberOfVariables
#             for index in subset:
#                 binaryRepresentation[index] = 1
#             binarySubsets.append(tuple(binaryRepresentation))
        
#         for binary_subset in binarySubsets:
#             result[binary_subset] = PolynomialFactory.ONE[self.field]
        
#         return self.createPolynomial(result)
    

#     def powerSumPolynomial(self, degree: int) -> Polynomial:
#         """
#         Returns
#         -------
#         Power sum polynomial of given degree pk = x1^k + x2^k + ... + xn^k
        
#         Raises
#         ------
#         ValueError: If degree is non-positive.
#         """
#         if degree <= 0:
#             raise ValueError("Degree of power sum polynomial must be positive")
        
#         result = {}
#         for var in self.variableNames:
#             exponent = Monomial({var: degree})
#             result[exponent] = PolynomialFactory.ONE[self.field]
        
#         return Polynomial(result, self.field)
    

#     def derivative(self, f: Polynomial, variable: str, order: int = 1) -> Polynomial:
#         """
#         Returns
#         -------
#         Order-th formal derivative of the polynomial f with respect to the variable.
        
#         Raises
#         ------
#         ValueError: If order is negative.
#         """
#         if order < 0:
#             raise ValueError("Order of derivative must be non-negative")
#         elif f.isZeroPolynomial() or variable not in self.variableNames:
#             return self.zeroPolynomial()
#         elif order == 0:
#             return f
        
#         def differentiate(g: Polynomial, variable: str) -> Polynomial:
#             result = {}
#             for monomial, coefficient in g.coefficients.items():
#                 if variable not in monomial.exponent:
#                     continue
#                 else:
#                     newCoefficient = coefficient * monomial.exponent[variable]
#                     newMonomial = copy.deepcopy(monomial)
#                     newMonomial.exponent[variable] -= 1
#                     if newMonomial.exponent[variable] == 0:
#                         del newMonomial.exponent[variable]
#                     result[newMonomial] = newCoefficient

#             return Polynomial(result, self.field)

#         h = copy.deepcopy(f)
#         while order > 0:
#             h = differentiate(h, variable)
#             order -= 1
#         return h
    

#     def embedCoefficients(self, coefficients: dict) -> Polynomial:
#         """
#         Returns
#         -------
#         Given dictionary to construct Polynomial ebeds it's coefficients into the field.
#         """
#         if self.field == RationalNumber:
#             coefficients = {power: coefficient if isinstance(coefficient, RationalNumber) else RationalNumber(coefficient) for power, coefficient in coefficients.items()}
#         elif self.field == GaloisField:
#             coefficients = {power: coefficient if isinstance(coefficient, GaloisField) else GaloisField(coefficient, self.GaloisField_prime) for power, coefficient in coefficients.items()}
#         elif self.field == float:
#             coefficients = {power: float(coefficient) for power, coefficient in coefficients.items()}
#         elif self.field == complex:
#             coefficients = {power: complex(coefficient) for power, coefficient in coefficients.items()}
#         return Polynomial(coefficients, self.field)
    

#     def lcm(self, f: Polynomial, g: Polynomial) -> Polynomial:
#         """
#         Returns
#         -------
#         Least common multiple of two polynomials.
#         """
#         t = Polynomial({Monomial({Monomial.DUMMY : PolynomialFactory.ONE[self.field]}): PolynomialFactory.ONE[self.field]}, self.field)
#         F = [t * f, (1 - t) * g]
#         variables = [Monomial.DUMMY] + self.variableNames
#         G = getGroebnerBasis(F, variables, lexOrder)
#         H = Ideal.eliminationIdeal(G, self.variableNames)
#         return H[0]
    

#     def gcd(self, f: Polynomial, g: Polynomial) -> Polynomial:
#         """
#         Returns
#         -------
#         Greatest common divisor of two polynomials.
#         """
#         return polynomialReduce(f * g, [self.lcm(f, g)], self.variableNames, lexOrder)[0][0]
    

#     def PolynomialGCD(self, *args: Polynomial) -> Polynomial:
#         """
#         Returns
#         -------
#         The greates common divisor of the provided polynomials.
        
#         Raises
#         ------
#         ValueError: If no arguments are provided or one of the arguments is not polynomial or not all polynomials are over the same field.
#         """
#         if len(args) == 0:
#             raise ValueError("At least one argument must be provided.")
#         if not all(isinstance(arg, Polynomial) for arg in args):
#             raise ValueError("All arguments must be polynomials.")
#         if not all(arg.field == args[0].field for arg in args):
#             raise ValueError("All arguments must be of the same field.")
#         if len(args) == 1 and isinstance(args[0], (list, set)):
#             args = tuple(args[0])
#         result = args[0]
#         for i in range(1, len(args)):
#             result = self.gcd(result, args[i])
#         return result


#     def PolynomialLCM(self, *args: Polynomial) -> Polynomial:
#         """
#         Returns
#         -------
#         The least common multiple of the provided polynomials.

#         Raises
#         ------
#         ValueError: If no arguments are provided or one of the arguments is not polynomial or not all polynomials are over the same field.
#         """
#         if len(args) == 0:
#             raise ValueError("At least one argument must be provided.")
#         if not all(isinstance(arg, Polynomial) for arg in args):
#             raise ValueError("All arguments must be polynomials.")
#         if not all(arg.field == args[0].field for arg in args):
#             raise ValueError("All arguments must be of the same field.")
#         if len(args) == 1 and isinstance(args[0], (list, set)):
#             args = tuple(args[0])
#         result = args[0]
#         for i in range(1, len(args)):
#             result = self.lcm(result, args[i])
#         return result