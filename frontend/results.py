import customtkinter as ctk


class Results(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        label = ctk.CTkLabel(self, text="Results", font=("Arial", 24, "bold"))
        label.pack(pady=20)

        # Description
        description = ctk.CTkLabel(self, text="Hash Cracking Results", font=("Arial", 16))
        description.pack(pady=10)

        # Textbox for displaying results
        self.results_textbox = ctk.CTkTextbox(self, width=700, height=400)
        self.results_textbox.pack(pady=10, padx=20)

    def display_results(self, results):
        """Clear and display the results in the textbox."""
        self.results_textbox.delete("1.0", "end")  # Clear previous content

        if not results:
            self.results_textbox.insert("1.0", "No results to display.")
            return

        # Format and insert each hash and its plaintext
        for hash_value, plaintext in results.items():
            self.results_textbox.insert("end", f"Hash: {hash_value}\n")
            self.results_textbox.insert("end", f"Password: {plaintext}\n")
            self.results_textbox.insert("end", "-" * 80 + "\n")  # Separator
