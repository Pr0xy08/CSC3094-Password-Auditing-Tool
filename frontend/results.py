import time
import customtkinter as ctk
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        # Frame for displaying graphs side by side
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(pady=20)

        self.char_freq_frame = ctk.CTkFrame(self.graph_frame)
        self.char_freq_frame.pack(side="left", padx=10)

        self.pqi_frame = ctk.CTkFrame(self.graph_frame)
        self.pqi_frame.pack(side="left", padx=10)

    def display_results(self, results):
        """Clear and display the results in the textboxes."""
        self.results_textbox.delete("1.0", "end")
        self.overall_results_textbox.delete("1.0", "end")

        if not results or "results" not in results or "overall_info" not in results:
            self.results_textbox.insert("1.0", "No results to display.")
            return

        # Display individual results
        for hash_value, data in results["results"].items():
            self.results_textbox.insert("end", f"Hash: {hash_value}\n")
            self.results_textbox.insert("end", f"Password: {data['password']}\n")
            self.results_textbox.insert("end", f"Time Taken: {data['time_taken']:.2f} seconds\n")
            self.results_textbox.insert("end", "-" * 80 + "\n")

        # Display overall info
        overall = results["overall_info"]
        self.overall_results_textbox.insert("end", "\n[Overall Statistics]\n")
        self.overall_results_textbox.insert("end", f"Mode: {overall['mode']}\n")
        self.overall_results_textbox.insert("end", f"Algorithm: {overall['algorithm']}\n")
        self.overall_results_textbox.insert("end", f"Wordlist: {overall['wordlist']}\n")
        self.overall_results_textbox.insert("end", f"Total Guesses: {overall['total_guesses']}\n")
        self.overall_results_textbox.insert("end", f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['start_time']))}\n")
        self.overall_results_textbox.insert("end", f"Finish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['finish_time']))}\n")
        self.overall_results_textbox.insert("end", f"Overall Time: {overall['overall_time']:.2f} seconds\n")

        # Generate graphs
        self.display_character_frequency_graph(results)
        self.display_password_quality_index_graph(results)

    def display_character_frequency_graph(self, results):
        passwords = [data['password'] for data in results['results'].values() if data['password'] != "Password not found."]
        all_passwords = "".join(passwords)
        char_count = Counter(all_passwords)
        sorted_char_count = dict(sorted(char_count.items(), key=lambda x: x[1]))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(sorted_char_count.keys(), sorted_char_count.values())
        ax.set_xlabel('Characters')
        ax.set_ylabel('Frequency')
        ax.set_title('Character Frequency Distribution')

        for widget in self.char_freq_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, self.char_freq_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def display_password_quality_index_graph(self, results):
        def calculate_pqi(password):
            length_score = min(len(password) / 12, 1)
            unique_chars = len(set(password)) / len(password) if password else 0
            return length_score * unique_chars * 100

        passwords = [data['password'] for data in results['results'].values() if data['password'] != "Password not found."]
        pqi_scores = {pwd: calculate_pqi(pwd) for pwd in passwords}
        sorted_pqi = dict(sorted(pqi_scores.items(), key=lambda x: x[1]))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(list(sorted_pqi.keys()), list(sorted_pqi.values()))
        ax.set_xlabel('Password Quality Index (PQI)')
        ax.set_title('PQI for Each Password')

        for widget in self.pqi_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, self.pqi_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()