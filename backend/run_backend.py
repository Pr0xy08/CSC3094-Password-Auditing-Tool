import hashlib
import itertools
import os
import multiprocessing
import time
from tkinter import filedialog
from ASCON.ascon import ascon_hash
from passlib.hash import lmhash


def hash_string(hash_type, string, hash_length=32): # hashes string but chosen hash type
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


def brute_force_crack(target_hash, hash_type, max_length=6, timeout=30): # brute force function
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
                    return None
    return None


def wordlist_crack(target_hash, hash_type, wordlist_path): # wordlist function
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            word = line.strip()
            if hash_string(hash_type, word, len(target_hash)) == target_hash:
                return word
    return None


def upload_file(): # function used to upload wordlist and target hash file
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])


def run_cracker(mode, algorithm, target_hash_path, wordlist_path=None):
    if not os.path.exists(target_hash_path):
        return {"error": "Target hash file not found!"}

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hashes = [line.strip() for line in file if line.strip()]

    if not target_hashes:
        return {"error": "No hashes found in the file!"}

    results = {}
    for target_hash in target_hashes:
        if mode == "Brute Force":
            result = brute_force_crack(target_hash, algorithm)
        elif mode == "Wordlist":
            if not wordlist_path or not os.path.exists(wordlist_path):
                results[target_hash] = "Error: Wordlist file not found!"
                continue
            result = wordlist_crack(target_hash, algorithm, wordlist_path)
        else:
            results[target_hash] = "Error: Invalid mode!"
            continue

        results[target_hash] = result if result else "Password not found."

    return results # return dictionary of hash value and associated plaintext
