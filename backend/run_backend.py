import hashlib
import itertools
import os
import multiprocessing
import time
from tkinter import filedialog
from ASCON.ascon import ascon_hash
from passlib.hash import lmhash


def hash_string(hash_type, string, hash_length=32):
    if hash_type == "MD5":
        return hashlib.md5(string.encode()).hexdigest()
    elif hash_type == "SHA-1":
        return hashlib.sha1(string.encode()).hexdigest()
    elif hash_type == "SHA-256":
        return hashlib.sha256(string.encode()).hexdigest()
    elif hash_type == "SHA-512":
        return hashlib.sha512(string.encode()).hexdigest()
    elif hash_type == "Ascon-Hash256":
        return ascon_hash(message=string.encode(), variant="Ascon-Hash256", hashlength=32).hex()
    elif hash_type == "Ascon-XOF128":
        return ascon_hash(message=string.encode(), variant="Ascon-XOF128", hashlength=hash_length // 2).hex()
    elif hash_type == "Ascon-CXOF128":
        return ascon_hash(message=string.encode(), variant="Ascon-CXOF128", hashlength=hash_length // 2).hex()
    elif hash_type == "NTLM":
        return hashlib.new('md4', string.encode('utf-16le')).hexdigest().upper()
    elif hash_type == "LM":
        return lmhash.hash(string).upper()
    else:
        raise ValueError("Unsupported hash type")


def brute_force_worker(args):
    target_hash, hash_type, attempt = args
    attempt_str = ''.join(attempt)
    if hash_string(hash_type, attempt_str, len(target_hash)) == target_hash:
        return attempt_str
    return None


def brute_force_crack(target_hash, hash_type, max_length=6, timeout=None):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_time = time.time()
    guesses = 0
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for length in range(1, max_length + 1):
            attempts = itertools.product(chars, repeat=length)
            args = ((target_hash, hash_type, attempt) for attempt in attempts)
            for result in pool.imap_unordered(brute_force_worker, args, chunksize=1000):
                guesses += 1
                if result is not None:
                    elapsed = time.time() - start_time
                    return result, elapsed, guesses
                if time.time() - start_time > timeout:
                    return None, time.time() - start_time, guesses
    return None, time.time() - start_time, guesses


def wordlist_crack(target_hash, hash_type, wordlist_path, timeout=None):
    start_time = time.time()
    guesses = 0
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            word = line.strip()
            guesses += 1
            if hash_string(hash_type, word, len(target_hash)) == target_hash:
                elapsed = time.time() - start_time
                return word, elapsed, guesses
            if time.time() - start_time > timeout:
                return None, time.time() - start_time, guesses
    return None, time.time() - start_time, guesses


def upload_file():
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])


def run_cracker(mode, algorithm, target_hash_path, wordlist_path=None, timeout=None):
    if not os.path.exists(target_hash_path):
        return {"error": "Target hash file not found!"}

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hashes = [line.strip() for line in file if line.strip()]

    if not target_hashes:
        return {"error": "No hashes found in the file!"}

    results = {}
    start_time = time.time()
    total_hashes_attempts = 0  # Renamed to track total hash attempts

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

    finish_time = time.time()
    overall_time = finish_time - start_time

    # Calculate average hashes per second (H/s)
    if overall_time > 0:
        avg_hashes_per_second = total_hashes_attempts / overall_time
    else:
        avg_hashes_per_second = 0

    return {
        "results": results,
        "overall_info": {
            "mode": mode,
            "algorithm": algorithm,
            "wordlist": wordlist_path,
            "start_time": start_time,
            "finish_time": finish_time,
            "overall_time": overall_time,
            "total_hashes_attempts": total_hashes_attempts,  # Renamed field
            "avg_hashes_per_second": avg_hashes_per_second  # Average hashes per second
        }
    }