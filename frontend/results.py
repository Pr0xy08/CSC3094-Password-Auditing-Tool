import time
import customtkinter as ctk
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import zxcvbn
import pandas as pd
import mplcursors
import matplotlib

matplotlib.use('TkAgg')  # Use TkAgg backend for matplotlib


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

        self.system_usage_button = ctk.CTkButton(self.graph_buttons_frame, text="System Usage Graph",
                                                 command=self.show_system_usage_graph)
        self.system_usage_button.pack(side="left", padx=10)

        self.password_length_button = ctk.CTkButton(self.graph_buttons_frame, text="Password Length Graph",
                                                    command=self.show_password_length_graph)
        self.password_length_button.pack(side="left", padx=10)

        # Button for showing the Success Rate Pie Chart
        self.success_rate_button = ctk.CTkButton(self.graph_buttons_frame, text="Success Rate Pie Chart",
                                                 command=self.show_success_rate_pie_chart)
        self.success_rate_button.pack(side="left", padx=10)

        # Frame for displaying the selected graph
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(pady=20)

        # Initially set the frame to be empty
        self.graph_canvas = None

    def display_results(self, results):  # displays results in text boxes and updates graphs
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

        # Automatically update the graphs with new data
        self.update_graphs(results)

    def update_graphs(self, results):  # updates graph with most current data
        self._clear_graph_frame()  # Clear the old graph

        # Update the graphs based on the new data
        self.show_success_rate_pie_chart()
        self.show_character_frequency_graph()
        self.show_pqi_graph()
        self.show_password_zxcvbn_graph()
        self.show_system_usage_graph()
        self.show_password_length_graph()

    def show_character_frequency_graph(self):
        self._clear_graph_frame()
        self.generate_character_frequency_graph(self.results)

    def show_pqi_graph(self):
        self._clear_graph_frame()
        self.generate_password_quality_index_graph(self.results)

    def show_password_zxcvbn_graph(self):
        self._clear_graph_frame()
        self.generate_password_zxcvbn_graph(self.results)

    def show_system_usage_graph(self):
        self._clear_graph_frame()
        self.generate_system_usage()

    def show_password_length_graph(self):
        self._clear_graph_frame()
        self.generate_password_length_graph(self.results)

    def show_success_rate_pie_chart(self):
        self._clear_graph_frame()
        self.generate_success_rate_pie_chart(self.results)

    def generate_character_frequency_graph(self, results):  # character freq graph of all characters in passwords found
        passwords = [data['password'] for data in results['results'].values() if
                     data['password'] != "Password not found."]  # don't include passwords not found
        all_passwords = "".join(passwords)
        char_count = Counter(all_passwords)
        sorted_char_count = dict(sorted(char_count.items(), key=lambda x: x[1]))

        # Convert the dictionary keys and values to lists
        sorted_keys = list(sorted_char_count.keys())
        sorted_values = list(sorted_char_count.values())

        # plot graph
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        bars = ax.bar(sorted_keys, sorted_values, color='lightgreen')
        ax.set_xlabel('Characters', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.set_title('Character Frequency Distribution', color='white')
        ax.tick_params(axis='both', labelcolor='white')

        # Add tooltips with mplcursors
        mplcursors.cursor(bars, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f'Character: {sorted_keys[sel.index]}\n'
                                                       f'Frequency: {int(sorted_values[sel.index])}'))

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)

    def generate_password_quality_index_graph(self, results):  # Password Quality Index Graph
        def calculate_pqi(password):  # function for finding pqi
            length_score = min(len(password) / 12, 1)
            unique_chars = len(set(password)) / len(password) if password else 0
            return length_score * unique_chars * 100

        passwords = [data['password'] for data in results['results'].values() if  # don't include passwords not found
                     data['password'] != "Password not found."]
        pqi_scores = {pwd: calculate_pqi(pwd) for pwd in passwords}  # calculate scores for each
        sorted_pqi = dict(sorted(pqi_scores.items(), key=lambda x: x[1]))  # sort from the highest score to lowest

        # plot graph
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        bars = ax.barh(list(sorted_pqi.keys()), list(sorted_pqi.values()), color='lightcoral')
        ax.set_xlabel('Password Quality Index (PQI)', color='white')
        ax.set_title('PQI for Each Password', color='white')
        ax.tick_params(axis='both', labelcolor='white')

        # Add tooltips with mplcursors
        mplcursors.cursor(bars, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f'Password: {list(sorted_pqi.keys())[sel.index]}\n'
                                                       f'PQI Score: {list(sorted_pqi.values())[sel.index]:.2f}'))

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)

    def generate_password_zxcvbn_graph(self, results):  # Password Strength (zxcvbn) Graph
        passwords = [data['password'] for data in results['results'].values() if  # dont include passwords not found
                     data['password'] != "Password not found."]

        # Use zxcvbn to calculate password strength score (0-4)
        strength_scores = {pwd: zxcvbn.zxcvbn(pwd)['score'] for pwd in passwords}
        sorted_strength = dict(sorted(strength_scores.items(), key=lambda x: x[1]))

        # plot graph
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        bars = ax.barh(list(sorted_strength.keys()), list(sorted_strength.values()), color='royalblue')
        ax.set_xlabel('Password Strength (0-4)', color='white')
        ax.set_title('Password Strength for Each Password', color='white')
        ax.tick_params(axis='both', labelcolor='white')

        # Add tooltips with mplcursors
        mplcursors.cursor(bars, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(f'Password: {list(sorted_strength.keys())[sel.index]}\n'
                                                       f'Strength: {list(sorted_strength.values())[sel.index]}'))

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)

    def generate_system_usage(self, log_file="usage_log.txt"):
        # Read the timestamp, cpu usage and ram usage data into a DataFrame (usage log)
        df = pd.read_csv(log_file, names=["timestamp", "cpu_usage", "ram_usage"])

        # Convert timestamps to readable format
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        # Plot the data
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax1.set_facecolor('#2b2b2b')
        ax2.set_facecolor('#2b2b2b')

        # Plot CPU usage
        ax1.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage (%)', color='blue')
        ax1.set_title('CPU Usage Over Time', color='white')
        ax1.set_xlabel('Time', color='white')
        ax1.set_ylabel('CPU Usage (%)', color='white')
        ax1.grid(True, color='gray')
        ax1.tick_params(axis='both', colors='white')
        ax1.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')

        # Plot RAM usage
        ax2.plot(df['timestamp'], df['ram_usage'], label='RAM Usage (%)', color='green')
        ax2.set_title('RAM Usage Over Time', color='white')
        ax2.set_xlabel('Time', color='white')
        ax2.set_ylabel('RAM Usage (%)', color='white')
        ax2.grid(True, color='gray')
        ax2.tick_params(axis='both', colors='white')
        ax2.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')

        plt.tight_layout()

        # Display the graph in the tkinter window
        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory

    def generate_password_length_graph(self, results):  # password length histogram
        passwords = [data['password'] for data in results['results'].values() if  # don't include passwords not found
                     data['password'] != "Password not found."]

        password_lengths = [len(pwd) for pwd in passwords]  # get length for each

        if not password_lengths:  # If password_lengths is empty, just return or display an empty graph
            # plot graph
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#2b2b2b')
            ax.set_facecolor('#2b2b2b')
            ax.set_xlabel('Password Length', color='white')
            ax.set_ylabel('Frequency', color='white')
            ax.set_title('Distribution of Password Lengths', color='white')
            ax.tick_params(axis='both', labelcolor='white')
            ax.set_xticks([])
            ax.set_yticks([])
            self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
            self.graph_canvas.get_tk_widget().pack()
            self.graph_canvas.draw()
            plt.close(fig)  # Prevents the figure from staying open in memory
            return

        # Proceed to plot the histogram if password_lengths is not empty
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        n, bins, patches = ax.hist(password_lengths, bins=range(min(password_lengths), max(password_lengths) + 2),
                                   color='skyblue', edgecolor='white', alpha=0.75)

        ax.set_xlabel('Password Length', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.set_title('Distribution of Password Lengths', color='white')
        ax.tick_params(axis='both', labelcolor='white')

        # Add tooltips using mplcursors
        mplcursors.cursor(patches, hover=True).connect(
            "add",
            lambda sel: sel.annotation.set_text(
                f'Length: {int(bins[sel.index])} - {int(bins[sel.index + 1])} chars\n'
                f'Frequency: {int(n[sel.index])}'))

        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory

    def generate_success_rate_pie_chart(self, results): # Function to create the Success Rate Pie Chart
        # Define success and failure counts
        success_count = sum(1 for data in results['results'].values() if data['password'] != "Password not found.")
        failure_count = len(results['results']) - success_count

        # Data for the pie chart
        labels = ['Success', 'Failure']
        sizes = [success_count, failure_count]
        colors = ['#4CAF50', '#F44336']  # Green and red

        # plot pie
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
               textprops={'color': 'white'}, wedgeprops={'edgecolor': 'black'})
        ax.set_title('Success Rate', color='white')

        # Display the graph in the tkinter window
        self.graph_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        self.graph_canvas.get_tk_widget().pack()
        self.graph_canvas.draw()

        # Close the figure after rendering it
        plt.close(fig)  # Prevents the figure from staying open in memory

    def _clear_graph_frame(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
