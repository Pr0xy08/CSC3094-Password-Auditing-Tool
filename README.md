# Password Auditing Tool with ASCON Integration

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [License](#license)
- [Credits](#credits)

---

## Overview

This is an interactive **GUI-based password auditing tool** designed to analyse password strength, patterns, and vulnerabilities. It leverages various **visualisations and statistics**, and supports a broad range of **hashing algorithms**, including:

- MD5, SHA Family (SHA1, SHA256, SHA512), NTLM, LM  
- BLAKE2b, BLAKE2s, SHA3 Family  
- **ASCON** (lightweight cryptography finalist)

---

## Features

### Visual Analytics
The tool visualises multiple password strength metrics, such as:
- Password Quality Index  
- Password Length Distribution  
- Success Rate  
- Character Frequency  
- Zxcvbn Password Score

### ASCON Support
A key differentiator is support for the **ASCON** hashing algorithm — implemented using the official implementation (`ascon.py`). While fully functional, its performance is not on par with other algorithms, making it a key focus area in future improvements.

---

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Pr0xy08/CSC3094-Password-Auditing-Tool.git
2. Navigate to project dir:
   ```bash
   cd CSC3094-Password-Auditing-Tool
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
---
## Usage Guide

1. Launch the app. You'll land on the **Run** page (`run.py`).
2. Select a hashing mode.  
   - *Wordlist mode (default)* is recommended for speed.
3. Choose a hash type.  
   - If unsure, tools like [Hash-Identifier](https://www.kali.org/tools/hash-identifier/) may help.
4. Set a timeout.  
   - This limits how long to audit each hash. E.g., `5s per hash` means 5 hashes = 25s max.
5. Upload a `.txt` file with target hashes.  
   - One hash per line, no other data.
6. If using Wordlist mode, upload a wordlist file.  
   - examples like `rockyou.txt` work well (used in the evaluation report).
7. Click **Run**, then wait for results and visual analytics to load.

---

## License

MIT License

Copyright (c) 2025 Drew Wandless

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Credits

Created by **Drew Wandless** as part of the CSC3094 coursework at **Newcastle University**.

Special thanks to:

- **Carlton Shepherd** (Supervisor)  
- **Newcastle University** for academic support and resources