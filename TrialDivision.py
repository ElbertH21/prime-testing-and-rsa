"""
Trial Division for prime testing and prime generation.

Two functions:
    is_prime_trial(n) --> tests whether a single number n is prime
    generate_primes_trial(n) --> generates all primes up to n

Both use the same core idea: a number n is prime if no integer in [2, sqrt(n)]
divides it evenly. We skip even divisors > 2 as a small optimization.
"""


def is_prime_trial(n):
    """
    Return True if n is prime, False otherwise, using trial division.

    Time complexity: O(sqrt(n))
        - We only check divisors up to sqrt(n) because if n = a * b
          and both a, b > sqrt(n), then a * b > n, a contradiction.
        - Skipping even numbers roughly halves the constant factor
          but does not change the asymptotic complexity.
    Space complexity: O(1)
    """
    # Handle small cases explicitly
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Only odd divisors from 3 up to sqrt(n)
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2

    return True


def generate_primes_trial(n):
    """
    Return a list of all primes <= n, using trial division on each candidate.

    Time complexity: O(n * sqrt(n) / log(n))
        - We run is_prime_trial (O(sqrt(k))) on each k from 2 to n.
        - Summing sqrt(k) from 2 to n is approximately O(n * sqrt(n)).
        - This is notably worse than the Sieve of Eratosthenes
          (O(n log log n)).
    Space complexity: O(n / log(n)) for the output list
    """
    if n < 2:
        return []

    primes = [2]
    # Only test odd candidates; evens > 2 are never prime
    for candidate in range(3, n + 1, 2):
        if is_prime_trial(candidate):
            primes.append(candidate)

    return primes


if __name__ == "__main__":
    # Test prime checking on a handful of known cases
    test_cases = [
        (0, False), (1, False), (2, True), (3, True), (4, False),
        (17, True), (25, False), (97, True), (100, False), (7919, True),
    ]
    for n, expected in test_cases:
        result = is_prime_trial(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_prime_trial({n}) = {result}")

    # Generate primes up to 50 and confirm against the known list
    print("\nPrimes up to 50:")
    print(generate_primes_trial(50))