import customtkinter as ctk


class Results(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Results", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(self, text="Results of the audit will appear below:", font=("Arial", 16))
        description.pack(pady=10)

        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 16), wraplength=600)
        self.output_label.pack(pady=10)

    # Function to update the result on the Results page
    def display_result(self, result):
        self.output_label.configure(text=result)
