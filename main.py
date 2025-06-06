import customtkinter as ctk
from frontend.help import Help
from frontend.results import Results
from frontend.run import Run

# Initialize CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.title("Password Auditing Tool")
        self.geometry("800x500")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(4, weight=1)  # Push logout button to bottom

        # Sidebar Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="ASCON Audit", font=("Arial", 20, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar Buttons
        self.run_button = ctk.CTkButton(self.sidebar, text="Run", command=self.show_run)
        self.run_button.grid(row=1, column=0, padx=10, pady=10)

        self.results_button = ctk.CTkButton(self.sidebar, text="Results", command=self.show_results)
        self.results_button.grid(row=2, column=0, padx=10, pady=10)

        self.help_button = ctk.CTkButton(self.sidebar, text="Help", command=self.show_help)
        self.help_button.grid(row=3, column=0, padx=10, pady=10)

        # Exit Button
        self.exit_button = ctk.CTkButton(self.sidebar, text="Exit", fg_color="red", hover_color="darkred",
                                         command=self.quit)
        self.exit_button.grid(row=5, column=0, padx=20, pady=20)

        # Main Content Area (frontend)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew")

        # Initialize Frames (frontend)
        self.pages = {}  # Store pages in a dictionary
        for Page in (Run, Results, Help):
            page_name = Page.__name__
            self.pages[page_name] = Page(parent=self.container, controller=self)
            self.pages[page_name].grid(row=0, column=0, sticky="nsew")

        self.show_run()  # Start with dashboard Page

    def show_page(self, page_name): # shows a specific page
        frame = self.pages[page_name]
        frame.tkraise()  # Bring the frame to the front

    def get_page(self, page_name): # gets instance of a page
        return self.pages.get(page_name)

    def show_run(self):
        self.show_page("Run")

    def show_results(self):
        self.show_page("Results")

    def show_help(self):
        self.show_page("Help")


if __name__ == "__main__":
    app = Main()
    app.mainloop()
