import hashlib
import itertools
import os
import threading
import time
from tkinter import filedialog


# Function to hash a string with a given algorithm
def hash_string(hash_type, string):
    if hash_type == "MD5":
        return hashlib.md5(string.encode()).hexdigest()
    elif hash_type == "SHA-1":
        return hashlib.sha1(string.encode()).hexdigest()
    elif hash_type == "SHA-256":
        return hashlib.sha256(string.encode()).hexdigest()
    elif hash_type == "SHA-512":
        return hashlib.sha512(string.encode()).hexdigest()
    else:
        raise ValueError("Unsupported hash type")


# Optimized Brute Force Function with threading and limits
def brute_force_crack(target_hash, hash_type, max_length=6, timeout=30):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_time = time.time()
    found = [None]  # Use a list to store the found password (mutable for threads)

    def attempt_crack(length):
        for attempt in itertools.product(chars, repeat=length):
            if found[0]:  # If another thread found the password, exit early
                return
            attempt_str = ''.join(attempt)
            if hash_string(hash_type, attempt_str) == target_hash:
                found[0] = attempt_str
                return
            # Stop brute force if timeout is reached
            if time.time() - start_time > timeout:
                return

    threads = []
    for length in range(1, max_length + 1):
        thread = threading.Thread(target=attempt_crack, args=(length,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to complete

    return found[0] if found[0] else "Password not found (timed out or too complex)."


# Wordlist function: checks each word from the list
def wordlist_crack(target_hash, hash_type, wordlist_path):
    with open(wordlist_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if hash_string(hash_type, word) == target_hash:
                return word  # Found match
    return None  # Not found


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path if file_path else None


def run_cracker(mode, algorithm, target_hash_path, wordlist_path=None):
    if not os.path.exists(target_hash_path):
        return "Error: Target hash file not found!"

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hashes = [line.strip() for line in file if line.strip()]  # Read all hashes, ignoring empty lines

    if not target_hashes:
        return "Error: No hashes found in the file!"

    results = {}  # Store results for each hash

    for target_hash in target_hashes:
        if mode == "Brute Force":
            result = brute_force_crack(target_hash, algorithm)
        elif mode == "Wordlist":
            if not wordlist_path or not os.path.exists(wordlist_path):
                return "Error: Wordlist file not found!"
            result = wordlist_crack(target_hash, algorithm, wordlist_path)
        else:
            return "Error: Invalid mode!"

        results[target_hash] = result if result else "Password not found."

    # Format the results for display
    result_text = "\n".join([f"{h} → {p}" for h, p in results.items()])

    return result_text
