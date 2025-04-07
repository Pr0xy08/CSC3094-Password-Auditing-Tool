import customtkinter as ctk


class Help(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=600)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Main Heading
        title_label = ctk.CTkLabel(scrollable_frame, text="Help", font=("Arial", 26, "bold"))
        title_label.pack(pady=(10, 5), anchor="center")

        # Intro paragraph
        description = ctk.CTkLabel(scrollable_frame, text="Welcome to the Help Page", font=("Arial", 16))
        description.pack(pady=(0, 20), anchor="center")

        # Section data - list of (title, content)
        sections = [
            ("Section 1: Overview",
             "This section acts as a short overview of what this tool is and its intentions. "
             "This tool is a password auditing tool made in Python that supports the use of various password hashes, with ASCON being one of them. "
             "Additionally, the tool makes use of post-audit visualizations to provide a higher level of information compared to similar systems. "
             "This tool is the result of research conducted during my dissertation and is intended for educational use only."),
            ("Section 2: Getting Started",
             "This section will guide you through using the program, starting with navigating to the 'Run' page. Here, you can choose between a wordlist-based or brute-force audit, with the wordlist option recommended. "
             "Next, you'll be prompted to input the target hash or hashes (in a .txt file, one hash per line, allowing for multiple hashes to be uploaded simultaneously). "
             "You will also select the hash type you believe the target hash to be. If you're using a wordlist, choose the list to compare against the target hash. "
             "Additionally, you can set a timer (default is 5 seconds) to ensure the program doesn’t run longer than necessary if a hash is not found. "
             "Once you're ready, click the 'Run' button, wait for the process to complete, and you'll be redirected to the results page to view the audit outcomes."),
            ("Section 3: Relevant Resources",
             "These are resources utilized throughout the development of the tool and may also be helpful for understanding its usage:\n\n"
             "- GitHub Repository for the Tool: https://github.com/Pr0xy08/CSC3094-Password-Auditing-Tool\n"
             "- Rockyou.txt Wordlist: https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt\n"
             "- Crackstation Wordlist: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm\n"
             "- Understanding Password Quality Index (PQI): https://core.ac.uk/download/286877142.pdf\n"
             "- Understanding Zxcvbn: https://dropbox.tech/security/zxcvbn-realistic-password-strength-estimation\n"
             "- Hash Identifier Tool: https://www.kali.org/tools/hash-identifier/"),
            ("Section 4: Troubleshooting",
             "Here are some common problems and solutions:\n\n"
             "- Struggling to find a password list? Refer to the 'Relevant Resources' section, with a personal recommendation for Rockyou.txt.\n"
             "- TXT file input read errors? Ensure the hashes are correctly formatted with each hash on a separate line, and no additional content in the file.\n"
             "- Don’t know the hash type? Use a tool like Hash Identifier (see 'Relevant Resources' section).")
        ]

        # Render each section
        for title, content in sections:
            section_title = ctk.CTkLabel(scrollable_frame, text=title, font=("Arial", 18, "bold"))
            section_title.pack(anchor="w", padx=20, pady=(10, 4))

            section_content = ctk.CTkLabel(scrollable_frame, text=content, font=("Arial", 14), wraplength=760, justify="left")
            section_content.pack(anchor="w", padx=30, pady=(0, 10))
