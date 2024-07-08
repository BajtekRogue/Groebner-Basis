from math import log
from NumberTheory.primes import PRIMES, PRIMES_UPPER_BOUND, sieveOfEratosthenes, primeFactorization

def eulerTotientFunction(n: int, usePrimeFactorization = True) -> int:
    """
    Returns
    -------
    Euler's totient function φ(n) of n. By default, it's done by the formula φ(n) = n * Π (1 - 1/p) for prime factors of n. Setting usePrimeFactorization to False will use the formula φ(n) = Σ gcd(i, n) for i = 1 to n. Definition takes O(n * log(n)) time, product formula takes O(n / log(n)) amortized time.

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if usePrimeFactorization:
        if PRIMES_UPPER_BOUND < n:
            sieveOfEratosthenes(n)
        result = n
        for p in PRIMES:
            if n % p == 0:
                result *= p - 1
                result //= p
            if p > n:
                break
        return int(result)
    else:
        def gcd(a: int, b: int) -> int:
            while b != 0:
                a, b = b, a % b
            return a
        
        result = 1
        for i in range(2, n):
            if gcd(i, n) == 1:
                result += 1
        return result


def divisors(n: int) -> list[int]:
    """
    Returns
    -------
    Divisors of n as a list in increasing order in O(sqrt(n)) time.

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    
    result1 = []
    result2 = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            result1.append(i)
            result2.append(n // i)
        i += 1

    if result1[-1] == result2[-1]:
        result2.pop()

    result2.reverse()
    return result1 + result2


def divisorFunction(n: int, s: complex = 1, usePrimeFactorization = True) -> complex:
    """
    Returns
    -------
    σ_s(n), sum of the s-th powers of divisors of n. The formula σ_s(n) = Π (p^((a+1)s) - 1) / (p^a - 1) for distinct prime factors of n is used by default. Setting usePrimeFactorization to False will use the definition.

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The first argument must be a positive integer.")

    if usePrimeFactorization:
        if PRIMES_UPPER_BOUND < n:
            sieveOfEratosthenes(n)
        result = 1
        for p, a in primeFactorization(n).items():
            result *= (p ** ((a + 1) * s) - 1) / (p ** s - 1)
        return int(result) if result.is_integer() else result
    else:
        result = 0
        for i in divisors(n):
            result += i ** s
        return result


def mobiusFunction(n: int) -> int:
    """
    Returns
    -------
    Möbius function μ(n).

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if n == 1:
        return 1

    if PRIMES_UPPER_BOUND ** 2 < n:
        sieveOfEratosthenes(n)

    count = 0
    for p in PRIMES:
        if n % (p ** 2) == 0:
            return 0
        elif n % p == 0:
            count += 1
        elif p > n:
            break
    return (-1) ** count


def littleOmegaFunction(n: int) -> int:
    """
    Returns
    -------
    ω(n) equal to the number of prime factors of n.

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if n == 1:
        return 0

    if PRIMES_UPPER_BOUND < n:
        sieveOfEratosthenes(n)

    result = 0
    for p in PRIMES:
        if n % p == 0:
            result += 1
    return result


def bigOmegaFunction(n: int) -> int:
    """
    Returns
    -------
    Ω(n) equal to the number of prime factors of n with multiplicity.

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if n == 1:
        return 0

    if PRIMES_UPPER_BOUND < n:
        sieveOfEratosthenes(n)

    pF = primeFactorization(n)
    return sum(pF.values())


def liouvilleLambdaFunction(n: int) -> int:
    """
    Returns
    -------
    Liouville function λ(n)

    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    return (-1) ** bigOmegaFunction(n)


def vonMangoldtFunction(n : int) -> float:
    """
    Returns
    -------
    Return the von Mangoldt function Λ(n)

    Raises
    ------
    ValueError: If n is not a positive integer.
    """   
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if n == 1:
        return 0
    
    pF = primeFactorization(n)
    if len(pF) == 1:
        return log(next(iter(pF.keys())))
    else:
        return 0
