import threading
import time
import psutil
import pytest
from backend.run_backend import wordlist_crack, hash_string
import statistics


# Functionality test for wordlist function
@pytest.mark.parametrize("hash_type,input_str", [
    ("MD5", "test"),
    ("SHA-1", "test"),
    ("SHA-256", "test"),
    ("SHA-512", "test"),
    ("Ascon-Hash256", "test"),
    ("Ascon-XOF128", "test"),
    ("Ascon-CXOF128", "test"),
    ("NTLM", "test"),
    ("LM", "test"),
    ("SHA-224", "test"),
    ("SHA-384", "test"),
    ("BLAKE2b", "test"),
    ("BLAKE2s", "test"),
    ("SHA3-256", "test"),
    ("SHA3-512", "test"),
])
def test_wordlist_crack_with_supported_hashes(tmp_path, hash_type, input_str):
    # Create a temporary wordlist file with some sample words
    wordlist = tmp_path / "wordlist.txt"
    sample_words = ["password", "123456", input_str]
    wordlist.write_text("\n".join(sample_words) + "\n")

    # Generate the hash of the target input using the given hash type
    expected_hash = hash_string(hash_type, input_str, hash_length=32)

    # Attempt to crack the hash using the wordlist
    result, elapsed, guesses = wordlist_crack(expected_hash, hash_type, str(wordlist), timeout=10)

    # Verify the result matches the input string
    assert result == input_str
    # Verify the number of guesses equals the number of words in the list
    assert guesses == len(sample_words)
    # Check that elapsed time is non-negative
    assert elapsed >= 0


# Test case where the wordlist does not contain a matching word
def test_wordlist_crack_no_match(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("password\n123456\nletmein\n")

    target_hash = "nonexistent_hash"
    result, elapsed, guesses = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=10)

    assert result is None  # Should return None if not found
    assert guesses == 3  # All three words were tried
    assert elapsed >= 0


# Test case with an empty wordlist
def test_wordlist_crack_empty_wordlist(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("")  # No content

    target_hash = "0d107d09f5bbe40cade3de5c71e9e9b7"  # MD5 of "test"
    result, elapsed, guesses = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=10)

    assert result is None  # No words to try
    assert guesses == 0
    assert elapsed >= 0


# Test case to ensure timeout is respected
def test_wordlist_crack_timeout(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("password\n123456\nletmein\n")

    target_hash = "0d107d09f5bbe40cade3de5c71e9e9b7"  # MD5 of "test"
    result, elapsed, guesses = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=0.0001)

    # Result should be None due to early timeout
    assert result is None
    # Guesses may be 0 or 1 depending on how quickly the timeout occurs
    assert guesses <= 1
    assert elapsed >= 0


# performance test for wordlist function, test data can be edited
@pytest.mark.parametrize("hash_type, target_word, wordlist_size", [
    ("MD5", "99999", 10 ** 5),
    ("SHA-1", "99999", 10 ** 5),
    ("SHA-256", "99999", 10 ** 5),
    ("SHA-512", "99999", 10 ** 5),
    ("Ascon-Hash256", "99999", 10 ** 5),
    ("Ascon-XOF128", "99999", 10 ** 5),
    ("Ascon-CXOF128", "99999", 10 ** 5),
    ("NTLM", "99999", 10 ** 5),
    ("LM", "99999", 10 ** 5),
    ("SHA-224", "99999", 10 ** 5),
    ("SHA-384", "99999", 10 ** 5),
    ("BLAKE2b", "99999", 10 ** 5),
    ("BLAKE2s", "99999", 10 ** 5),
    ("SHA3-256", "99999", 10 ** 5),
    ("SHA3-512", "99999", 10 ** 5),
])
def test_wordlist_crack_performance(tmp_path, hash_type, target_word, wordlist_size):
    # Create the large wordlist once
    wordlist = tmp_path / "large_wordlist.txt"
    wordlist.write_text("\n".join(map(str, range(wordlist_size))) + "\n")
    target_hash = hash_string(hash_type, target_word, hash_length=32)
    process = psutil.Process()

    hps_list = []
    mem_list = []
    cpu_list = []
    time_list = []

    for _ in range(10): # repeats 10 times
        memory_samples = []
        cpu_samples = []
        stop_event = threading.Event()

        def monitor_performance():
            while not stop_event.is_set():
                memory_samples.append(process.memory_info().rss / (1024 * 1024))  # MB
                cpu_samples.append(process.cpu_percent(interval=None))
                time.sleep(0.05)

        process.cpu_percent(interval=None)
        monitor_thread = threading.Thread(target=monitor_performance)
        monitor_thread.start()

        start = time.perf_counter()
        result = wordlist_crack(target_hash, hash_type, str(wordlist), timeout=60)
        end = time.perf_counter()

        stop_event.set()
        monitor_thread.join()

        elapsed_time = end - start
        total_attempts = result[2]
        hashes_per_second = total_attempts / elapsed_time if elapsed_time > 0 else 0

        average_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
        average_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

        assert result[0] == target_word
        assert total_attempts <= wordlist_size

        hps_list.append(hashes_per_second)
        mem_list.append(average_memory)
        cpu_list.append(average_cpu)
        time_list.append(elapsed_time)

    # Print final averaged stats
    print(f"{hash_type:<15}: "
          f"{statistics.mean(hps_list):,.2f} H/s | "
          f"Avg CPU: {statistics.mean(cpu_list):.2f}% | "
          f"Avg Mem: {statistics.mean(mem_list):.5f} MB | "
          f"Avg Time: {statistics.mean(time_list):.5f}s")
