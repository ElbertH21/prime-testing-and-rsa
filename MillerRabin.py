"""
Miller-Rabin probabilistic primality test.

One function:
    is_prime_miller_rabin(n, k=10) -- tests whether n is prime using k rounds

Unlike Trial Division which is deterministic, Miller-Rabin is probabilistic.
Each round independently has at most a 1/4 chance of a false positive, so
with k=10 rounds the probability of incorrectly calling a composite number
prime is at most (1/4)^10 ≈ 9.5 * 10^-7, which is negligible in practice.
This is the same approach used by real cryptographic libraries (e.g. OpenSSL)
when generating RSA keys.
"""

import random


def is_prime_miller_rabin(n, k=10):
    """
    Return True if n is probably prime, False if n is definitely composite.

    Parameters:
        n : int  -- the number to test (must be a positive integer)
        k : int  -- number of rounds (default 10). Higher k = more accuracy.
                    Each round reduces the false positive probability by 1/4.

    Time complexity: O(k * log^2(n))
        - Each round does O(log n) modular multiplications via fast exponentiation.
        - Each modular multiplication on an n-bit number costs O(log n).
        - k rounds total gives O(k * log^2(n)).
        - Far faster than Trial Division's O(sqrt(n)) for large n, which is
          the entire reason Miller-Rabin is used in cryptography.
    Space complexity: O(log n) for intermediate values during modular exponentiation.

    How it works:
        1. Write n - 1 as 2^r * d where d is odd (factor out powers of 2).
        2. Pick a random witness a in [2, n-2].
        3. Compute x = a^d mod n.
        4. If x == 1 or x == n-1, this round passes (n might be prime).
        5. Otherwise square x up to r-1 times. If we reach n-1, round passes.
        6. If we never reach 1 or n-1, n is definitely composite.
        7. Repeat k times. If all rounds pass, n is probably prime.
    """
    # Handle small and trivial cases explicitly
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Step 1: write n-1 as 2^r * d with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Step 2: run k independent rounds
    for _ in range(k):
        # Pick a random witness a in [2, n-2]
        a = random.randrange(2, n - 1)

        # Step 3: compute a^d mod n using Python's built-in fast modular exponentiation
        x = pow(a, d, n)

        # Step 4: if x is 1 or n-1 this round is inconclusive (probably prime)
        if x == 1 or x == n - 1:
            continue

        # Step 5: square x up to r-1 times looking for n-1
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # Step 6: never reached n-1, so n is definitely composite
            return False

    # Step 7: all k rounds passed — n is probably prime
    return True


# Quick sanity check when run directly
if __name__ == "__main__":
    # Known primes and composites
    test_cases = [
        (0, False), (1, False), (2, True), (3, True), (4, False),
        (17, True), (25, False), (97, True), (100, False), (7919, True),
        # Large prime — this is where Miller-Rabin shines over Trial Division
        (2**61 - 1, True),   # Mersenne prime
        (2**61 - 2, False),  # Clearly composite (even)
    ]

    print("Primality tests:")
    for n, expected in test_cases:
        result = is_prime_miller_rabin(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_prime_miller_rabin({n}) = {result}")

    # Cross-check with Trial Division on all numbers up to 200
    print("\nCross-checking against Trial Division for n in [0, 200]...")
    from TrialDivision import is_prime_trial
    mismatches = []
    for n in range(201):
        if is_prime_trial(n) != is_prime_miller_rabin(n):
            mismatches.append(n)
    if mismatches:
        print(f"  MISMATCHES at: {mismatches}")
    else:
        print("  All match — no discrepancies found.")