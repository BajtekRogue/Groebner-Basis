from typing import Callable
from .polynomial import Polynomial, Monomial
from .groebnerBasis import polynomialReduce, getGroebnerBasis
from .monomialOrders import lexOrder, gradedLexOrder

class Ideal:
    """
    Ideal of a polynomial ring in finitly many variables represented by a list of its generators.
    """
    def __init__(self, *generators):
        if len(generators) == 0:
            self.field = None
            self.generators = [Polynomial({}, None)]
            self.variables = []
            self.groebnerBasis = []
        else:
            if len(generators) == 1 and isinstance(generators[0], (list, set, tuple)):
                generators = generators[0]
            else:
                generators = list(generators)

            if not all(isinstance(generator, Polynomial) for generator in generators):
                raise TypeError(f"Generators must be polynomials")
            elif not all(generator.field == generators[0].field for generator in generators):
                raise ValueError("All generators must be over the same field")
            
            self.field = generators[0].field
            self.generators = list(set(generators))
            self.variables = set()
            for generator in generators:
                self.variables.update(generator.getVariables)
            self.variables = sorted(list(self.variables))
            self.groebnerBasis = None
    

    def __str__(self):
        result = '〈'
        for generator in self.generators:
            result += str(generator) + ', '
        return result[:-2] + '〉'

    
    def __repr__(self):
        return self.__str__()
    

    def __eq__(self, other):
        if isinstance(other, Ideal):
            if self.field != other.field:
                raise ValueError("The ideals must be over the same field.")
            if self.groebnerBasis is None:
                self.groebnerBasis = self.calculateGroebnerBasis(self.variables)
            if other.groebnerBasis is None:
                other.groebnerBasis = other.calculateGroebnerBasis(other.variables)
            return set(self.groebnerBasis) == set(other.groebnerBasis)
        else:
            return NotImplemented


    def __ne__(self, other):
        return not self == other
    

    def __pos__(self):
        return self
    

    def __neg__(self):
        return self
    

    def __contains__(self, other):
        return self.isInIdeal(other)
    

    def __add__(self, other):
        return self.algebraicSum(other)
    

    def __radd__(self, other):
        return self.algebraicSum(other)
    

    def __iadd__(self, other):
        return self.algebraicSum(other)
    

    def __sub__(self, other):
        return self + other
    

    def __rsub__(self, other):
        return other + self
    

    def __isub__(self, other):
        return self + other
    

    def __mul__(self, other):
        return self.algebraicProduct(other)
    

    def __rmul__(self, other):
        return self.algebraicProduct(other)
    

    def __imul__(self, other):
        return self.algebraicProduct(other)
    

    def __and__(self, other):
        return self.intersection(other)
    

    def __lt__(self, other):
        return self.subset(other) and self != other


    def __le__(self, other):
        return self.subset(other)
    

    def __gt__(self, other):
        return other.subset(self) and self != other
    

    def __ge__(self, other):
        return other.subset(self)
    

    def calculateGroebnerBasis(self, permutation: list[str], order: Callable = lexOrder) -> list[Polynomial]:
        """
        Returns:
        --------
        The reduced Groebner basis for the ideal with respect to the monomial order given by permutation.
        """
        return getGroebnerBasis(self.generators, permutation, order)
    

    def reduceBasis(self, permutation: list[str], order: Callable = lexOrder) -> None:
        """
        Reduces the generators of the ideal to a Groebner basis with respect to the monomial order given by permutation.
        """
        self.generators = getGroebnerBasis(self.generators, permutation, order)
        self.groebnerBasis = self.generators
    

    def isInIdeal(self, f: Polynomial) -> bool:
        """
        Returns
        -------
        True if f is in the ideal, False otherwise.

        Raises
        ------
        TypeError: If f is not a polynomial.
        ValueError: If f is not in over the same field as the ideal.
        """
        if not isinstance(f, Polynomial):
            raise TypeError("The argument must be a polynomial.")
        elif f.field != self.field:
            raise ValueError("The polynomial must be over the same field as ideal")
        else:
            if self.groebnerBasis is None:
                self.groebnerBasis = self.calculateGroebnerBasis(self.variables)
            return polynomialReduce(f, self.groebnerBasis, self.variables)[1].isZeroPolynomial()
    

    def algebraicSum(self, other):
        """
        Returns
        -------
        Algebraic sum of two ideals.

        Raises
        ------
        TypeError: If the argument is not an ideal.
        ValueError: If the ideals are not over the same field.
        """
        if not isinstance(other, Ideal):
            raise TypeError("The argument must be an ideal.")
        elif self.field != other.field:
            raise ValueError("The ideals must be over the same field.")
        else:
            return Ideal(self.generators + other.generators)
    

    def algebraicProduct(self, other):
        """
        Returns
        -------
        Algebraic product of two ideals.

        Raises
        ------
        TypeError: If the argument is not an ideal.
        ValueError: If the ideals are not over the same field.
        """
        if not isinstance(other, Ideal):
            raise TypeError("The argument must be an ideal.")
        elif self.field != other.field:
            raise ValueError("The ideals must be over the same field.")
        else:
            result = set()
            for f in self.generators:
                for g in other.generators:
                    result.add(f * g)
            return Ideal(tuple(result))
    

    def intersection(self, other):
        """
        Returns
        -------
        Intersection of ideals.
        Raises
        ------
        TypeError: If the argument is not an ideal.
        ValueError: If the ideals are not over the same field.
        """
        if not isinstance(other, Ideal):
            raise TypeError("The argument must be an ideal.")
        elif self.field != other.field:
            raise ValueError("The ideals must be over the same field.")
        else:
            t = Polynomial({Monomial({Monomial.DUMMY : 1}): self.field(1)}, self.field)
            s = self.field(1) - t
            tI = Ideal([t * f for f in self.generators])
            sJ = Ideal([s * g for g in other.generators])
            K = tI + sJ
            variables = list(set(self.variables + other.variables))
            permutation = [Monomial.DUMMY] + variables
            G = K.calculateGroebnerBasis(permutation, lexOrder)
            H = Ideal.eliminationIdeal(G, variables)
            return Ideal(H)
        

    @staticmethod
    def eliminationIdeal(F: list, variables: list[str]) -> list:
        """
        Returns
        -------
        Elimination ideal of <F> leaving only the argument variables.
        """
        result = []
        for f in F:
            if set(f.getVariables).issubset(set(variables)):
                result.append(f)
        return result
    

    def subset(self, other) -> bool:
        """
        Returns
        -------
        True if self is a subset of other, False otherwise.
        TypeError: If the argument is not an ideal.
        ValueError: If the ideals are not over the same field.
        """
        if not isinstance(other, Ideal):
            raise TypeError("The argument must be an ideal.")
        elif self.field != other.field:
            raise ValueError("The ideals must be over the same field.")
        else:
            return all(f in other for f in self.generators)