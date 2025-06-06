import hashlib
import itertools
import os
import multiprocessing
import time
import psutil
from tkinter import filedialog
from ASCON.ascon import ascon_hash
from passlib.hash import lmhash, nthash


# TODO: make performance of both functions better (Implement GPU acceleration and look into ASCON implementation methods)

def hash_string(hash_type, string, # takes a string and hashes it to the given hash type and hash length
                hash_length):
    if hash_type == "MD5":
        return hashlib.md5(string.encode()).hexdigest()  # hash to md5
    elif hash_type == "SHA-1":
        return hashlib.sha1(string.encode()).hexdigest()  # hash to sha1
    elif hash_type == "SHA-224":
        return hashlib.sha224(string.encode()).hexdigest()  # newly added - hash to sha224
    elif hash_type == "SHA-256":
        return hashlib.sha256(string.encode()).hexdigest()  # hash to sha256
    elif hash_type == "SHA-384":
        return hashlib.sha384(string.encode()).hexdigest()  # hash to sha-384
    elif hash_type == "SHA-512":
        return hashlib.sha512(string.encode()).hexdigest()  # hash to sha512
    elif hash_type == "Ascon-Hash256":
        return ascon_hash(message=string.encode(), variant="Ascon-Hash256",
                          hashlength=32).hex()  # ascon hash 256
    elif hash_type == "Ascon-XOF128":
        return ascon_hash(message=string.encode(), variant="Ascon-XOF128",
                          hashlength=hash_length // 2).hex()  # hash to ascon xof128
    elif hash_type == "Ascon-CXOF128":
        return ascon_hash(message=string.encode(), variant="Ascon-CXOF128",
                          hashlength=hash_length // 2).hex()  # hash to ascon cxof128
    elif hash_type == "NTLM":
        return nthash.hash(string).upper() # hash to ntlm
    elif hash_type == "LM":
        return lmhash.hash(string).upper()  # hash to lm
    elif hash_type == "BLAKE2b":
        return hashlib.blake2b(string.encode()).hexdigest() # hash to BLAKE2b
    elif hash_type == "BLAKE2s":
        return hashlib.blake2s(string.encode()).hexdigest()  # hash to BLAKE2s
    elif hash_type == "SHA3-256":
        return hashlib.sha3_256(string.encode()).hexdigest() # hash to SHA3-256
    elif hash_type == "SHA3-512":
        return hashlib.sha3_512(string.encode()).hexdigest() # hash to SHA3-512
    else:
        raise ValueError("Unsupported hash type")


def brute_force_worker(queue, result, stop_event, target_hash, hash_type, hash_length, guess_counter):
    while not stop_event.is_set():
        try:
            attempt = queue.get(timeout=1)
        except:
            continue

        attempt_str = ''.join(attempt)
        guess_counter.value += 1  # Increment shared counter

        if hash_string(hash_type, attempt_str, hash_length) == target_hash:
            result["password"] = attempt_str
            result["found"] = True
            stop_event.set()
            break


def generate_attempts(queue, chars, max_length, stop_event):
    try:
        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                if stop_event.is_set():
                    return
                queue.put(attempt)
    except:
        pass


def brute_force_crack(target_hash, hash_type, max_length=6, timeout=None): # brute force audit function
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_time = time.perf_counter() # begin timer

    manager = multiprocessing.Manager() # multi processing
    result = manager.dict()
    result["password"] = None
    result["found"] = False

    guess_counter = multiprocessing.Value('i', 0)  # Shared counter

    queue = multiprocessing.Queue(maxsize=10000)
    stop_event = multiprocessing.Event()

    producer = multiprocessing.Process(target=generate_attempts, args=(queue, chars, max_length, stop_event))
    producer.start()

    workers = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(
            target=brute_force_worker,
            args=(queue, result, stop_event, target_hash, hash_type, len(target_hash), guess_counter)
        )
        p.start()
        workers.append(p)

    try:
        while True:
            if result["found"]:
                break
            if timeout and (time.perf_counter() - start_time > timeout):
                break
            time.sleep(0.001)
    finally:
        stop_event.set()
        producer.terminate()
        producer.join()
        for p in workers:
            p.terminate()
            p.join()

    elapsed = time.perf_counter() - start_time
    return result["password"], elapsed, guess_counter.value # return results


def wordlist_crack(target_hash, hash_type, wordlist_path, timeout=None): # function for wordlist audit
    start_time = time.perf_counter() # begin counter
    timeout_threshold = start_time + timeout if timeout else None
    guesses = 0
    target_len = len(target_hash)

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file: # opens wordlist
        for line in file:
            word = line.rstrip('\n')
            guesses += 1 # strips each and appends to counter
            if hash_string(hash_type, word, target_len) == target_hash:
                elapsed = time.perf_counter() - start_time # finish if word found
                return word, elapsed, guesses
            if timeout_threshold and time.perf_counter() > timeout_threshold: # continue till timeout
                return None, time.perf_counter() - start_time, guesses

    return None, time.perf_counter() - start_time, guesses


def upload_file():
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])


