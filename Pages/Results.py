import customtkinter as ctk


class Results(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Results", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(self, text="This is the Results page", font=("Arial", 16))
        description.pack(pady=10)
