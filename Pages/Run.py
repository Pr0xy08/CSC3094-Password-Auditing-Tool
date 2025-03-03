import customtkinter as ctk


class Run(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        def mode_combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        def type_combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        label = ctk.CTkLabel(self, text="Run", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(self, text="This is the Run Page", font=("Arial", 16))
        description.pack(pady=10)

        # select cracking mode
        mode_combobox = ctk.CTkComboBox(self, values=["Brute Force", "Wordlist"], command=mode_combobox_callback)
        mode_combobox.pack(padx=20, pady=10)
        mode_combobox.set("Wordlist")  # set initial value

        # select hash type
        type_combobox = ctk.CTkComboBox(self, values=["Ascon-Hash256", "Ascon-XOF128", "Ascon-CXOF128", "MD5", "SHA-1", "DES", "SHA-256", "SHA-512", "scrypt", "bcrypt", "PBKDF2"], command=type_combobox_callback)
        type_combobox.pack(padx=20, pady=10)
        type_combobox.set("MD5")
