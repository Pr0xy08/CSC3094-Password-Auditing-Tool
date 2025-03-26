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

        # Frame for organizing the textboxes side by side
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(pady=10, padx=20)

        # Textbox for displaying individual results
        self.results_textbox = ctk.CTkTextbox(results_frame, width=350, height=175)
        self.results_textbox.pack(side="left", padx=10)

        # Textbox for displaying overall results
        self.overall_results_textbox = ctk.CTkTextbox(results_frame, width=350, height=175)
        self.overall_results_textbox.pack(side="left", padx=10)

    def display_results(self, results):
        """Clear and display the results in the textboxes."""
        self.results_textbox.delete("1.0", "end")  # Clear previous content
        self.overall_results_textbox.delete("1.0", "end")  # Clear previous content

        if not results or "results" not in results or "overall_info" not in results:
            self.results_textbox.insert("1.0", "No results to display.")
            return

        # Display individual results
        for hash_value, data in results["results"].items():
            self.results_textbox.insert("end", f"Hash: {hash_value}\n")
            self.results_textbox.insert("end", f"Password: {data['password']}\n")
            self.results_textbox.insert("end", f"Time Taken: {data['time_taken']:.2f} seconds\n")
            self.results_textbox.insert("end", "-" * 80 + "\n")  # Separator

        # Display overall info in the second textbox
        overall = results["overall_info"]
        self.overall_results_textbox.insert("end", "\n[Overall Statistics]\n")
        self.overall_results_textbox.insert("end", f"Mode: {overall['mode']}\n")
        self.overall_results_textbox.insert("end", f"Algorithm: {overall['algorithm']}\n")
        self.overall_results_textbox.insert("end", f"Wordlist: {overall['wordlist']}\n")
        self.overall_results_textbox.insert("end", f"Total Guesses: {overall['total_guesses']}\n")
        self.overall_results_textbox.insert("end", f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['start_time']))}\n")
        self.overall_results_textbox.insert("end", f"Finish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['finish_time']))}\n")
        self.overall_results_textbox.insert("end", f"Overall Time: {overall['overall_time']:.2f} seconds\n")