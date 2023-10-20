import tkinter as tk
from tkinter import ttk
import random
import string
import subprocess
import pyperclip
from tkinter import filedialog
from pytube import YouTube

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
        else:
            password_display.config(text="Password length must be greater than 0")
    except ValueError:
        password_display.config(text="Invalid input for password length")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), 
        ("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css"), ("HTML Files", "*.html"),
        ("Java Files", "*.java"), ("PHP Files", "*.php"), ("Ruby Files", "*.rb"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            text_content = text_editor_text.get(1.0, tk.END)
            file.write(text_content)

def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), 
        ("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css"), ("HTML Files", "*.html"),
        ("Java Files", "*.java"), ("PHP Files", "*.php"), ("Ruby Files", "*.rb"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            text_content = text_editor_text.get(1.0, tk.END)
            file.write(text_content)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), 
        ("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("CSS Files", "*.css"), ("HTML Files", "*.html"),
        ("Java Files", "*.java"), ("PHP Files", "*.php"), ("Ruby Files", "*.rb"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            file_contents = file.read()
            text_editor_text.delete(1.0, tk.END)
            text_editor_text.insert(tk.END, file_contents)

def youtube_video_downloader():
    youtube_url = youtube_url_var.get()
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.get_highest_resolution()
        file_name = yt.title + ".mp4"
        stream.download(filename=file_name)
        downloaded_label.config(text=f"Downloaded: {file_name}")
    except Exception as e:
        downloaded_label.config(text=f"Error: {str(e)}")

root = tk.Tk()
root.title("Magnet")

style = ttk.Style()
style.theme_use("clam")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

password_generator_tab = create_tab("Password Generator")

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

text_save_button = ttk.Button(text_editor_tab, text="Save", command=save_file)
text_save_button.pack(side=tk.RIGHT)

text_save_as_button = ttk.Button(text_editor_tab, text="Save As", command=save_file_as)
text_save_as_button.pack(side=tk.RIGHT)

text_open_button = ttk.Button(text_editor_tab, text="Open", command=open_file)
text_open_button.pack(side=tk.RIGHT)

youtube_downloader_tab = create_tab("Video Downloader")

youtube_url_var = tk.StringVar()
youtube_url_entry = ttk.Entry(youtube_downloader_tab, textvariable=youtube_url_var)
youtube_url_entry.pack()

download_button = ttk.Button(youtube_downloader_tab, text="Download", command=youtube_video_downloader)
download_button.pack()

downloaded_label = ttk.Label(youtube_downloader_tab, text="", font=("Helvetica", 12))
downloaded_label.pack()

root.mainloop()
