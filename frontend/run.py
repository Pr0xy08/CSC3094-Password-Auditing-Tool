import customtkinter as ctk
from backend.run_backend import upload_file, run_cracker
import threading


# TODO: Add missing input or invalid input error handling popup
# TODO: maybe add a loading bar/estimated time ect
# TODO: maybe add an attempt counter
# TODO: maybe add a way to pause or cancel the audit


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
        self.select_hash_type = ctk.CTkComboBox(
            input_frame,
            values=["MD5", "SHA-1", "SHA-256", "SHA-512", "Ascon-Hash256", "Ascon-XOF128", "Ascon-CXOF128", "NTLM",
                    "LM"]
        )
        self.select_hash_type.pack(padx=10, pady=5, fill="x")
        self.select_hash_type.set("MD5")

        # Timeout Selection
        ctk.CTkLabel(input_frame, text="Select Timeout per password (seconds):", font=("Arial", 14, "bold")).pack(
            anchor="w", padx=10)
        self.timeout_input = ctk.CTkComboBox(
            input_frame, values=["5", "10", "20", "30", "60", "120", "300"]
        )
        self.timeout_input.pack(padx=10, pady=5, fill="x")
        self.timeout_input.set("5")

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

        # Loading indicator (Initially hidden)
        self.loading_label = ctk.CTkLabel(self, text="", font=("Arial", 14), text_color="white")
        self.loading_label.pack(pady=10)
        self.loading_label.pack_forget()  # Hide it initially

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

    # Function ran when upload wordlist button is pressed
    def upload_wordlist_file(self):
        self.wordlist_path = upload_file()
        if self.wordlist_path:
            self.upload_wordlist.configure(text="Wordlist Uploaded", fg_color="green")

    # Function to run the cracking process in the background thread
    def run_crack(self):
        mode = self.select_mode.get()
        hash_type = self.select_hash_type.get()
        timeout = int(self.timeout_input.get())

        if not self.target_hash_path:  # If no target hash is uploaded, produce an error
            self.controller.show_error("Error: Please upload a target hash file.")
            return

        if mode == "Wordlist" and not self.wordlist_path:  # If mode is wordlist and no wordlist, produce error
            self.controller.show_error("Error: Please upload a wordlist file.")
            return

        # Show the loading indicator
        self.loading_label.pack(pady=10)
        self.loading_text = "Loading."  # Start with one dot

        # Start the dot animation
        self.animate_loading_dots()

        # Run cracking process in the background
        threading.Thread(target=self.run_crack_in_background, args=(mode, hash_type, timeout)).start()

    # Function that runs the cracker in the background and updates GUI once done
    def run_crack_in_background(self, mode, hash_type, timeout):
        result = run_cracker(mode, hash_type, self.target_hash_path, self.wordlist_path, timeout)

        # Update GUI safely after processing is done
        self.after(0, self.display_results, result)

    # Function to animate the loading dots
    def animate_loading_dots(self):
        # Cycle through "Loading.", "Loading.." and "Loading..."
        if self.loading_text == "Loading.":
            self.loading_text = "Loading.."
        elif self.loading_text == "Loading..":
            self.loading_text = "Loading..."
        else:
            self.loading_text = "Loading."

        self.loading_label.configure(text=self.loading_text)

        # Call this method again in 500ms (adjustable)
        self.after(500, self.animate_loading_dots)

    # Function to display results and hide loading label
    def display_results(self, result):
        # Navigate to the Results page and pass the result
        self.controller.get_page("Results").display_results(result)
        self.controller.show_page("Results")

        # Reset the buttons and file paths
        self.target_hash_path = None
        self.wordlist_path = None
        self.upload_target_hash.configure(text="Upload Target Hash (txt file)", fg_color="#007ACC")
        self.upload_wordlist.configure(text="Upload Wordlist (txt file)", fg_color="#007ACC")

        # Hide the loading label after the process is complete
        self.loading_label.pack_forget()

        # Update wordlist button visibility after reset
        self.toggle_wordlist_button()
