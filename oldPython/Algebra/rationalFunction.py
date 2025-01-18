from .polynomialMethods  import polynomialGCD
from .polynomial import Monomial, Polynomial
from .groebnerBasis import polynomialReduce

class RationalFunction:
    """
    RationalFunction class represents a rational function of the form f(x) = p(x)/q(x) where p(x) and q(x) are polynomials.
    """ 
    def __init__(self, numerator: Polynomial, denominator: Polynomial, field = None, reduce: bool = False):
        if denominator.isZeroPolynomial():
            raise ValueError("Denominator cannot be zero")
        elif not isinstance(numerator, Polynomial) or not isinstance(denominator, Polynomial):
            raise TypeError("Numerator and denominator must be polynomials")
        elif numerator.field != denominator.field:
            raise ValueError("Numerator and denominator must be over the same field")
        
        if field is None:
            field = numerator.field

        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'numerator', numerator)
        object.__setattr__(self, 'denominator', denominator)
        object.__setattr__(self, 'field', numerator.field)
        object.__setattr__(self, '_initialized', True)

        if reduce:
            self.reduce()

    def __setattr__(self, name, value):
        if self.__dict__.get('_initialized', False):
            raise AttributeError(f"{self.__class__.__name__} does not support attribute assignment")
        super().__setattr__(name, value)


    def __delattr__(self, name):
        raise AttributeError(f"{self.__class__.__name__} does not support attribute deletion")


    def __str__(self):
        return f"({self.numerator})/({self.denominator})"  

    
    def __repr__(self):
        return self.__str__()
    
    
    def __eq__(self, other):
        q = self - other
        return q.numerator.isZeroPolynomial()
    
    
    def __ne__(self, other):
        return not self == other
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        return RationalFunction(-self.numerator, self.denominator)
     
    
    def __add__(self, other):
        if isinstance(other, RationalFunction):
            return RationalFunction(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)
        elif isinstance(other, Polynomial):
            return RationalFunction(self.numerator + other * self.denominator, self.denominator)
        else:
            try:
                return RationalFunction(self.numerator + other * self.denominator, self.denominator)
            except:
                return NotImplemented
    
    
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
        if isinstance(other, RationalFunction):
            return RationalFunction(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, Polynomial):
            return RationalFunction(self.numerator * other, self.denominator)
        else:
            try:
                return RationalFunction(self.numerator * other, self.denominator)
            except:
                return NotImplemented
        
    
    def __rmul__(self, other):
        return self * other
    
    
    def __imul__(self, other):
        return self * other
    
    
    def __truediv__(self, other):
        if isinstance(other, RationalFunction):
            return RationalFunction(self.denominator * other.denominator, self.numerator * other.numerator)
        elif isinstance(other, Polynomial):
            return RationalFunction(self.denominator, self.numerator * other)
        else:
            try:
                return RationalFunction(self.denominator, self.numerator * other)
            except:
                return NotImplemented
        

    def __rtruediv__(self, other):
        return RationalFunction(other) / self
    

    def __itruediv__(self, other):
        return self / other
    

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"Exponentiation is only supported with integer exponents")

        if other == 0:
            return RationalFunction(Polynomial({Monomial.constant(): 1}, self.field), Polynomial({Monomial.constant(): 1}, self.field), field = self.field)
        elif other < 0:
            self = RationalFunction(Polynomial({Monomial.constant(): 1}, self.field), Polynomial({Monomial.constant(): 1}, self.field), field = self.field) / self
            other = -other

        result = 1
        base = RationalFunction(self.numerator, self.denominator)

        while other > 0:
            if other % 2 == 1:
                result *= base
            base *= base
            other //= 2

        return result
    
    
    def __ipow__(self, other):
        return self ** other


    def __hash__(self):
        return hash((self.numerator, self.denominator))
    

    def __copy__(self):
        return RationalFunction(self.numerator, self.denominator)
    

    def reduce(self) -> None:
        """
        Reduce the rational function to its simplest form.
        """
        d = polynomialGCD(self.numerator, self.denominator)
        variables = list(set(self.numerator.getVariables) | set(self.denominator.getVariables))
        u, _ = polynomialReduce(self.numerator, [d], variables)
        v, _ = polynomialReduce(self.denominator, [d], variables)
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'numerator', u[0])
        object.__setattr__(self, 'denominator', v[0])
        object.__setattr__(self, '_initialized', True)


    @property
    def getVariables(self) -> list[str]:
        """
        Returns
        -------
        The list of variables in the rational function sorted alphabetically.
        """
        return sorted(list(set(self.numerator.getVariables) | set(self.denominator.getVariables)))