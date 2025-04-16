import threading
import time
import psutil
import pytest
from backend.run_backend import brute_force_crack, hash_string


# Test if brute-force cracking can correctly find known small strings
@pytest.mark.parametrize("hash_type,input_str,max_length", [
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
    # Hash the known input to use as the cracking target
    target_hash = hash_string(hash_type, input_str, hash_length=32)

    # Run the brute-force attack
    result, elapsed, guesses = brute_force_crack(
        target_hash, hash_type, max_length=max_length, timeout=60
    )

    # Ensure the result hashes back to the original target hash
    assert hash_string(hash_type, result, hash_length=32) == target_hash
    assert guesses > 0  # Should have made some guesses
    assert elapsed > 0  # Elapsed time should be positive


# Test when no match is possible within the max_length range
def test_brute_force_crack_no_match():
    # The string "nonexistent" can't be guessed with max_length=2
    target_hash = hash_string("MD5", "nonexistent", 32)
    result, elapsed, guesses = brute_force_crack(
        target_hash, "MD5", max_length=2, timeout=5
    )

    assert result is None  # Should return None when no match is found
    assert guesses > 0
    assert elapsed > 0


# Test that a timeout is correctly enforced and prevents full execution
def test_brute_force_crack_timeout():
    # Provide a long target string that can't be cracked in time
    target_hash = hash_string("MD5", "zzzzzz", 32)
    result, elapsed, guesses = brute_force_crack(
        target_hash, "MD5", max_length=6, timeout=0.001
    )

    assert result is None  # Should time out before finding result
    assert elapsed <= 1  # Timeout should happen fast
    assert guesses >= 0  # Might get a few guesses in


# Performance and resource usage test for brute-force cracking across multiple hash types
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
    # Prepare the hash of the known target word
    target_hash = hash_string(hash_type, target_word, hash_length=32)

    # Set up performance monitoring
    process = psutil.Process()
    memory_samples = []
    cpu_samples = []
    stop_event = threading.Event()

    # Background thread for tracking memory and CPU usage
    def monitor_performance():
        while not stop_event.is_set():
            memory_samples.append(process.memory_info().rss / (1024 * 1024))  # Convert to MB
            cpu_samples.append(process.cpu_percent(interval=None))
            time.sleep(0.05)

    # Prime CPU monitor
    process.cpu_percent(interval=None)
    monitor_thread = threading.Thread(target=monitor_performance)
    monitor_thread.start()

    # Execute the brute-force crack and time it
    start_time = time.perf_counter()
    result, elapsed, guesses = brute_force_crack(
        target_hash, hash_type, max_length=max_length, timeout=60
    )
    end_time = time.perf_counter()

    # Stop performance monitoring
    stop_event.set()
    monitor_thread.join()

    # Calculate performance metrics
    elapsed_time = end_time - start_time
    hashes_per_second = guesses / elapsed_time if elapsed_time > 0 else 0
    average_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    average_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    # Verify correct cracking
    assert hash_string(hash_type, result, hash_length=32) == target_hash
    assert guesses > 0

    # Output the performance metrics
    print(f"{hash_type:<15}: {hashes_per_second:,.2f} H/s | "
          f"Average CPU: {average_cpu:.2f}% | "
          f"Average Mem: {average_memory:.5f} MB | "
          f"Total Time: {elapsed_time:.5f}s")
