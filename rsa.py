"""
RSA encryption and decryption.

Three functions:
    generate_keypair(bits=512) -- generates a public/private key pair
    encrypt(message, public_key) -- encrypts an integer message
    decrypt(ciphertext, private_key) -- decrypts back to the original message

Relies on MillerRabin.is_prime_miller_rabin() for fast probabilistic prime
generation. This is the same approach used by real cryptographic libraries:
finding large primes quickly via Miller-Rabin, then building keys from them.

RSA security rests on the fact that multiplying two large primes p and q is
trivial, but factoring the result n = p * q back into p and q is computationally
infeasible for large enough bit sizes. Shor's algorithm on a quantum computer
breaks this assumption, which is why post-quantum cryptography is an active
research area.
"""

import random
from MillerRabin import is_prime_miller_rabin


# Key generation helpers

def _generate_large_prime(bits):
    """
    Return a random prime with exactly `bits` bits.

    Strategy:
        1. Generate a random odd integer of the right bit length.
        2. Test it with Miller-Rabin.
        3. Repeat until we find a prime.

    By the prime number theorem, roughly 1 in ln(2^bits) = bits * ln(2)
    candidates will be prime, so on average this loop runs O(bits) times.
    Each Miller-Rabin call costs O(k * log^2(n)), giving an overall cost of
    O(k * bits^3) per prime — acceptable for bits <= 2048 in practice.
    """
    while True:
        # Set the top two bits to 1 to guarantee the prime is `bits` bits long
        # and large enough that p * q will be 2*bits bits long.
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | (1 << bits - 2) | 1  # ensure odd + top bits set
        if is_prime_miller_rabin(candidate):
            return candidate


def _extended_gcd(a, b):
    """
    Return (gcd, x, y) such that a*x + b*y = gcd(a, b).
    Used internally by _mod_inverse.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = _extended_gcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1


def _mod_inverse(e, phi):
    """
    Return d such that (e * d) % phi == 1, i.e. the modular inverse of e mod phi.

    This is the private exponent d in RSA. We compute it via the extended
    Euclidean algorithm in O(log(min(e, phi))) steps.

    Raises ValueError if the inverse does not exist (gcd(e, phi) != 1),
    which should not happen in practice since e=65537 is chosen to be
    coprime with phi for any valid RSA prime pair.
    """
    gcd, x, _ = _extended_gcd(e % phi, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist — e and phi are not coprime.")
    return x % phi


# Public API

def generate_keypair(bits=512):
    """
    Generate an RSA public/private key pair.

    Parameters:
        bits : int -- bit length of each prime p and q (default 512).
                      The resulting modulus n = p * q will be 2*bits bits long.
                      Use 512 for fast demos, 1024 for more realistic security.

    Returns:
        public_key  : (e, n) -- exponent and modulus for encryption
        private_key : (d, n) -- exponent and modulus for decryption

    Time complexity: O(k * bits^3) dominated by prime generation.
    Space complexity: O(bits) for the key values.

    RSA key generation steps:
        1. Choose two distinct large primes p and q.
        2. Compute n = p * q  (the modulus).
        3. Compute phi = (p-1) * (q-1)  (Euler's totient).
        4. Choose e = 65537  (standard public exponent, prime, fast in binary).
        5. Compute d = modular inverse of e mod phi  (private exponent).
    """
    # Step 1: find two distinct primes of the requested bit length
    p = _generate_large_prime(bits)
    q = _generate_large_prime(bits)
    while q == p:  # astronomically unlikely but guard anyway
        q = _generate_large_prime(bits)

    # Step 2: modulus
    n = p * q

    # Step 3: Euler's totient
    phi = (p - 1) * (q - 1)

    # Step 4: public exponent — 65537 = 2^16 + 1, prime, universally standard
    e = 65537

    # Step 5: private exponent via modular inverse
    d = _mod_inverse(e, phi)

    public_key  = (e, n)
    private_key = (d, n)
    return public_key, private_key


def encrypt(message, public_key):
    """
    Encrypt an integer message using the public key.

    Parameters:
        message    : int       -- must satisfy 0 < message < n
        public_key : (e, n)   -- from generate_keypair()

    Returns:
        ciphertext : int

    Formula: ciphertext = message^e mod n
    Time complexity: O(log e * log^2 n) via fast modular exponentiation.

    Note: in production RSA, raw integers are never encrypted directly.
    A padding scheme (e.g. OAEP) is applied first. This implementation
    is intentionally simplified for demonstration purposes.
    """
    e, n = public_key
    if not (0 < message < n):
        raise ValueError(f"Message must be an integer in (0, n). Got {message}.")
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    """
    Decrypt a ciphertext integer using the private key.

    Parameters:
        ciphertext  : int      -- output of encrypt()
        private_key : (d, n)  -- from generate_keypair()

    Returns:
        message : int -- the original integer passed to encrypt()

    Formula: message = ciphertext^d mod n
    Time complexity: O(log d * log^2 n) via fast modular exponentiation.
    """
    d, n = private_key
    return pow(ciphertext, d, n)


# Demo

if __name__ == "__main__":
    import time

    print("Generating 512-bit RSA key pair...")
    start = time.perf_counter()
    pub, priv = generate_keypair(bits=512)
    elapsed = time.perf_counter() - start
    print(f"  Done in {elapsed:.3f}s")
    print(f"  Public key  (e, n): e={pub[0]}, n={str(pub[1])[:40]}...  ({pub[1].bit_length()} bits)")
    print(f"  Private key (d, n): d={str(priv[0])[:40]}...")

    print("\nEncrypt / decrypt demo:")
    message = 42
    ciphertext = encrypt(message, pub)
    recovered  = decrypt(ciphertext, priv)
    print(f"  Original  : {message}")
    print(f"  Encrypted : {str(ciphertext)[:60]}...")
    print(f"  Decrypted : {recovered}")
    print(f"  Match      : {message == recovered}")

    print("\nGenerating 1024-bit RSA key pair (slower)...")
    start = time.perf_counter()
    pub1024, priv1024 = generate_keypair(bits=1024)
    elapsed = time.perf_counter() - start
    print(f"  Done in {elapsed:.3f}s")
    ciphertext = encrypt(message, pub1024)
    recovered  = decrypt(ciphertext, priv1024)
    print(f"  Match      : {message == recovered}")