import threading
import time
import psutil
import pytest
from backend.run_backend import wordlist_crack, hash_string


# Unit tests to test if wordlist_crack functionally works as intended
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
])
def test_wordlist_crack_with_supported_hashes(tmp_path, hash_type, input_str):
    wordlist = tmp_path / "wordlist.txt"
    sample_words = ["password", "123456", input_str]
    wordlist.write_text("\n".join(sample_words) + "\n")

    expected_hash = hash_string(hash_type, input_str, hash_length=32)
    result = wordlist_crack(expected_hash, hash_type, str(wordlist), timeout=10)

    assert result[0] == input_str
    assert result[2] == len(sample_words)
    assert result[1] >= 0


def test_wordlist_crack_no_match(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("password\n123456\nletmein\n")

    target_hash = "nonexistent_hash"
    result = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=10)

    assert result[0] is None
    assert result[2] == 3
    assert result[1] >= 0


def test_wordlist_crack_empty_wordlist(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("")

    target_hash = "0d107d09f5bbe40cade3de5c71e9e9b7"
    result = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=10)

    assert result[0] is None
    assert result[2] == 0
    assert result[1] >= 0


def test_wordlist_crack_timeout(tmp_path):
    wordlist = tmp_path / "wordlist.txt"
    wordlist.write_text("password\n123456\nletmein\n")

    target_hash = "0d107d09f5bbe40cade3de5c71e9e9b7"
    result = wordlist_crack(target_hash, "MD5", str(wordlist), timeout=0.0001)

    assert result[0] is None
    assert result[2] <= 1
    assert result[1] >= 0


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
])
def test_wordlist_crack_performance_precise(tmp_path, hash_type, target_word, wordlist_size):
    wordlist = tmp_path / "large_wordlist.txt"
    wordlist.write_text("\n".join(map(str, range(wordlist_size))) + "\n")
    target_hash = hash_string(hash_type, target_word, hash_length=32)

    process = psutil.Process()
    memory_samples = []
    cpu_samples = []

    def monitor_performance():
        while not stop_event.is_set():
            memory_samples.append(process.memory_info().rss / (1024 * 1024))
            cpu_samples.append(process.cpu_percent(interval=None))
            time.sleep(0.05)

    stop_event = threading.Event()
    monitor_thread = threading.Thread(target=monitor_performance)

    process.cpu_percent(interval=None)
    monitor_thread.start()

    start = time.perf_counter()
    result = wordlist_crack(target_hash, hash_type, str(wordlist), timeout=60)
    end = time.perf_counter()

    stop_event.set()
    monitor_thread.join()

    elapsed_time = end - start
    total_attempts = result[2]
    hash_rate = total_attempts / elapsed_time if elapsed_time > 0 else 0

    average_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    average_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    assert result[0] == target_word
    assert total_attempts <= wordlist_size

    print(f"\n[{hash_type} Performance]| "
          f"Total Guesses: {total_attempts}| "
          f"Hash Rate: {hash_rate:,.2f} H/s| "
          f"Average CPU: {average_cpu:.2f}%| "
          f"Average Mem: {average_memory:.5f} MB| "
          f"Total Time: {elapsed_time:.5f}s|")
