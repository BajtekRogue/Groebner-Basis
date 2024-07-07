
from .monomial import Monomial
from functools import cmp_to_key
from .rational import rational
from .galoisField import GaloisField

class Polynomial:
    
    def __init__(self, coefficients: dict, field = None):
        if field is None and coefficients:
            field = next(iter(coefficients.values())).__class__
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'coefficients', coefficients)
        object.__setattr__(self, 'field', field)
        self.removeZeroCoefficients()
        object.__setattr__(self, '_initialized', True)


    def __setattr__(self, name, value):
        if self.__dict__.get('_initialized', False):
            raise AttributeError(f"{self.__class__.__name__} does not support attribute assignment")
        super().__setattr__(name, value)


    def __delattr__(self, name):
        raise AttributeError(f"{self.__class__.__name__} does not support attribute deletion")


    def __str__(self):
        if len(self.coefficients) == 0:
            return '0'
      
        result = ''
        self.sortCoefficients() 
        for monomial, coefficient in self.coefficients.items():
            if isinstance(coefficient, float) and coefficient.is_integer():
                coefficient = int(coefficient)

            if isinstance(coefficient, (complex, GaloisField)) or coefficient > 0:
                result += ' + '
            else:
                result += ' - '

            if isinstance(coefficient, (complex, GaloisField)):
                result += f'{coefficient}'
            elif monomial == Monomial.constant():
                result += f'{abs(coefficient)}'
            # elif isinstance(coefficient, GaloisField) and coefficient.number != 1:
            #     result += f'{coefficient}'
            # elif isinstance(coefficient, GaloisField) and coefficient.number == 1:
            #     result += ''
            elif (coefficient != 1 and coefficient != -1):
                result += f'{abs(coefficient)}'

            if monomial != Monomial.constant():
                result += monomial.__str__()

        if result[1] == '+':
            return result[3:]
        else:
            return result[1:]


    def __repr__(self):
        return self.__str__()
    
    
    def __eq__(self, other):
        p = self - other
        return p.isZeroPolynomial()
    
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    
    def __pos__(self):
        return self
    
    
    def __neg__(self):
        result = {}
        for monomial, coefficient in self.coefficients.items():
            result[monomial] = -coefficient
            
        return Polynomial(result, self.field)
    
    
    def __add__(self, other):
        result = {}
        
        for monomial, coefficient in self.coefficients.items():
                result[monomial] = coefficient
                
        if isinstance(other, Polynomial):
            if self.field != other.field:
                raise ValueError(f"Both polynomials must be over the same field")
            
            for monomial, coefficient in other.coefficients.items():
                if monomial in result:
                    result[monomial] += coefficient
                else:
                    result[monomial] = coefficient
        
        elif isinstance(other, (int, float, complex, rational, GaloisField)):
            if isinstance(other, GaloisField) and self.field != GaloisField:
                raise ValueError(f"Cannot add modular integer to a polynomial over a field of characteristic 0")
            elif Monomial.constant() in result:
                result[Monomial.constant()] += other
            else:
                result[Monomial.constant()] = other
        else:
            return NotImplemented
        
        return Polynomial(result, self.field)
    
    
    def __radd__(self, other):
        return self.__add__(other)


    def __iadd__(self, other):
        return self + other


    def __sub__(self, other):
        return self + (-other)
    
    
    def __rsub__(self, other):
        return -self + other
    
    
    def __isub__(self, other):
        return self + (-other)
    
    
    def __mul__(self, other):
        result = {}
        
        if isinstance(other, Polynomial):
            if self.field != other.field:
                raise ValueError(f"Both polynomials must be over the same field")
            for monomial1, coefficient1 in self.coefficients.items():
                for monomial2, coefficient2 in other.coefficients.items():
                    newMonomial = monomial1 * monomial2
                    newCoefficient = coefficient1 * coefficient2
                    
                    if newMonomial in result:
                        result[newMonomial] += newCoefficient
                    else:
                        result[newMonomial] = newCoefficient
                        
        elif isinstance(other, (int, float, complex, rational, GaloisField)):
            if isinstance(other, GaloisField) and self.field != GaloisField:
                raise ValueError(f"Cannot multiply a polynomial over a field of characteristic 0 by a modular integer ")
            elif Polynomial.isCoefficientZero(other):
                return Polynomial({}, self.field)
            else:
                for monomial, coefficient in self.coefficients.items():
                    result[monomial] = coefficient * other
        else:
            return NotImplemented
        
        return Polynomial(result, self.field)
        
    
    def __rmul__(self, other):
        return self * other
    
    
    def __imul__(self, other):
        return self * other
    
    
    def __pow__(self, other):
        if not isinstance(other, int) or other < 0:
            raise TypeError(f"Exponentiation is only supported with natural exponents")

        if other == 0:
            return Polynomial({Monomial.constant(): 1}, self.field)


        result = Polynomial({Monomial.constant(): 1}, self.field)
        base = self

        while other > 0:
            if other % 2 == 1:
                result *= base
            base *= base
            other //= 2

        return result
    
    
    def __ipow__(self, other):
        return self ** other
    
    
    def __hash__(self):
        return hash(tuple(self.coefficients.items()))
                    
    
    def evaluate(self, point: dict):
        """
        Returns
        -------
        The value of the polynomial at the given point. For example givne f(x,y) imputing {'x': 1, 'y': 2} returns f(1,2)

        Raises
        ------
        ValueError: If the point does not contain all variables of the polynomial or its number are not from the same field.
        """
        if self.field == GaloisField and not all(isinstance(value, GaloisField) for value in point.values()):
            raise ValueError(f"All values in the point must be from the same field as the polynomial")
        result = 0
        for monomial, coefficient in self.coefficients.items():
            term = coefficient
            for variable, power in monomial.exponent.items():
                term *= point[variable] ** power
            result += term
        
        return result
    

    def totalDegree(self) -> int:
        """
        Returns
        -------
        Total degree of the polynomial, which is the maximal sum of the degrees of all monomials.
        """
        if len(self.coefficients) == 0:
            return -1
        
        max_sum = 0
        for monomial in self.coefficients.keys():
            max_sum = max(max_sum, monomial.degree())
        return max_sum
    

    @staticmethod
    def isCoefficientZero(coefficient) -> bool:
        """
        Returns
        -------
        If field is countable, checks if the coefficient is zero. If the field is uncountable, checks if the coefficient is close to zero.
        """
        if isinstance(coefficient, (float, complex)) and abs(coefficient) < 0.0001:
            return True
        elif isinstance(coefficient, (int, rational)) and coefficient == 0:
            return True
        elif isinstance(coefficient, GaloisField) and (coefficient.number == 0 or coefficient.number % coefficient.prime == 0):
            return True
        else:
            return False
        

    def isZeroPolynomial(self) -> bool:
        """
        Returns
        -------
        Checks if the polynomial is identically zero. If the field is countable, checks if all coefficients are zero. If the field is uncountable, checks if all coefficients are close to zero.
        """
        return all(Polynomial.isCoefficientZero(coefficient) for coefficient in self.coefficients.values())

    
    def removeZeroCoefficients(self) -> None:
        """
        Removes all zero coefficients from the polynomial.
        """
        nonZeroCoefficients = {monomial: coefficient for monomial, coefficient in self.coefficients.items() if not Polynomial.isCoefficientZero(coefficient)}
        object.__setattr__(self, 'coefficients', nonZeroCoefficients)
    
    
    def sortCoefficients(self) -> None:
        """
        Sorts the coefficients of the polynomial in descending order of the monomial degree and the maximum exponent.
        """
        def monomial_to_key(alpha: Monomial, beta: Monomial) -> int:
            if alpha.degree() < beta.degree():
                return -1
            elif alpha.degree() > beta.degree():
                return 1
            else:
                if max(alpha.exponent.values()) < max(beta.exponent.values()):
                    return -1
                elif max(alpha.exponent.values()) > max(beta.exponent.values()):
                    return 1
                else:
                    return 0

        keyFunction = cmp_to_key(monomial_to_key)
        sortedCoefficients = dict(sorted(self.coefficients.items(), key=lambda item: keyFunction(item[0]), reverse=True))
        object.__setattr__(self, 'coefficients', sortedCoefficients)
    

    @property
    def getCoefficients(self) -> dict:
        """
        Returns
        -------
        The coefficients of the polynomial.
        """
        return self.coefficients


    @property
    def getMonomials(self) -> list:
        """
        Returns
        -------
        The monomials of the polynomial.
        """
        return list(self.coefficients.keys())
    
    
    @property
    def getVariables(self) -> list[str]:
        """
        Returns
        -------
        The list of variables in the polynomial sorted alphabetically.
        """
        result = set()
        for monomial in self.coefficients.keys():
            result.update(monomial.exponent.keys())
        return sorted(list(result))
    

