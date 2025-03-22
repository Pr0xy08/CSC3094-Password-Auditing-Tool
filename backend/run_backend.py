import hashlib
import itertools
import os
import multiprocessing
import time
import asyncio
import queue
from tkinter import filedialog
from ASCON.ascon import ascon_hash


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
    else:
        raise ValueError("Unsupported hash type")


def brute_force_worker(args):
    target_hash, hash_type, attempt = args
    attempt_str = ''.join(attempt)
    if hash_string(hash_type, attempt_str, len(target_hash)) == target_hash:
        return attempt_str
    return None


def brute_force_crack(target_hash, hash_type, max_length=6, timeout=600):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for length in range(1, max_length + 1):
            attempts = itertools.product(chars, repeat=length)
            args = ((target_hash, hash_type, attempt) for attempt in attempts)
            for result in pool.imap_unordered(brute_force_worker, args, chunksize=1000):
                if result is not None:
                    return result
                if time.time() - start_time > timeout:
                    return "Password not found (timed out)."
    return "Password not found."


def wordlist_crack(target_hash, hash_type, wordlist_path):
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            word = line.strip()
            if hash_string(hash_type, word, len(target_hash)) == target_hash:
                return word
    return None


def upload_file():
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])


def run_cracker(mode, algorithm, target_hash_path, wordlist_path=None):
    if not os.path.exists(target_hash_path):
        return "Error: Target hash file not found!"

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hashes = [line.strip() for line in file if line.strip()]

    if not target_hashes:
        return "Error: No hashes found in the file!"

    results = {}
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

    return "\n".join([f"{h} -> {p}" for h, p in results.items()])
