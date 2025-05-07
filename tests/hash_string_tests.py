import threading
from functools import partial
import time
import psutil
import pytest
from backend.run_backend import hash_string


# Functionality test for hash_string function, works as intended
@pytest.mark.parametrize("hash_type,input_str,expected", [
    ("MD5", "test", "098f6bcd4621d373cade4e832627b4f6"),
    ("SHA-1", "test", "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"),
    ("SHA-256", "test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"),
    ("SHA-512", "test",
     "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff"),
    ("Ascon-Hash256", "test", "3b19624921eb1d6751215350f5fa6db45ca83a3b03555651353fd63d8d0b2b7b"),
    ("Ascon-XOF128", "test", "85130352d6c207646d091b46d2bb0df6fe2189a7be71ac5826a4ce62e8262e8e"),
    ("Ascon-CXOF128", "test", "8a054af4c5f8b03e2085c68595da50f95516717ba787e5b217455d1608a5fe25"),
    ("NTLM", "test", "0CB6948805F797BF2A82807973B89537"),
    ("LM", "test", "01FC5A6BE7BC6929AAD3B435B51404EE"),
    ("SHA-224", "test", "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"),
    ("SHA-384", "test",
     "768412320f7b0aa5812fce428dc4706b3cae50e02a64caa16a782249bfe8efc4b7ef1ccb126255d196047dfedf17a0a9"),
    ("BLAKE2b", "test",
     "a71079d42853dea26e453004338670a53814b78137ffbed07603a41d76a483aa9bc33b582f77d30a65e6f29a896c0411f38312e1d66e0bf16386c86a89bea572"),
    ("BLAKE2s", "test", "f308fc02ce9172ad02a7d75800ecfc027109bc67987ea32aba9b8dcc7b10150e"),
    ("SHA3-256", "test", "36f028580bb02cc8272a9a020f4200e346e276ae664e45ee80745574e2f5ab80"),
    ("SHA3-512", "test",
     "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"),
])
def test_known_hashes(hash_type, input_str, expected):
    # Ensure the generated hash matches the expected result
    assert hash_string(hash_type, input_str, hash_length=len(expected)) == expected


# Performance test for hash_string algorithms
def test_hash_string_performance():
    # Hash types to benchmark
    hash_types = [
        "MD5", "SHA-1", "SHA-256", "SHA-512",
        "Ascon-Hash256", "Ascon-XOF128", "Ascon-CXOF128",
        "NTLM", "LM", "SHA-224", "SHA-384", "BLAKE2b", "BLAKE2s", "SHA3-256", "SHA3-512"
    ]
    # Consistent input string for benchmarking
    input_str = "The quick brown fox jumps over the lazy dog"
    hash_length = 32
    iterations = 1000  # Number of times to run hashing

    # Get the current process for resource monitoring
    process = psutil.Process()
    print("\n[Hash String Performance Report]")

    # Loop through each hash type and measure performance
    for hash_type in hash_types:
        stmt = partial(hash_string, hash_type, input_str, hash_length)

        memory_samples = []
        cpu_samples = []
        stop_event = threading.Event()

        # Background thread to monitor memory and CPU usage periodically
        def monitor_performance():
            while not stop_event.is_set():
                memory_samples.append(process.memory_info().rss / (1024 * 1024))  # Memory in MB
                cpu_samples.append(process.cpu_percent(interval=None))
                time.sleep(0.05)

        # Prime the CPU usage counter
        process.cpu_percent(interval=None)
        monitor_thread = threading.Thread(target=monitor_performance)
        monitor_thread.start()

        # Time how long it takes to perform a large number of hash operations
        start = time.perf_counter()
        for _ in range(iterations):
            stmt()
        end = time.perf_counter()

        # Stop monitoring thread and calculate results
        stop_event.set()
        monitor_thread.join()

        elapsed_time = end - start
        hashes_per_second = iterations / elapsed_time
        average_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
        average_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

        # Print performance metrics for each hash algorithm
        print(f"{hash_type:<15}: {hashes_per_second:,.2f} H/s | "
              f"Average CPU: {average_cpu:.2f}% | "
              f"Average Mem: {average_memory:.5f} MB | "
              f"Total Time: {elapsed_time:.5f}s")
