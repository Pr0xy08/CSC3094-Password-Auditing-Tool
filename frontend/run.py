from tkinter import END
import customtkinter as ctk


from backend.run_backend import mode_combobox_callback, type_combobox_callback, select_file


class Run(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        """
        def getText():
            print(textbox.get('1.0', END))
        """

        # title
        label = ctk.CTkLabel(self, text="Run", font=("Arial", 24))
        label.pack(pady=20)

        description = ctk.CTkLabel(self, text="This is the Run Page", font=("Arial", 16))
        description.pack(pady=10)

        # select cracking mode
        mode_combobox = ctk.CTkComboBox(self, values=["Brute Force", "Wordlist"], command=mode_combobox_callback)
        mode_combobox.pack(padx=20, pady=10)
        mode_combobox.set("Wordlist")  # set initial value

        # select hash type
        type_combobox = ctk.CTkComboBox(self,
                                        values=["Ascon-Hash256", "Ascon-XOF128", "Ascon-CXOF128", "MD5", "SHA-1", "DES",
                                                "SHA-256", "SHA-512", "scrypt", "bcrypt", "PBKDF2"],
                                        command=type_combobox_callback)
        type_combobox.pack(padx=20, pady=10)
        type_combobox.set("MD5")

        # upload target hash file (as txt)
        button_to_select = ctk.CTkButton(self, text="Upload target hash (txt file)", fg_color="blue", command=select_file)
        button_to_select.pack(padx=25, pady=25)

        # upload wordlist (as txt)
        button_to_select = ctk.CTkButton(self, text="Upload wordlist (txt file)", fg_color="blue",
                                         command=select_file)
        button_to_select.pack(padx=25, pady=25)

        """"
        textbox = ctk.CTkTextbox(self)
        button = ctk.CTkButton(self, text="Upload target hash", command=getText)
        textbox.pack(pady=30, padx=20)
        button.pack(pady=30, padx=20)
        """

