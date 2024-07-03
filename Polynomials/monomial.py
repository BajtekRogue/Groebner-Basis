
class Monomial:
    """
    Represents a monomial like x^2y^3z^4 as {'x': 2, 'y': 3, 'z': 4}. Immutable. If Monomial.STRICT is set to True, contructor will check if variables are allowed and exponents are natural numbers.
    """
    
    VARIABLES = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω'}
    DUMMY = '_'

    def __init__(self, exponent: dict[str, int]):
        exponent = {var: exp for var, exp in exponent.items() if exp != 0}
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, 'exponent', dict(sorted(exponent.items())))
        object.__setattr__(self, '_initialized', True)


    def __setattr__(self, attr, value):
        if self.__dict__.get('_initialized', False):
            raise AttributeError(f"{self.__class__.__name__} does not support attribute assignment")
        super().__setattr__(attr, value)


    def __delattr__(self, attr):
        raise AttributeError(f"{self.__class__.__name__} does not support attribute deletion")


    def __str__(self):
        def toSuperscript(num):
            superscripts = {'0': '⁰','1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
            return ''.join(superscripts[digit] for digit in str(num))

        if not self.exponent:
            return '1'
        result = ''
        for var, exp in self.exponent.items():
            if exp == 1:
                result += var
            else:
                result += var + toSuperscript(exp)

        return result


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        return self.exponent == other.exponent
    

    def __ne__(self, other):
        return not self.__eq__(other)


    def __mul__(self, other):
        exponent = self.exponent.copy()
        for var, exp in other.exponent.items():
            if var in exponent:
                exponent[var] += exp
            else:
                exponent[var] = exp
        return Monomial(exponent)


    def __rmul__(self, other):
        return self * other
    
    
    def __imul__(self, other):
        for var, exp in other.exponent.items():
            if var in self.exponent:
                self.exponent[var] += exp
            else:
                self.exponent[var] = exp
        return self
    

    def __truediv__(self, other):
        exponent = self.exponent.copy()
        for var, exp in other.exponent.items():
            if var in exponent:
                exponent[var] -= exp
            else:
                exponent[var] = -exp
        if all(exp >= 0 for exp in exponent.values()): 
            return Monomial(exponent)
        else:
            raise ValueError(f'Cannot divide monomials {self} by {other}')
    

    def __itruediv__(self, other):
        for var, exp in other.exponent.items():
            if var in self.exponent:
                self.exponent[var] -= exp
            else:
                self.exponent[var] = -exp
        if all(exp >= 0 for exp in self.exponent.values()): 
            return self
        else:
            raise ValueError(f'Cannot divide monomials {self} by {other}')
    

    def __rtruediv__(self, other):
        return self * other
    

    def __hash__(self):
        return hash(tuple(sorted(self.exponent.items())))
    

    def __len__(self):
        return len(self.exponent)
    

    def degree(self):
        """
        Returns
        -------
        The degree of the monomial is sum of it's exponents.
        """
        return sum(self.exponent.values())
    
    
    @staticmethod
    def makeFromTuples(exponents: tuple[int], variables: tuple[str]):
        """
        Returns
        -------
        For example converts (1, 2), ('x', 'y') into {'x': 1, 'y': 2}
        """
        return Monomial(dict(zip(variables, exponents)))


    @staticmethod
    def constant():
        """
        Returns a constant monomial 1
        """
        return Monomial({})


    @staticmethod
    def leastCommonMultiple(alpha, beta):
        """
        Returns
        -------
        The least common multiple of two monomials. For example lcm(x^2y^5, x^3y^2) = x^3*y^5
        """
        variables = sorted(list(set(alpha.exponent.keys()).union(set(beta.exponent.keys()))))
        result = []

        for i in variables:
            if i not in alpha.exponent and i in beta.exponent:
                result.append(beta.exponent[i])
            elif i in alpha.exponent and i not in beta.exponent:
                result.append(alpha.exponent[i])
            else:
                result.append(max(alpha.exponent[i], beta.exponent[i]))

        return Monomial.makeFromTuples(tuple(result), variables)
    

    @property
    def getVariables(self) -> list[str]:
        """
        Returns
        -------
        List of variables in the monomial.
        """
        return list(self.exponent.keys())
