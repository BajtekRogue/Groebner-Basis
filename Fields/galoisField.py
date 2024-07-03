
class GaloisField():
    """
    Class representing integers modulo a prime number. Supported primes up to 1000. To extend prime range to N run getMorePrimes(N).
    """
    PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997}
    
    def __init__(self, number, prime) -> None:
        
        if prime not in GaloisField.PRIMES:
            raise ValueError(f"Not a prime {prime}")
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'number', number % prime)
        object.__setattr__(self, 'prime', prime)
        object.__setattr__(self, '_initialized', True)


    def __setattr__(self, name, value):
        if self.__dict__.get('_initialized', False):
            raise AttributeError(f"{self.__class__.__name__} does not support attribute assignment")
        super().__setattr__(name, value)


    def __delattr__(self, name):
        raise AttributeError(f"{self.__class__.__name__} does not support attribute deletion")
        
        
    def __str__(self):
        def toSubscript(num):
            subscripts = {'0': '₀','1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}
            return ''.join(subscripts[digit] for digit in str(num))
        return "[" + str(self.number) + "]" + toSubscript(self.prime)

    
    def __repr__(self):
        return self.__str__()
    
    
    def __eq__(self, other):
        if isinstance(other, GaloisField):
            return self.number == other.number and self.prime == other.prime
        else:
            return NotImplemented
    
    
    def __pos__(self):
        return self

    
    def __neg__(self):
        return GaloisField(self.prime - self.number, self.prime)
    
    
    def __add__(self, other):
        if isinstance(other, GaloisField) and self.prime == other.prime:
            return GaloisField(self.number + other.number, self.prime)
        elif isinstance(other, int):
            return GaloisField(self.number + other, self.prime)
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
        if isinstance(other, GaloisField) and self.prime == other.prime:
            return GaloisField(self.number * other.number, self.prime)
        elif isinstance(other, int):
            return GaloisField(self.number * other, self.prime)
        else:
            return NotImplemented
        
    
    def __rmul__(self, other):
        return self * other

    
    def __imul__(self, other):
        return self * other
    
    
    def __truediv__(self, other):

        def extendedEuclidAlgorithm(a, b):
            x, y, prev_x, prev_y = 0, 1, 1, 0
            while b != 0:
                quotient = a // b
                a, b = b, a % b
                x, prev_x = prev_x - quotient * x, x
                y, prev_y = prev_y - quotient * y, y
            return a, prev_x, prev_y
        
        if isinstance(other, GaloisField) and self.prime == other.prime:
            _, x, _ = extendedEuclidAlgorithm(other.number, self.prime)
            return self * GaloisField(x, self.prime)
        elif isinstance(other, int):
            _, x, _ = extendedEuclidAlgorithm(other, self.prime)
            return self * GaloisField(x, self.prime)
        else:
            return NotImplemented
        

    def __rtruediv__(self, other):
        return GaloisField(other, self.prime) / self
    

    def __itruediv__(self, other):
        return self / other
    

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"Exponentiation is only supported with integer exponents")

        if other == 0:
            return GaloisField(1, self.prime)
        elif other < 0:
            self = GaloisField(1, self.prime) / self
            other = -other

        result = 1
        base = self

        while other > 0:
            if other % 2 == 1:
                result *= base
            base *= base
            other //= 2

        return result
    
    
    def __ipow__(self, other):
        return self ** other


    def __abs__(self):
        return self.number

    
    def __int__(self):
        return self.number
    

    def __hash__(self):
        return hash((self.number, self.prime))
    

    @staticmethod
    def getMorePrimes(N) -> None:
        """
        Extend the range of supported primes up to N.
        """

        isPrime = [True] * (N + 1)
        isPrime[0] = isPrime[1] = False
        for i in range(2, N + 1):
            if isPrime[i]:
                GaloisField.PRIMES.add(i)
                for j in range(i * i, N + 1, i):
                    isPrime[j] = False