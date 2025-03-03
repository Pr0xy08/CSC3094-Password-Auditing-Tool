import hashlib


# Read the password from test.txt
with open("test.txt") as f:
    password = f.read().strip()  # Strip newline characters

# Open and read wordlist.txt
found = False
with open("wordlist.txt") as t:
    for line in t:
        if hashlib.md5(line.strip().encode()).hexdigest() == password:  # hashed password with current line
            print("Success! Password is:", line)
            found = True
            break  # Stop after finding the password

if not found:
    print("Fail, no password found")
