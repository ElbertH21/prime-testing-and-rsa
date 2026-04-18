def sieve(n):
    # Boolean array: True means "assume prime"
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            # Mark multiples of p starting from p*p
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Collect all primes
    return [i for i in range(2, n + 1) if is_prime[i]]


# Example usage:
print(sieve(50))