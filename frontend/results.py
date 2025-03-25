import time

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

        if not results or "results" not in results or "overall_info" not in results:
            self.results_textbox.insert("1.0", "No results to display.")
            return

        # Display individual results
        for hash_value, data in results["results"].items():
            self.results_textbox.insert("end", f"Hash: {hash_value}\n")
            self.results_textbox.insert("end", f"Password: {data['password']}\n")
            self.results_textbox.insert("end", f"Time Taken: {data['time_taken']:.2f} seconds\n")
            self.results_textbox.insert("end", "-" * 80 + "\n")  # Separator

        # Display overall info
        overall = results["overall_info"]
        self.results_textbox.insert("end", "\n[Overall Statistics]\n")
        self.results_textbox.insert("end", f"Mode: {overall['mode']}\n")
        self.results_textbox.insert("end", f"Algorithm: {overall['algorithm']}\n")
        self.results_textbox.insert("end", f"Wordlist: {overall['wordlist']}\n")
        self.results_textbox.insert("end", f"Total Guesses: {overall['total_guesses']}\n")
        self.results_textbox.insert("end", f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['start_time']))}\n")
        self.results_textbox.insert("end", f"Finish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['finish_time']))}\n")
        self.results_textbox.insert("end", f"Overall Time: {overall['overall_time']:.2f} seconds\n")