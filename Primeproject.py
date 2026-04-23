import random
import TrialDivision


#Generate Primes using Sieve of Eratosthenes
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


#Test function for Trial division
def random_prime_test_cases(count, max_n):

    #Generate `count` random integers in [0, max_n] for testing is_prime_trial.
    #Returns a list of (n, expected_result) tuples.

    cases = []
    for _ in range(count):
        n = random.randint(0, max_n)
        expected = TrialDivision.is_prime_trial(n)
        cases.append((n, expected))
    return cases

#Test function to ensure both Trial and Sieve are same output
def random_range_prime_tests(count, max_n):
    
    #Generate `count` random values of n and compare trial-division prime
    #generation against the sieve implementation.
    
    for _ in range(count):
        n = random.randint(1, max_n)
        primes_trial = TrialDivision.generate_primes_trial(n)
        primes_sieve = sieve(n)

        if primes_trial != primes_sieve:
            print(f"Mismatch at n={n}")
            print("Trial:", primes_trial)
            print("Sieve:", primes_sieve)
            return

    print(f"All {count} random tests passed up to n={max_n}")

def adversarial_prime_tests(count, max_n):
    
    #Generate adversarial test cases that are more likely to expose bugs.
    
    #create empty list to stor test cases
    tests = []

    #loop for count amount of random inputs
    for _ in range(count):

        #pick a random float between 0 and 1
        choice = random.random()

        #case to generate large numbers
        if choice < 0.25:
            n = random.randint(max_n // 2, max_n)

        #test case for almost perfect square
        elif choice < 0.50:
            base = random.randint(1, int(max_n**0.5))
            n = base * base + random.randint(-2, 2)

        #multiple of two random numbers
        elif choice < 0.75:
            a = random.randint(2, int(max_n**0.5))
            b = random.randint(2, int(max_n**0.5))
            n = a * b

        # Random odd number (higher chance of prime)
        else:
            n = random.randrange(3, max_n, 2)

        expected = TrialDivision.is_prime_trial(n)
        tests.append((n, expected))

    return tests

