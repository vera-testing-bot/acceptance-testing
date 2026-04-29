"""
Random number generator implemented from scratch using multiple entropy sources.

This module provides a rand() function that generates pseudo-random numbers
by combining entropy from multiple sources:
1. System time (high-precision)
2. Process ID
3. Object ID (memory address variation)
4. OS-provided entropy (when available)
"""

import time
import os
import sys
import hashlib
import threading

# Lock for thread-safe seed updates
_lock = threading.Lock()

# Internal state for the RNG
_state = None


def _get_time_entropy() -> int:
    """Get entropy from high-precision system time."""
    # Combine seconds and nanoseconds for maximum entropy
    t = time.time_ns()
    return t


def _get_pid_entropy() -> int:
    """Get entropy from process ID."""
    return os.getpid()


def _get_object_entropy() -> int:
    """Get entropy from a newly created object's memory address."""
    # Creating a new object and using its id provides memory-based entropy
    obj = object()
    return id(obj)


def _get_os_entropy() -> int:
    """Get entropy from OS-provided random source when available."""
    try:
        # Use os.urandom for OS entropy (non-blocking)
        random_bytes = os.urandom(8)
        return int.from_bytes(random_bytes, byteorder='big')
    except Exception:
        # Fallback if urandom is not available
        return _get_time_entropy() ^ _get_pid_entropy()


def _mix_entropy(sources: list[int]) -> int:
    """
    Mix multiple entropy sources into a single seed value.

    Uses a combination of XOR and bit rotation to ensure good mixing.
    """
    result = 0
    for i, source in enumerate(sources):
        # Rotate and mix each source
        rotation = (i * 17) % 64
        rotated = ((source << rotation) | (source >> (64 - rotation))) & 0xFFFFFFFFFFFFFFFF
        result ^= rotated
        # Additional mixing with multiplication (golden ratio approximation)
        result = (result * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    return result


def _initialize_state() -> int:
    """Initialize the RNG state using multiple entropy sources."""
    entropy_sources = [
        _get_time_entropy(),
        _get_pid_entropy(),
        _get_object_entropy(),
        _get_os_entropy(),
    ]
    return _mix_entropy(entropy_sources)


def _xorshift64(state: int) -> tuple[int, int]:
    """
    Xorshift64* random number generator.

    This is a well-known PRNG algorithm by George Marsaglia.
    Returns a tuple of (new_state, random_value).
    """
    # xorshift64* algorithm
    state ^= (state >> 12) & 0xFFFFFFFFFFFFFFFF
    state ^= (state << 25) & 0xFFFFFFFFFFFFFFFF
    state ^= (state >> 27) & 0xFFFFFFFFFFFFFFFF
    # Multiplier for xorshift64*
    result = (state * 0x2545F4914F6CDD1D) & 0xFFFFFFFFFFFFFFFF
    return state, result


def rand() -> float:
    """
    Generate a random float in the range [0.0, 1.0).

    This function uses a custom random number generator that combines
    entropy from multiple sources:
    - High-precision system time
    - Process ID
    - Memory address (object ID)
    - OS-provided entropy (when available)

    The implementation uses the xorshift64* algorithm for generating
    pseudo-random numbers from the mixed entropy seed.

    Returns:
        A float value in the range [0.0, 1.0).

    Example:
        >>> random_val = rand()
        >>> 0.0 <= random_val < 1.0
        True
    """
    global _state

    with _lock:
        if _state is None:
            _state = _initialize_state()

        _state, value = _xorshift64(_state)

    # Convert to float in range [0.0, 1.0)
    # Use 53 bits of precision (same as Python's random module)
    return (value >> 11) / (1 << 53)


def randint(a: int, b: int) -> int:
    """
    Generate a random integer in the range [a, b] (inclusive).

    Args:
        a: Lower bound (inclusive)
        b: Upper bound (inclusive)

    Returns:
        A random integer N such that a <= N <= b.

    Example:
        >>> n = randint(1, 6)  # Simulate a dice roll
        >>> 1 <= n <= 6
        True
    """
    if a > b:
        raise ValueError(f"Empty range in randint({a}, {b})")

    range_size = b - a + 1
    # Use rejection sampling to avoid bias
    while True:
        value = int(rand() * range_size * 2)  # Generate extra range
        if value < range_size:
            return a + value


def seed(s: int | None = None) -> None:
    """
    Seed the random number generator.

    Args:
        s: The seed value. If None, the RNG will be re-initialized
           with fresh entropy from multiple sources.

    Example:
        >>> seed(42)  # Reproducible sequence
        >>> a = rand()
        >>> seed(42)
        >>> b = rand()
        >>> a == b
        True
    """
    global _state

    with _lock:
        if s is None:
            _state = _initialize_state()
        else:
            # Mix the provided seed similar to entropy mixing
            _state = _mix_entropy([s, _get_pid_entropy()])


def random_bytes(n: int) -> bytes:
    """
    Generate n random bytes.

    Args:
        n: Number of bytes to generate.

    Returns:
        A bytes object containing n random bytes.

    Example:
        >>> data = random_bytes(16)
        >>> len(data) == 16
        True
    """
    result = bytearray()
    while len(result) < n:
        # Generate 8 bytes at a time
        value = int(rand() * (1 << 64))
        result.extend(value.to_bytes(8, byteorder='big'))
    return bytes(result[:n])


def random_point_in_sphere(n: int) -> list[float]:
    """
    Generate a random point inside an n-dimensional unit sphere.

    Args:
        n: The number of dimensions. Must be greater than zero.

    Returns:
        A list of n coordinates representing a point uniformly sampled
        from the n-dimensional unit sphere centered at the origin.
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")

    while True:
        point = [(2.0 * rand()) - 1.0 for _ in range(n)]
        radius_squared = sum(value * value for value in point)
        if radius_squared <= 1.0:
            return point
