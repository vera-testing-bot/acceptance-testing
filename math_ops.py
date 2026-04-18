def multiply(a, b):
    return a * b


def power(base, exp):
    """
    Calculate the exponent of a number.
    
    Args:
        base: The base number
        exp: The exponent
    
    Returns:
        base raised to the power of exp
    
    Raises:
        ValueError: If base is 0 and exp is negative
    """
    if base == 0 and exp < 0:
        raise ValueError("Cannot raise 0 to a negative power")
    return base ** exp
