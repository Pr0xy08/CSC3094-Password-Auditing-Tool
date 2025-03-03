import customtkinter as ctk
from backend.run_backend import upload_file, run_cracker


class Run(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Store paths of target hash and wordlist
        self.target_hash_path = None
        self.wordlist_path = None

        # Title
        label = ctk.CTkLabel(self, text="Run", font=("Arial", 24))
        label.pack(pady=20)

        # Input to choose cracking mode
        self.select_mode = ctk.CTkComboBox(
            self, values=["Brute Force", "Wordlist"]
        )
        self.select_mode.pack(padx=20, pady=10)
        self.select_mode.set("Wordlist")  # Set initial value

        # Input to choose hash type
        self.select_hash_type = ctk.CTkComboBox(
            self,
            values=["MD5", "SHA-1", "SHA-256", "SHA-512"],
        )
        self.select_hash_type.pack(padx=20, pady=10)
        self.select_hash_type.set("MD5")

        # Input to upload a txt file containing the target hash
        self.upload_target_hash = ctk.CTkButton(
            self, text="Upload target hash (txt file)", fg_color="blue",
            command=self.upload_target # runs upload_target function
        )
        self.upload_target_hash.pack(padx=25, pady=25)

        # Input to upload a txt file containing a wordlist
        self.upload_wordlist = ctk.CTkButton(
            self, text="Upload wordlist (txt file)", fg_color="blue",
            command=self.upload_wordlist_file # runs upload_wordlist function
        )
        self.upload_wordlist.pack(padx=25, pady=25)

        # Button to run cracking function with selected inputs
        self.run_button = ctk.CTkButton(
            self, text="Run", fg_color="Red", command=self.run_crack # runs run_crack function
        )
        self.run_button.pack(padx=25, pady=25)

        # Output Label
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 16)) # outputs depending upon inputs made
        self.output_label.pack(pady=10)

    def upload_target(self):
        self.target_hash_path = upload_file()
        if self.target_hash_path:
            self.upload_target_hash.configure(text="Target Hash Uploaded")

    def upload_wordlist_file(self):
        self.wordlist_path = upload_file()
        if self.wordlist_path:
            self.upload_wordlist.configure(text="Wordlist Uploaded")

    def run_crack(self):
        mode = self.select_mode.get() # gets mode selected
        hash_type = self.select_hash_type.get() # gets hash type selected

        if not self.target_hash_path: # presence check for target hash
            self.output_label.configure(text="Please upload a target hash file.")
            return

        if mode == "Wordlist" and not self.wordlist_path: # presence check for wordlist
            self.output_label.configure(text="Please upload a wordlist file.")
            return

        result = run_cracker(mode, hash_type, self.target_hash_path, self.wordlist_path) # runs with selected mode, hash type, target hash and wordlist
        self.output_label.configure(text=f"Result: {result}") # The result of run_cracker function is output
