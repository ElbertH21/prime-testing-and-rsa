# Prime Testing and RSA

Prime number algorithms and RSA encryption written from scratch in Python. It compares three ways to find or test primes (trial division, the Sieve of Eratosthenes, and Miller-Rabin), then uses Miller-Rabin to generate RSA keys.

Team project for **CS404: Algorithms and Complexity**, University of Missouri–Kansas City, Spring 2026.
Forked from the team repository [TimothyHuff89/CS-404-project](https://github.com/TimothyHuff89/CS-404-project).

## Who did what

| Part | Files | Author |
|---|---|---|
| Miller-Rabin primality test | `MillerRabin.py` | Elbert Henriquez |
| RSA key generation, encryption, decryption | `RSA.py` | Elbert Henriquez |
| Test and timing harness | `main.py` | Elbert Henriquez |
| Trial division | `TrialDivision.py` | Timothy Huff |
| Sieve of Eratosthenes, random and adversarial test generators | `Primeproject.py` | Timothy Huff |

## What's inside

**Trial division** (`TrialDivision.py`) checks every odd divisor up to √n.
- Testing one number: O(√n)
- Listing all primes up to n: O(n√n / log n)

**Sieve of Eratosthenes** (`Primeproject.py`) crosses out multiples of each prime, starting at p².
- Time: O(n log log n)
- Space: O(n)

**Miller-Rabin** (`MillerRabin.py`) is a probabilistic primality test, the same kind of test real crypto libraries use to make RSA keys.
- Writes n − 1 as 2^r · d, then checks random "witnesses" using fast modular exponentiation.
- With 10 rounds, the chance of calling a composite number prime is at most (1/4)^10 ≈ 9.5 × 10⁻⁷.
- Time: O(k · log² n), which is much faster than trial division for large numbers.

**RSA** (`RSA.py`), textbook version:
1. Generate two large primes p and q: random candidates come from Python's `secrets` module (a secure random source) and are tested with Miller-Rabin. The top two bits are set, so n has the full bit length.
2. Compute n = p · q and Euler's totient φ = (p − 1)(q − 1).
3. Use the standard public exponent e = 65537.
4. Find the private exponent d = e⁻¹ mod φ with the extended Euclidean algorithm.
5. Encrypt with c = m^e mod n and decrypt with m = c^d mod n.

The demos use 512-bit and 1024-bit primes, which give 1024-bit and 2048-bit keys.

## Testing (`main.py`)

- Compares trial division and the sieve on random ranges (both must return the same primes).
- Checks trial division and Miller-Rabin against known primes and non-primes.
- Runs Miller-Rabin on "adversarial" inputs that are likely to expose bugs: numbers near perfect squares, products of two factors, large numbers, and random odd numbers.
- Times each method: the sieve and trial division up to 1,000,000, Miller-Rabin on the Mersenne prime 2^61 − 1, and RSA key generation.
- Runs an RSA round trip: encrypt a message, decrypt it, and confirm it matches.

`MillerRabin.py` also cross-checks itself against trial division for every number from 0 to 200.

## How to run

You only need Python 3 (no extra packages).

```bash
python main.py          # full demo: all tests, timings, and RSA
python MillerRabin.py   # Miller-Rabin tests + cross-check with trial division
python RSA.py           # RSA key generation and encrypt/decrypt demo
```

## Changes made after the course

- Prime candidates in `RSA.py` now come from `secrets` (a secure random source) instead of `random`.
- Fixed a comment in `main.py`: Miller-Rabin tests whether a number is prime; it does not factor it.

## Limits (this is for learning, not real security)

- **No padding.** Real RSA uses a padding scheme such as OAEP. Without it, the same message always gives the same ciphertext.
- **No protection against timing attacks.**
- RSA is only secure because factoring n is hard for normal computers. Shor's algorithm on a large quantum computer would break it, which is why post-quantum cryptography exists.
