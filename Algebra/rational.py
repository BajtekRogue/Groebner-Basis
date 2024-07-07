
class rational:
    """
    Fraction in reduced form with positive denominator
    """ 
    def __init__(self, numerator, denominator = 1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        if isinstance(numerator, float):
            numerator = round(numerator, 4)
            numerator = round(numerator * 10**4)
            denominator = 10**4
            
        def gcd(a: int, b: int) -> int:
            while b != 0:
                a, b = b, a % b
            return a
        
        d = gcd(numerator, denominator)
        numerator //= d
        denominator //= d

        if denominator < 0:
            numerator = -numerator
            denominator = -denominator

        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'numerator', numerator)
        object.__setattr__(self, 'denominator', denominator)
        object.__setattr__(self, '_initialized', True)


    def __setattr__(self, name, value):
        if self.__dict__.get('_initialized', False):
            raise AttributeError(f"{self.__class__.__name__} does not support attribute assignment")
        super().__setattr__(name, value)


    def __delattr__(self, name):
        raise AttributeError(f"{self.__class__.__name__} does not support attribute deletion")


    def __str__(self):
        if self.denominator == 1:
            return f"{self.numerator}" 
        else:
            return f"{self.numerator}/{self.denominator}"  

    
    def __repr__(self):
        return self.__str__()
    
    
    def __eq__(self, other):
        if isinstance(other, rational):
            return self.numerator == other.numerator and self.denominator == other.denominator
        elif isinstance(other, int):
            return self.numerator == other and self.denominator == 1
        elif isinstance(other, float):
            return (self.numerator / self.denominator - other) < 0.0001 
        else:
            return False
    
    
    def __ne__(self, other):
        return not self == other
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        return rational(-self.numerator, self.denominator)
     
    
    def __add__(self, other):
        if isinstance(other, rational):
            return rational(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)
        elif isinstance(other, int):
            return rational(self.numerator + other * self.denominator, self.denominator)
        elif isinstance(other, float):
            return self + rational(other)
        else:
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
        if isinstance(other, rational):
            return rational(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, int):
            return rational(self.numerator * other, self.denominator)
        elif isinstance(other, float):
            return self * rational(other)
        else:
            return NotImplemented
        
    
    def __rmul__(self, other):
        return self * other
    
    
    def __imul__(self, other):
        return self * other
    
    
    def __truediv__(self, other):
        if isinstance(other, rational) and other.numerator != 0:
            return self * rational(other.denominator, other.numerator)
        elif isinstance(other, int) and other != 0:
            return self * rational(1, other)
        elif isinstance(other, float) and abs(other) > 0.0001:
            self /= rational(other)
            return self
        else:
            return NotImplemented
        

    def __rtruediv__(self, other):
        return rational(other) / self
    

    def __itruediv__(self, other):
        return self / other
    

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"Exponentiation is only supported with integer exponents")

        if other == 0:
            return rational(1)
        elif other < 0:
            self = rational(1) / self
            other = -other

        result = 1
        base = rational(self.numerator, self.denominator)

        while other > 0:
            if other % 2 == 1:
                result *= base
            base *= base
            other //= 2

        return result
    
    
    def __ipow__(self, other):
        return self ** other


    def __lt__(self, other):
        if isinstance(other, rational):
            return self.numerator * other.denominator < other.numerator * self.denominator
        elif isinstance(other, int):
            return self < rational(other, 1)
        elif isinstance(other, float):
            return self.numerator / self.denominator < other
        else:
            return NotImplemented
    

    def __le__(self, other):
        if isinstance(other, rational):
            return self.numerator * other.denominator <= other.numerator * self.denominator
        elif isinstance(other, int):
            return self <= rational(other, 1)
        elif isinstance(other, float):
            return self.numerator / self.denominator <= other
        else:
            return NotImplemented
        
    
    def __gt__(self, other):
        if isinstance(other, rational):
            return self.numerator * other.denominator > other.numerator * self.denominator
        elif isinstance(other, int):
            return self > rational(other, 1)
        elif isinstance(other, float):
            return self.numerator / self.denominator > other
        else:
            return NotImplemented
    

    def __ge__(self, other):
        if isinstance(other, rational):
            return self.numerator * other.denominator >= other.numerator * self.denominator
        elif isinstance(other, int):
            return self >= rational(other, 1)
        elif isinstance(other, float):
            return self.numerator / self.denominator >= other
        else:
            return NotImplemented
    
    
    def __abs__(self):
        return rational(abs(self.numerator), self.denominator)


    def __float__(self):
        return self.numerator / self.denominator
    
    
    def __int__(self):
        return self.numerator // self.denominator


    def __hash__(self):
        return hash((self.numerator, self.denominator))
    

    def __copy__(self):
        return rational(self.numerator, self.denominator)
    