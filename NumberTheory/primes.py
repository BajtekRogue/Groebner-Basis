
PRIMES = []
PRIMES_UPPER_BOUND = 1_000_000
PRIMES_SET = set()

def sieveOfEratosthenes(N = PRIMES_UPPER_BOUND) -> None:
    """
    Generate prime numbers up to N.
    """
    global PRIMES, PRIMES_UPPER_BOUND, PRIMES_SET
    PRIMES_UPPER_BOUND = N
    PRIMES = []
    isPrime = [True] * (N + 1)
    isPrime[0] = isPrime[1] = False
    for i in range(2, N + 1):
        if isPrime[i]:
            PRIMES.append(i)
            for j in range(i * i, N + 1, i):
                isPrime[j] = False
    PRIMES_SET = set(PRIMES)


def primeFactorization(n: int) -> dict[int, int]:
    """
    Returns
    -------
    The prime factorization of n as dict with prime factors as keys and their powers as values.
    
    Raises
    ------
    ValueError: If n is not a positive integer.
    """
    if n < 1 or not isinstance(n, int):
        raise ValueError("The argument must be a positive integer.")
    if PRIMES_UPPER_BOUND < n:
        sieveOfEratosthenes(n)

    result = {}
    for p in PRIMES:
        if n % p == 0:
            result[p] = 0
            while n % p == 0:
                result[p] += 1
                n //= p
        elif p > n:
            break
    return result


sieveOfEratosthenes()