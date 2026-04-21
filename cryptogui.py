#!/usr/bin/env python3

import customtkinter as ctk
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
import os, subprocess

from scripts.info.tool_info import TOOL_INFO
from scripts.info.compatibility_table import compatibility_table

class CryptoGUI:
    def __init__(self):

        # --- CONFIGURATION ---

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # --- CREATE GUI ---

        self.root = ctk.CTk()
        self.root.title("Cryptography GUI")
        self.root.geometry("800x1000")

        # TITLE AND LOGIC

        ctk.CTkLabel(self.root, text="Cryptography tools", font=("Roboto", 50)).pack(pady=20, padx=20) # Title
        ctk.CTkFrame(self.root, height=5, fg_color="gray").pack(pady=25, padx=20, fill="x") # Separator

        tool_var = ctk.StringVar(value="") # Variable to store the selected tool
        operation_var = ctk.StringVar(value="") # Variable to store the selected operation
        text_var = ctk.StringVar(value="") # Variable to store the text
        key_var = ctk.StringVar(value="") # Variable to store the key

        home_path = os.path.expanduser("~")

        tool_names = [tool["name"] for tool in TOOL_INFO.values()] # List of tool names (pretty names)
        tool_names.insert(0, "")
        name_to_key = { # Dictionary to map pretty names to TOOL_INFO keys
            TOOL_INFO[tool]["name"]: tool for tool in TOOL_INFO.keys()
        }

        def on_tool_change(choice): # Function to update the operations menu when a tool is selected
            try: # If the tool is not in TOOL_INFO, set tool_var to "" and clear the operations menu
                tool_var.set(name_to_key[choice])
                operation_menu.configure(values=TOOL_INFO[tool_var.get()]["operations"])
            except:
                tool_var.set("")
                operation_menu.configure(values=[])
                
            operation_var.set("")

        def on_operation_change(choice): # Function to update the text and key entries when an operation is selected
            widgets = [text, text_file, key, key_file] # List of widgets to update

            if choice in ["encrypt", "decrypt"]: # If the operation is encrypt or decrypt, enable the text and key entries
                for widget in widgets:
                    widget.configure(state="normal")

            elif choice == "bruteforce": # If the operation is bruteforce, enable the text entry and disable the key entry
                for widget in widgets:
                    if widgets.index(widget) < 2:
                        widget.configure(state="normal")
                    else:
                        widget.configure(state="disabled")
            else:
                for widget in widgets: # If the operation is not encrypt, decrypt, or bruteforce, disable all entries
                    widget.configure(state="disabled")

        def text_file_open(): # Function to open a file for text
            file = filedialog.askopenfile(initialdir=home_path, title="Abrir archivo", filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*")]) # Open a file dialog
            if file: # If a file was selected
                content = file.read().strip() # Read the file and strip whitespace
                file.close() # Close the file
                text.delete("1.0", "end") # Clear the textbox
                text.insert("1.0", content) # Insert the file content into the textbox

        def key_file_open(): # Function to open a file for the key
            file = filedialog.askopenfile(initialdir=home_path, title="Abrir archivo", filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*")]) # Open a file dialog
            if file: # If a file was selected
                content = file.read().strip() # Read the file and strip whitespace
                file.close() # Close the file
                key.delete("0", "end") # Clear the key entry
                key.insert("0", content) # Insert the file content into the key entry

        def run_command(): # Function to run the command selected in the GUI
            if tool_var.get() == "": # If no tool is selected, show an error message
                CTkMessagebox(title="Error", icon="warning", message="Select a tool", font=("Roboto", 16))
                return
            if operation_var.get() == "": # If no operation is selected, show an error message
                CTkMessagebox(title="Error", icon="warning", message="Select an operation", font=("Roboto", 16))
                return
            if operation_var.get() in ["encrypt", "decrypt", "bruteforce"] and text.get("1.0", "end").strip() == "":
                CTkMessagebox(title="Error", icon="warning", message="Text is required", font=("Roboto", 16))
                return
            if operation_var.get() in ["encrypt", "decrypt"] and key.get() == "":
                CTkMessagebox(title="Error", icon="warning", message="Key is required", font=("Roboto", 16))
                return

            # We prepare the command to run the crypto script
            command = ["python3", "crypto.py", f"--{tool_var.get()}", f"-{operation_var.get()[0]}"] # for operation, we do [0] to grab the first character

            if operation_var.get() in ["encrypt", "decrypt", "bruteforce"]: # If it requires text, we add it to the command
                command.extend(['-t', f'"{text.get("1.0", "end-1c")}"']) # we add -t "text" between "" to avoid spaces in the command

            if operation_var.get() in ["encrypt", "decrypt"]: # If it requires a key, we add it to the command
                command.extend(["-k", key.get().strip()])

            try: # We try to run the command
                result = subprocess.run(command, capture_output=True, text=True, check=True) # We capture the output and check for errors
                CTkMessagebox(title="Result", icon="", message=result.stdout, font=("Roboto", 16), width=600)

            except subprocess.CalledProcessError as e:
                CTkMessagebox(title="Error en ejecución", icon="cancel", message=e.stderr.strip() if e.stderr else str(e), font=("Roboto", 16))

        # GUI ELEMENTS

        ctk.CTkLabel(self.root, text="Select a tool", font=("Roboto", 30)).pack(pady=10, padx=20) # Select a tool label
        tool_menu = ctk.CTkOptionMenu(self.root, values=tool_names, command=on_tool_change, width=480, font=("Roboto", 16))
        tool_menu.pack(pady=10, padx=20) # Tool menu

        ctk.CTkLabel(self.root, text="Select an operation", font=("Roboto", 30)).pack(pady=10, padx=20) # Select an operation label
        operation_menu = ctk.CTkOptionMenu(self.root, variable=operation_var, values=[], command=on_operation_change, width=480, font=("Roboto", 16))
        operation_menu.pack(pady=10, padx=20) # Operation menu

        ctk.CTkLabel(self.root, text="Text", font=("Roboto", 30)).pack(pady=10, padx=20) # Text label
        text = ctk.CTkTextbox(self.root, width=480, height=100, font=("Roboto", 16), state="disabled")
        text.pack(pady=10, padx=20) # Textbox
        text_file = ctk.CTkButton(self.root, text="Open file for text", command=text_file_open, width=480, font=("Roboto", 16), state="disabled")
        text_file.pack(pady=10, padx=20) # Button to open a file

        ctk.CTkLabel(self.root, text="Key", font=("Roboto", 30)).pack(pady=10, padx=20) # Key label
        key = ctk.CTkEntry(self.root, width=480, font=("Roboto", 16), state="disabled")
        key.pack(pady=10, padx=20) # Key entry
        key_file = ctk.CTkButton(self.root, text="Open file for key", command=key_file_open, width=480, font=("Roboto", 16), state="disabled")
        key_file.pack(pady=10, padx=20) # Button to open a file

        ctk.CTkFrame(self.root, height=5, fg_color="gray").pack(pady=25, padx=20, fill="x")  # Separator

        run_button = ctk.CTkButton(self.root, text="Run", command=run_command, width=480, font=("Roboto", 16)) # Run button
        run_button.pack(pady=10, padx=20)

        self.root.mainloop() # Start the GUI

CryptoGUI() # Create the GUI