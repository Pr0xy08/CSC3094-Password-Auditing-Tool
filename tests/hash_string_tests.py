import timeit
from functools import partial

import pytest
from backend.run_backend import hash_string


# unit tests to test if hash_string functionally works as intended
@pytest.mark.parametrize("hash_type,input_str,expected", [
    ("MD5", "test", "098f6bcd4621d373cade4e832627b4f6"),
    ("SHA-1", "test", "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"),
    ("SHA-256", "test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"),
    ("SHA-512", "test",
     "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff"),
    ("Ascon-Hash256", "test", "3b19624921eb1d6751215350f5fa6db45ca83a3b03555651353fd63d8d0b2b7b"),  # fixed
    ("Ascon-XOF128", "test", "85130352d6c207646d091b46d2bb0df6fe2189a7be71ac5826a4ce62e8262e8e"),  # fixed
    ("Ascon-CXOF128", "test", "8a054af4c5f8b03e2085c68595da50f95516717ba787e5b217455d1608a5fe25"),  # fixed
    ("NTLM", "test", "0CB6948805F797BF2A82807973B89537"),  # fixed
    ("LM", "test", "01FC5A6BE7BC6929AAD3B435B51404EE"),
])
def test_known_hashes(hash_type, input_str,
                      expected):  # hash type, string to hash, expected results, the length of the expected hash
    assert hash_string(hash_type, input_str, hash_length=len(expected)) == expected


# Test hashes per second of each of the hashing functions
def test_hash_string_performance():
    hash_types = [
        "MD5", "SHA-1", "SHA-256", "SHA-512",
        "Ascon-Hash256", "Ascon-XOF128", "Ascon-CXOF128",
        "NTLM", "LM"
    ]
    input_str = "The quick brown fox jumps over the lazy dog"  # the test string hashed each time
    hash_length = 32  # length set to 32
    iterations = 1000

    print("\nHash Performance (Hashes per second):")
    for hash_type in hash_types:
        stmt = partial(hash_string, hash_type, input_str, hash_length)
        duration = timeit.timeit(stmt, number=iterations)
        hashes_per_second = iterations / duration
        print(f"{hash_type:<15} : {hashes_per_second:,.2f} H/s")
