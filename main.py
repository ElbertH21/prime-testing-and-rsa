import Primeproject
import TrialDivision
import time
import MillerRabin

DIVIDER = "\n" + "─" * 60 + "\n"

def timed_call(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    print(f"{func.__name__}({args}) took {end - start:.8f} seconds")
    return result
 
 
if __name__ == "__main__":
 
    # Generate primes up to 50 and confirm against the known list
    print("\nTrial Division Primes up to 50:")
    print(TrialDivision.generate_primes_trial(50))
 
    print(DIVIDER)
    print(f"Sieve Primes up to 50: \n{Primeproject.sieve(50)}\n")

    print(DIVIDER)
    #test both functions Trial/Sieve against each other
    print("Test both functions Trial/Sieve against each other")
    Primeproject.random_range_prime_tests(10, 10_000)
    print()

    print(DIVIDER)
    
    print("Miller-Rabin up to 50:\n")
    print([n for n in range(2, 51) if MillerRabin.is_prime_miller_rabin(n, k=10)])
 
    print(DIVIDER)
    # Test prime checking on a handful of known cases
    test_cases = [
        (0, False), (1, False), (2, True), (3, True), (4, False),
        (17, True), (25, False), (97, True), (100, False), (7919, True),
    ]
    for n, expected in test_cases:
        result = TrialDivision.is_prime_trial(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_prime_trial({n}) = {result}")
 
    print(DIVIDER)
    for n, expected in test_cases:
        result = MillerRabin.is_prime_miller_rabin(n, k=10)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_prime_miller_rabin({n}) = {result}")
 
    print(DIVIDER)
    #test random cases to see if prime
    for n, expected in Primeproject.random_prime_test_cases(10, 10_000):
        print(f"Test is_prime_trial({n}) -> {expected}")
 
    print(DIVIDER)
    #test more cases that are meant to fail (fuzzing)
    for n, expected in Primeproject.adversarial_prime_tests(10, 100_000):
        print(f"{n} -> {expected}")
 
    print(DIVIDER)
    # Random test cases generated via adversarial_prime_tests() from Primeproject.py
    for n, expected in Primeproject.adversarial_prime_tests(10, 100_000):
        result = MillerRabin.is_prime_miller_rabin(n, k=10)
        print(f"{n} -> {result}")

    print(DIVIDER)

    timed_call(Primeproject.sieve, 1000000)
    timed_call(TrialDivision.generate_primes_trial, 1000000)