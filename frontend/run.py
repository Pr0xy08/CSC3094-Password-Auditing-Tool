import customtkinter as ctk
from backend.run_backend import upload_file, run_cracker


class Run(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.set_default_color_theme("green")

        # Store file paths
        self.target_hash_path = None
        self.wordlist_path = None

        # Title
        title_label = ctk.CTkLabel(self, text="Run an Audit", font=("Arial", 28, "bold"))
        title_label.pack(pady=20)

        # Frame for input selections
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Cracking Mode Selection
        ctk.CTkLabel(input_frame, text="Select Mode:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
        self.select_mode = ctk.CTkComboBox(
            input_frame, values=["Brute Force", "Wordlist"], command=self.toggle_wordlist_button
        )
        self.select_mode.pack(padx=10, pady=5, fill="x")
        self.select_mode.set("Wordlist")

        # Hash Type Selection
        ctk.CTkLabel(input_frame, text="Select Hash Type:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
        self.select_hash_type = ctk.CTkComboBox(input_frame, values=["MD5", "SHA-1", "SHA-256", "SHA-512"])
        self.select_hash_type.pack(padx=10, pady=5, fill="x")
        self.select_hash_type.set("MD5")

        # File Upload Buttons
        upload_frame = ctk.CTkFrame(self)
        upload_frame.pack(pady=15, padx=20, fill="x")

        self.upload_target_hash = ctk.CTkButton(
            upload_frame, text="Upload Target Hashes (txt file)", fg_color="#007ACC", hover_color="darkblue",
            text_color="white", command=self.upload_target
        )
        self.upload_target_hash.pack(padx=10, pady=10, fill="x")

        self.upload_wordlist = ctk.CTkButton(
            upload_frame, text="Upload Wordlist (txt file)", fg_color="#007ACC", hover_color="darkblue",
            text_color="white", command=self.upload_wordlist_file
        )
        self.upload_wordlist.pack(padx=10, pady=10, fill="x")

        # Run Button
        self.run_button = ctk.CTkButton(
            self, text="Run", text_color="white", command=self.run_crack
        )
        self.run_button.pack(padx=25, pady=25, fill="x")

        # Output Label
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.output_label.pack(pady=10)

        # Initially update wordlist button visibility
        self.toggle_wordlist_button()

    # Function to show/hide wordlist button based on selected mode
    def toggle_wordlist_button(self, *_):
        if self.select_mode.get() == "Wordlist":
            self.upload_wordlist.pack(padx=10, pady=10, fill="x")
        else:
            self.upload_wordlist.pack_forget()

    # Function ran when upload target hash button is pressed
    def upload_target(self):
        self.target_hash_path = upload_file()
        if self.target_hash_path:
            self.upload_target_hash.configure(text="Target Hash Uploaded", fg_color="green")
            self.output_label.configure(text="Target hash file uploaded successfully.", text_color="green")

    # Function ran when upload wordlist button is pressed
    def upload_wordlist_file(self):
        self.wordlist_path = upload_file()
        if self.wordlist_path:
            self.upload_wordlist.configure(text="Wordlist Uploaded", fg_color="green")
            self.output_label.configure(text="Wordlist file uploaded successfully.", text_color="green")

    # Function ran when run button is pressed
    def run_crack(self):
        mode = self.select_mode.get()
        hash_type = self.select_hash_type.get()

        if not self.target_hash_path: # if no target hash is uploaded produce error
            self.output_label.configure(text="Error: Please upload a target hash file.", text_color="red")
            return

        if mode == "Wordlist" and not self.wordlist_path: # if the mode is wordlist and there is no wordlist produce error
            self.output_label.configure(text="Error: Please upload a wordlist file.", text_color="red")
            return

        # Call the cracking function
        result = run_cracker(mode, hash_type, self.target_hash_path, self.wordlist_path)

        # Display the result
        self.output_label.configure(text=f"Result: {result}", text_color="green")

        # Reset the buttons and file paths
        self.target_hash_path = None
        self.wordlist_path = None
        self.upload_target_hash.configure(text="Upload Target Hash (txt file)", fg_color="#007ACC")
        self.upload_wordlist.configure(text="Upload Wordlist (txt file)", fg_color="#007ACC")

        # Update wordlist button visibility after reset
        self.toggle_wordlist_button()