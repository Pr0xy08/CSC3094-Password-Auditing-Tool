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

        # Frame for displaying the character frequency graph
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(pady=20)

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
        self.overall_results_textbox.insert("end",
                                            f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['start_time']))}\n")
        self.overall_results_textbox.insert("end",
                                            f"Finish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['finish_time']))}\n")
        self.overall_results_textbox.insert("end", f"Overall Time: {overall['overall_time']:.2f} seconds\n")

        # Generate character frequency graph for passwords
        self.display_character_frequency_graph(results)

    def display_character_frequency_graph(self, results):
        # Collect all the passwords, excluding "Password not found."
        passwords = [data['password'] for hash_value, data in results['results'].items() if
                     data['password'] != "Password not found."]
        # Combine all passwords into a single string
        all_passwords = "".join(passwords)

        # Count character frequency
        char_count = Counter(all_passwords)

        # Sort characters by frequency (lowest to highest)
        sorted_char_count = dict(sorted(char_count.items(), key=lambda x: x[1]))

        # Create a figure for the plot with a smaller size
        fig, ax = plt.subplots(figsize=(6, 4))  # Smaller graph size

        # Plot the character frequency
        ax.bar(sorted_char_count.keys(), sorted_char_count.values())

        ax.set_xlabel('Characters')
        ax.set_ylabel('Frequency')
        ax.set_title('Character Frequency Distribution')

        # Embed the plot into the tkinter window using a canvas
        for widget in self.graph_frame.winfo_children():
            widget.destroy()  # Remove any existing plot

        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()