def monitor_system_usage():  # function takes a reading of CPU and RAM Usage
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage  # returns both


def monitor_usage_periodically(log_file="usage_log.txt"):
    with open(log_file, 'a') as file:  # Open in append mode
        # Log an initial entry before the loop starts
        timestamp = time.time()  # take time measurement
        cpu_usage, ram_usage = monitor_system_usage()  # take cpu and memory measurement
        file.write(f"{timestamp},{cpu_usage},{ram_usage}\n")
        file.flush()  # immediately write contents

        while True:
            timestamp = time.time()  # takes time measurement
            cpu_usage, ram_usage = monitor_system_usage()  # take cpu and memory measurement
            file.write(f"{timestamp},{cpu_usage},{ram_usage}\n")
            file.flush()  # immediately write contents
            time.sleep(0.0001)  # interval between next log, still need to tweak this


def run_audit(mode, algorithm, target_hash_path, wordlist_path=None, timeout=None): # function tied to run button
    log_file = "usage_log.txt"

    # Clear or create the log file
    if os.path.exists(log_file):
        os.remove(log_file)
    with open(log_file, 'w') as file:
        file.write("")  # Start fresh

    if not os.path.exists(target_hash_path):
        return {"error": "Target hash file not found!"}

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hashes = [line.strip() for line in file if line.strip()]

    if not target_hashes:
        return {"error": "No hashes found in the file!"}

    # Start monitoring CPU and RAM usage in a separate process
    monitor_process = multiprocessing.Process(target=monitor_usage_periodically, args=(log_file,))
    monitor_process.start()

    time.sleep(3)  # Allow the monitor process to start logging before audit commences

    results = {}
    overall_start_time = time.time()  # Then begin overall timer
    total_hashes_attempts = 0

    # Run the cracker algorithm
    for target_hash in target_hashes:
        if mode == "Brute Force":
            result, elapsed, hashes_attempted = brute_force_crack(target_hash, algorithm, timeout=timeout)
        elif mode == "Wordlist":
            if not wordlist_path or not os.path.exists(wordlist_path):
                results[target_hash] = {
                    "password": "Error: Wordlist file not found!",
                    "time_taken": None
                }
                continue
            result, elapsed, hashes_attempted = wordlist_crack(target_hash, algorithm, wordlist_path, timeout=timeout)
        else:
            results[target_hash] = {
                "password": "Error: Invalid mode!",
                "time_taken": None
            }
            continue

        total_hashes_attempts += hashes_attempted
        results[target_hash] = {
            "password": result if result else "Password not found.",
            "time_taken": elapsed
        }

    # calculate overall time
    overall_finish_time = time.time()
    overall_time_taken = overall_finish_time - overall_start_time

    # Calculate average hashes per second (H/s)
    avg_hashes_per_second = total_hashes_attempts / overall_time_taken if overall_time_taken > 0 else 0

    time.sleep(1)  # Allow the monitor process to complete logging and store data to txt file

    # Stop the monitoring process
    monitor_process.terminate()
    monitor_process.join()

    # returns all results
    return {
        "results": results,
        "overall_info": {
            "mode": mode,
            "algorithm": algorithm,
            "wordlist": wordlist_path,
            "start_time": overall_start_time,
            "finish_time": overall_finish_time,
            "overall_time": overall_time_taken,
            "total_hashes_attempts": total_hashes_attempts,
            "avg_hashes_per_second": avg_hashes_per_second
        }
    }
