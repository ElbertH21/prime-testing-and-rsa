import Primeproject
import TrialDivision

if __name__ == "__main__":

    # Generate primes up to 50 and confirm against the known list
    print("\nTrial Division Primes up to 50:")
    print(TrialDivision.generate_primes_trial(50))

    print(f"\nSieve Primes up to 50: \n{Primeproject.sieve(50)}\n")

    #test both functions Trial/Sieve against each other
    Primeproject.random_range_prime_tests(10, 10_000)
    print()

        # Test prime checking on a handful of known cases
    test_cases = [
        (0, False), (1, False), (2, True), (3, True), (4, False),
        (17, True), (25, False), (97, True), (100, False), (7919, True),
    ]
    for n, expected in test_cases:
        result = TrialDivision.is_prime_trial(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_prime_trial({n}) = {result}")

    print()
    #test random cases to see if prime
    for n, expected in Primeproject.random_prime_test_cases(10, 10_000):
        print(f"Test is_prime_trial({n}) -> {expected}")

    print()
    #test more cases that are meant to fail (fuzzing)
    for n, expected in Primeproject.adversarial_prime_tests(10, 100_000):
        print(f"{n} -> {expected}")

