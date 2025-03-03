import customtkinter as ctk


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(self, text="Welcome to the Dashboard", font=("Arial", 16))
        description.pack(pady=10)
