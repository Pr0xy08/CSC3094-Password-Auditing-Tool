import hashlib
import itertools
import os
from tkinter import filedialog


def hash_string(hash_type, string): # hashes string with specific type chosen
    if hash_type == "MD5":
        return hashlib.md5(string.encode()).hexdigest() # hashes string with MD5 if MD5 is chosen
    elif hash_type == "SHA-1":
        return hashlib.sha1(string.encode()).hexdigest() # hashes string with SHA1 if SHA1 is chosen
    elif hash_type == "SHA-256":
        return hashlib.sha256(string.encode()).hexdigest() # hashes string with SHA256 if SHA256 is chosen
    elif hash_type == "SHA-512":
        return hashlib.sha512(string.encode()).hexdigest() # hashes string with SHA512 if SHA512 is chosen
    # Add more hash functions as needed
    else:
        raise ValueError("Unsupported hash type")


def brute_force_crack(target_hash, hash_type, max_length=6):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for length in range(1, max_length + 1):
        for attempt in itertools.product(chars, repeat=length):
            attempt = ''.join(attempt)
            if hash_string(hash_type, attempt) == target_hash:
                return attempt
    return None


def wordlist_crack(target_hash, hash_type, wordlist_path): # takes target hash, hash_type and wordlist
    with open(wordlist_path, 'r', encoding='utf-8') as file: # open wordlist
        for line in file: # for each word
            word = line.strip()
            if hash_string(hash_type, word) == target_hash: # hash the word and compare it to target hash
                return word # If the word is the target hash then return the word
    return None # if not found return None


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path if file_path else None


def run_cracker(mode, algorithm, target_hash_path, wordlist_path=None):
    if not os.path.exists(target_hash_path):
        return "Target hash file not found!"

    with open(target_hash_path, 'r', encoding='utf-8') as file:
        target_hash = file.readline().strip()

    if mode == "Brute Force":
        result = brute_force_crack(target_hash, algorithm)
    elif mode == "Wordlist":
        if not wordlist_path or not os.path.exists(wordlist_path):
            return "Wordlist file not found!"
        result = wordlist_crack(target_hash, algorithm, wordlist_path)
    else:
        return "Invalid mode!"

    return result if result else "Password not found."


