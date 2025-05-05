#!/usr/bin/env python3

"""
Implementation of Ascon, an authenticated cipher and hash function
NIST SP 800-232
https://ascon.iaik.tugraz.at/
"""

debug = False
debugpermutation = False


# === Ascon hash/xof ===

def ascon_hash(message, variant="Ascon-Hash256", hashlength=32):
    """
        Ascon hash function and extendable-output function.
        message: a bytes object of arbitrary length
        variant: "Ascon-Hash256" (with 256-bit output for 128-bit security), "Ascon-XOF128", or "Ascon-CXOF128" (both with arbitrary output length, security=min(128, bitlen/2))
        hashlength: the requested output bytelength (must be 32 for variant "Ascon-Hash256"; can be arbitrary for Ascon-XOF128, but should be >= 32 for 128-bit security)
        customization: a bytes object of at most 256 bytes specifying the customization string (only for Ascon-CXOF128)
        returns a bytes object containing the hashtag
        """
    versions = {"Ascon-Hash256": 2,
                "Ascon-XOF128": 3,
                "Ascon-CXOF128": 4}
    assert variant in versions.keys()
    if variant == "Ascon-Hash256": assert (hashlength == 32)
    a = b = 12  # rounds
    rate = 8  # bytes
    taglen = 256 if variant == "Ascon-Hash256" else 0

    # Initialization
    iv = to_bytes([versions[variant], 0, (b << 4) + a]) + int_to_bytes(taglen, 2) + to_bytes([rate, 0, 0])
    S = bytes_to_state(iv + zero_bytes(32))
    if debug: printstate(S, "initial value:")

    ascon_permutation(S, 12)
    if debug: printstate(S, "initialization:")

    # Message Processing (Absorbing)
    m_padding = to_bytes([0x01]) + zero_bytes(rate - (len(message) % rate) - 1)
    m_padded = message + m_padding

    # message blocks 0,...,n
    for block in range(0, len(m_padded), rate):
        S[0] ^= bytes_to_int(m_padded[block:block + rate])
        ascon_permutation(S, 12)
    if debug: printstate(S, "process message:")

    # Finalization (Squeezing)
    H = b""
    while len(H) < hashlength:
        H += int_to_bytes(S[0], rate)
        ascon_permutation(S, 12)
    if debug: printstate(S, "finalization:")
    return H[:hashlength]


# === Ascon permutation ===

def ascon_permutation(S, rounds=1):
    """
    Ascon core permutation for the sponge construction - internal helper function.
    S: Ascon state, a list of 5 64-bit integers
    rounds: number of rounds to perform
    returns nothing, updates S
    """
    assert (rounds <= 12)
    if debugpermutation: printwords(S, "permutation input:")
    for r in range(12 - rounds, 12):
        # --- add round constants ---
        S[2] ^= (0xf0 - r * 0x10 + r * 0x1)
        if debugpermutation: printwords(S, "round constant addition:")
        # --- substitution layer ---
        S[0] ^= S[4]
        S[4] ^= S[3]
        S[2] ^= S[1]
        T = [(S[i] ^ 0xFFFFFFFFFFFFFFFF) & S[(i + 1) % 5] for i in range(5)]
        for i in range(5):
            S[i] ^= T[(i + 1) % 5]
        S[1] ^= S[0]
        S[0] ^= S[4]
        S[3] ^= S[2]
        S[2] ^= 0XFFFFFFFFFFFFFFFF
        if debugpermutation: printwords(S, "substitution layer:")
        # --- linear diffusion layer ---
        S[0] ^= rotr(S[0], 19) ^ rotr(S[0], 28)
        S[1] ^= rotr(S[1], 61) ^ rotr(S[1], 39)
        S[2] ^= rotr(S[2], 1) ^ rotr(S[2], 6)
        S[3] ^= rotr(S[3], 10) ^ rotr(S[3], 17)
        S[4] ^= rotr(S[4], 7) ^ rotr(S[4], 41)
        if debugpermutation: printwords(S, "linear diffusion layer:")


# === helper functions ===


def zero_bytes(n):
    return n * b"\x00"


def to_bytes(l):  # where l is a list or bytearray or bytes
    return bytes(bytearray(l))


def bytes_to_int(bytes):
    return sum([bi << (i * 8) for i, bi in enumerate(to_bytes(bytes))])


def bytes_to_state(bytes):
    return [bytes_to_int(bytes[8 * w:8 * (w + 1)]) for w in range(5)]


def int_to_bytes(integer, nbytes):
    return to_bytes([(integer >> (i * 8)) % 256 for i in range(nbytes)])


def rotr(val, r):
    return (val >> r) | ((val & (1 << r) - 1) << (64 - r))


def printstate(S, description=""):
    print(" " + description)
    print(" ".join(["{s:016x}".format(s=s) for s in S]))


def printwords(S, description=""):
    print(" " + description)
    print("\n".join(["  x{i}={s:016x}".format(**locals()) for i, s in enumerate(S)]))
