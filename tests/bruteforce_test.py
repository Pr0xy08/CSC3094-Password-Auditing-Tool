import threading
import time
import psutil
import pytest
from backend.run_backend import brute_force_crack, hash_string


# Unit tests for the brute_force_crack function

@pytest.mark.parametrize("hash_type,input_str,max_length", [ # benchmark inputs
    ("MD5", "ab", 2),
    ("SHA-1", "ab", 2),
    ("SHA-256", "ab", 2),
    ("SHA-512", "ab", 2),
    ("Ascon-Hash256", "ab", 2),
    ("Ascon-XOF128", "ab", 2),
    ("Ascon-CXOF128", "ab", 2),
    ("NTLM", "ab", 2),
    ("LM", "ab", 2),
])
def test_brute_force_crack_known_values(hash_type, input_str, max_length):
    target_hash = hash_string(hash_type, input_str, hash_length=32)
    result, elapsed, guesses = brute_force_crack(target_hash, hash_type, max_length=max_length, timeout=60)

    assert hash_string(hash_type, result, hash_length=32) == target_hash
    assert guesses > 0 # guesses should be more than 0
    assert elapsed > 0 # time should be more than 0


def test_brute_force_crack_no_match(): # unable to find a match in all 2 character strings
    target_hash = hash_string("MD5", "nonexistent", 32) # change the hash type here if necessary
    result, elapsed, guesses = brute_force_crack(target_hash, "MD5", max_length=2, timeout=5)

    assert result is None # result should be none a nonexistent is of length > max_len of 2
    assert guesses > 0
    assert elapsed > 0


def test_brute_force_crack_timeout(): # should time out before a match is found
    target_hash = hash_string("MD5", "zzzzzz", 32)  # change hash type here if necessary
    result, elapsed, guesses = brute_force_crack(target_hash, "MD5", max_length=6, timeout=0.001)

    assert result is None
    assert elapsed <= 1  # should time out quickly
    assert guesses >= 0


@pytest.mark.parametrize("hash_type,target_word,max_length", [
    ("MD5", "abcd", 4),
    ("SHA-1", "abcd", 4),
    ("SHA-256", "abcd", 4),
    ("SHA-512", "abcd", 4),
    ("Ascon-Hash256", "abcd", 4),
    ("Ascon-XOF128", "abcd", 4),
    ("Ascon-CXOF128", "abcd", 4),
    ("NTLM", "abcd", 4),
    ("LM", "abcd", 4),
])
def test_brute_force_crack_performance(hash_type, target_word, max_length):
    target_hash = hash_string(hash_type, target_word, hash_length=32)
    process = psutil.Process()
    memory_samples = []
    cpu_samples = []

    stop_event = threading.Event()

    def monitor_performance():
        while not stop_event.is_set():
            memory_samples.append(process.memory_info().rss / (1024 * 1024))  # MB
            cpu_samples.append(process.cpu_percent(interval=None))
            time.sleep(0.05)

    process.cpu_percent(interval=None)  # Initialize CPU percent
    monitor_thread = threading.Thread(target=monitor_performance)
    monitor_thread.start()

    start_time = time.perf_counter()
    result, elapsed, guesses = brute_force_crack(target_hash, hash_type, max_length=max_length, timeout=60)
    end_time = time.perf_counter()

    stop_event.set()
    monitor_thread.join()

    elapsed_time = end_time - start_time
    hashes_per_second = guesses / elapsed_time if elapsed_time > 0 else 0
    average_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    average_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    assert hash_string(hash_type, result, hash_length=32) == target_hash
    assert guesses > 0

    print(f"{hash_type:<15}: {hashes_per_second:,.2f} H/s | "
          f"Average CPU: {average_cpu:.2f}% | "
          f"Average Mem: {average_memory:.5f} MB | "
          f"Total Time: {elapsed_time:.5f}s")
