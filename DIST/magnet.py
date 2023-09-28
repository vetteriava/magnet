import tkinter as tk
from tkinter import ttk
import random
import string
import subprocess
import pyperclip

def create_tab(title):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=title)
    return tab

def execute_command():
    command = command_entry.get()
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        command_output.config(state=tk.NORMAL)
        command_output.delete(1.0, tk.END)
        command_output.insert(tk.END, output)
        command_output.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        command_output.config(state=tk.NORMAL)
        command_output.delete(1.0, tk.END)
        command_output.insert(tk.END, f"Error: {e.returncode}\n{e.output}")
        command_output.config(state=tk.DISABLED)
    except Exception as e:
        command_output.config(state=tk.NORMAL)
        command_output.delete(1.0, tk.END)
        command_output.insert(tk.END, str(e))
        command_output.config(state=tk.DISABLED)

def generate_password():
    try:
        password_length = int(password_length_var.get())
        if password_length > 0:
            characters = string.ascii_letters + string.digits + string.punctuation
            generated_password = ''.join(random.choice(characters) for _ in range(password_length))
            password_display.config(text=generated_password)
            pyperclip.copy(generated_password)
            copied_label.config(text="Copied to Clipboard")

            # Save the current text to the undo stack
            undo_stack.append(text_editor_text.get(1.0, tk.END))

            # Clear the redo stack
            redo_stack.clear()
        else:
            password_display.config(text="Password length must be greater than 0")
    except ValueError:
        password_display.config(text="Invalid input for password length")

# Function to undo the last change
def undo():
    if undo_stack:
        current_text = text_editor_text.get(1.0, tk.END)
        redo_stack.append(current_text)
        new_text = undo_stack.pop()
        text_editor_text.delete(1.0, tk.END)
        text_editor_text.insert(tk.END, new_text)

# Function to redo the last undone change
def redo():
    if redo_stack:
        current_text = text_editor_text.get(1.0, tk.END)
        undo_stack.append(current_text)
        new_text = redo_stack.pop()
        text_editor_text.delete(1.0, tk.END)
        text_editor_text.insert(tk.END, new_text)

root = tk.Tk()
root.title("Magnet")

style = ttk.Style()
style.theme_use("clam")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

password_generator_tab = create_tab("Password Generator")

password_length_label = ttk.Label(password_generator_tab, text="Password Length:")
password_length_label.pack()

password_length_var = tk.StringVar()
password_length_entry = ttk.Entry(password_generator_tab, textvariable=password_length_var)
password_length_entry.pack()

password_display = ttk.Label(password_generator_tab, text="", font=("Helvetica", 14))
password_display.pack()

generate_password_button = ttk.Button(password_generator_tab, text="Generate Password", command=generate_password)
generate_password_button.pack()

copied_label = ttk.Label(password_generator_tab, text="", font=("Helvetica", 12))
copied_label.pack()

command_prompt_tab = create_tab("Command Prompt")

command_entry = ttk.Entry(command_prompt_tab, font=("Helvetica", 12))
command_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

command_output = tk.Text(command_prompt_tab, wrap=tk.WORD, font=("Helvetica", 12))
command_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
command_output.config(state=tk.DISABLED)

run_command_button = ttk.Button(command_prompt_tab, text="Run Command", command=execute_command)
run_command_button.pack()

text_editor_tab = create_tab("Text Editor")

text_editor_text = tk.Text(text_editor_tab, wrap=tk.WORD, font=("Helvetica", 12))
text_editor_text.pack(fill=tk.BOTH, expand=True)

text_save_button = ttk.Button(text_editor_tab, text="Save")
text_save_button.pack(side=tk.RIGHT)

text_save_as_button = ttk.Button(text_editor_tab, text="Save As")
text_save_as_button.pack(side=tk.RIGHT)

text_open_button = ttk.Button(text_editor_tab, text="Open")
text_open_button.pack(side=tk.RIGHT)

# Initialize stacks for undo and redo
undo_stack = []
redo_stack = []

root.mainloop()