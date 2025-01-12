def _euclidAlgorithm2(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def _extendedEuclidAlgorithm2(a: int, b: int) -> tuple[int, int, int]:
    x, y, prev_x, prev_y = 0, 1, 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a % b
        x, prev_x = prev_x - quotient * x, x
        y, prev_y = prev_y - quotient * y, y
    return a, prev_x, prev_y
    

def integerGCD(*args: int) -> int:
    """
    Parameters
    ----------
    *args : int or list or set

    Returns
    -------
    The greatest common divisor of the provided integers.
    
    Raises
    ------
    ValueError: If no arguments are provided or one of the arguments is not integer.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided.")
    elif len(args) == 1 and isinstance(args[0], (list, set)):
        args = tuple(args[0])
    elif not all(isinstance(arg, int) for arg in args):
        raise ValueError("All arguments must be integers.")
    result = args[0]
    for i in range(1, len(args)):
        result = _euclidAlgorithm2(result, args[i])
    return abs(result)


def integerLCM(*args: int) -> int:
    """
    Parameters
    ----------
    *args : int or list or set

    Returns
    -------
    The least common multiple of the provided integers.

    Raises
    ------
    ValueError: If no arguments are provided or one of the arguments is not integer.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided.")
    elif len(args) == 1 and isinstance(args[0], (list, set)):
        args = tuple(args[0])
    elif not all(isinstance(arg, int) for arg in args):
        raise ValueError("All arguments must be integers.")
    result = args[0]
    for i in range(1, len(args)):
        result *=  args[i] // _euclidAlgorithm2(result, args[i])
    return abs(result)


def extendedEuclidAlgorithm(*args: int) -> tuple[int, list[int]]:
    """
    Extended Euclidean Algorithm for multiple integers.
    
    Parameters
    ----------
    *args : int or list or set

    Returns
    -------
    (d, coefficients) where d = gcd(a1, a2, ..., an) and coefficients = [u1, u2, ..., un] where u1*a1 + u2*a2 + ... + un*an = d.
    
    Raises
    ------
    ValueError: If no arguments are provided or not all are integers.
    """
    if len(args) == 0:
        raise ValueError("At least one argument must be provided.")
    if not all(isinstance(arg, int) for arg in args):
        raise ValueError("All arguments must be integers.")
    
    d, x, y = _extendedEuclidAlgorithm2(args[0], args[1])
    coefficients = [x, y]
    
    for i in range(2, len(args)):
        d, x, y = _extendedEuclidAlgorithm2(d, args[i])
        coefficients = [c * x for c in coefficients] + [y]
    
    return d, coefficients


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