from tkinter import filedialog


def select_file():
    filename = filedialog.askopenfilename()
    if filename:  # Check if a file was selected
        print("Selected file:", filename)

        # Try to open and read the contents of the file
        try:
            with open(filename, 'r') as file:  # Open the file in read mode
                file_contents = file.read()  # Read the entire file contents
                print("File contents:")
                print(file_contents)  # Print the contents of the file
        except Exception as e:
            print(f"Error reading file: {e}")


def mode_combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


def type_combobox_callback(choice):
    print("combobox dropdown clicked:", choice)