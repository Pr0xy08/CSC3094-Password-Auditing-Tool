import time
import customtkinter as ctk
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import zxcvbn  # For password strength scoring


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

        # Frame for buttons to switch between graphs
        self.graph_buttons_frame = ctk.CTkFrame(self)
        self.graph_buttons_frame.pack(pady=10)

        # Buttons for switching between graphs
        self.char_freq_button = ctk.CTkButton(self.graph_buttons_frame, text="Character Frequency",
                                              command=self.show_character_frequency_graph)
        self.char_freq_button.pack(side="left", padx=10)

        self.pqi_button = ctk.CTkButton(self.graph_buttons_frame, text="PQI Graph", command=self.show_pqi_graph)
        self.pqi_button.pack(side="left", padx=10)

        self.password_strength_button = ctk.CTkButton(self.graph_buttons_frame, text="Password zxcvbn Score",
                                                      command=self.show_password_zxcvbn_graph)
        self.password_strength_button.pack(side="left", padx=10)

        # Frame for displaying the selected graph
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(pady=20)

        # Initially set the frame to be empty
        self.graph_canvas = None

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
            self.results_textbox.insert("end", f"Time Taken: {data['time_taken']:.10f} seconds\n")
            self.results_textbox.insert("end", "-" * 80 + "\n")

        # Display overall info
        overall = results["overall_info"]
        self.overall_results_textbox.insert("end", "\n[Overall Statistics]\n")
        self.overall_results_textbox.insert("end", f"Mode: {overall['mode']}\n")
        self.overall_results_textbox.insert("end", f"Algorithm: {overall['algorithm']}\n")
        self.overall_results_textbox.insert("end", f"Wordlist: {overall['wordlist']}\n")
        self.overall_results_textbox.insert("end", f"Total Hashes Attempted: {overall['total_hashes_attempts']}\n")
        self.overall_results_textbox.insert("end", f"Average Hashes/Second: {overall['avg_hashes_per_second']:.2f}\n")
        self.overall_results_textbox.insert("end",
                                            f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['start_time']))}\n")
        self.overall_results_textbox.insert("end",
                                            f"Finish Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall['finish_time']))}\n")
        self.overall_results_textbox.insert("end",
                                            f"Overall Time: {overall['overall_time']:.10f} seconds\n")

        # Store the results for later use
        self.results = results

    def show_character_frequency_graph(self):
        self._clear_graph_frame()
        self.display_character_frequency_graph(self.results)

    def show_pqi_graph(self):
        self._clear_graph_frame()
        self.display_password_quality_index_graph(self.results)

    def show_password_zxcvbn_graph(self):
        self._clear_graph_frame()
        self.display_password_zxcvbn_graph(self.results)

    def _clear_graph_frame(self):
        """Clears the current graph in the graph frame."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def display_character_frequency_graph(self, results):
        passwords = [data['password'] for data in results['results'].values() if
                     data['password'] != "Password not found."]
        all_passwords = "".join(passwords)
        char_count = Counter(all_passwords)
        sorted_char_count = dict(sorted(char_count.items(), key=lambda x: x[1]))

        # Set background color to match application dark theme (#2b2b2b)
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')  # Set figure background color
        ax.set_facecolor('#2b2b2b')  # Set axes background color
        ax.bar(sorted_char_count.keys(), sorted_char_count.values(), color='lightgreen')  # Bars in a light color
        ax.set_xlabel('Characters', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.set_title('Character Frequency Distribution', color='white')
        ax.tick_params(axis='both', labelcolor='white')  # Set tick label color to white

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory

    def display_password_quality_index_graph(self, results):
        def calculate_pqi(password):
            length_score = min(len(password) / 12, 1)
            unique_chars = len(set(password)) / len(password) if password else 0
            return length_score * unique_chars * 100

        passwords = [data['password'] for data in results['results'].values() if
                     data['password'] != "Password not found."]
        pqi_scores = {pwd: calculate_pqi(pwd) for pwd in passwords}
        sorted_pqi = dict(sorted(pqi_scores.items(), key=lambda x: x[1]))

        # Set background color to match application dark theme (#2b2b2b)
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')  # Set figure background color
        ax.set_facecolor('#2b2b2b')  # Set axes background color
        ax.barh(list(sorted_pqi.keys()), list(sorted_pqi.values()), color='lightcoral')  # Bars in a light color
        ax.set_xlabel('Password Quality Index (PQI)', color='white')
        ax.set_title('PQI for Each Password', color='white')
        ax.tick_params(axis='both', labelcolor='white')  # Set tick label color to white

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory

    def display_password_zxcvbn_graph(self, results):
        passwords = [data['password'] for data in results['results'].values() if
                     data['password'] != "Password not found."]

        # Use zxcvbn to calculate password strength score  (0-4)
        strength_scores = {pwd: zxcvbn.zxcvbn(pwd)['score'] for pwd in passwords}
        sorted_strength = dict(sorted(strength_scores.items(), key=lambda x: x[1]))

        # Set background color to match application dark theme (#2b2b2b)
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')  # Set figure background color
        ax.set_facecolor('#2b2b2b')  # Set axes background color
        ax.barh(list(sorted_strength.keys()), list(sorted_strength.values()), color='royalblue')  # Blue bars
        ax.set_xlabel('Password Strength (0-4)', color='white')
        ax.set_title('Password Strength for Each Password', color='white')
        ax.tick_params(axis='both', labelcolor='white')  # Set tick label color to white

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory
