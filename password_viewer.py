import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
import pyperclip

# === Decrypt Function ===
def decrypt_passwords(key_path, enc_path):
    try:
        with open(key_path, "rb") as f:
            key = f.read()
        fernet = Fernet(key)

        with open(enc_path, "rb") as f:
            lines = f.readlines()

        decrypted = []
        for i, line in enumerate(lines):
            try:
                decrypted_pw = fernet.decrypt(line.strip()).decode()
                decrypted.append(f"{i+1}. {decrypted_pw}")
            except InvalidToken:
                decrypted.append(f"{i+1}. ❌ Invalid or corrupted entry.")
        return decrypted

    except Exception as e:
        return [f"Error: {str(e)}"]

# === Load Files and Show Passwords ===
def load_and_show():
    key_path = filedialog.askopenfilename(title="Select secret.key", filetypes=[("Key Files", "*.key")])
    if not key_path:
        return
    enc_path = filedialog.askopenfilename(title="Select passwords.enc", filetypes=[("Encrypted Files", "*.enc")])
    if not enc_path:
        return

    passwords = decrypt_passwords(key_path, enc_path)
    text_box.delete("1.0", tk.END)
    for line in passwords:
        text_box.insert(tk.END, line + "\n")

# === Copy to Clipboard ===
def copy_to_clipboard():
    selected_text = text_box.get("sel.first", "sel.last")
    if selected_text:
        pyperclip.copy(selected_text)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Selection", "Please select a password to copy.")

# === GUI Setup ===
viewer = ttkb.Window(themename="superhero")
viewer.title("🔎 PyPassword Viewer")
viewer.geometry("600x420")

# Define a custom style for the button
style = ttkb.Style()
style.configure("LargeButton.TButton", font=("Segoe UI", 14, "bold"), padding=(10, 5))

viewer.grid_columnconfigure(0, weight=1)
viewer.grid_rowconfigure(0, weight=1)
viewer.grid_rowconfigure(1, weight=1)
viewer.grid_rowconfigure(2, weight=1)

ttkb.Label(viewer, text="🔑 View Encrypted Passwords", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=15, sticky="nsew")

# Use the custom style for the button
load_button = ttkb.Button(viewer, text="Load Key & Encrypted File", style="LargeButton.TButton", command=load_and_show)
load_button.grid(row=1, column=0, pady=10, sticky="nsew")

frame = ttkb.Frame(viewer)
frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

scrollbar = ttkb.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

text_box = tk.Text(frame, wrap="word", font=("Courier New", 11), yscrollcommand=scrollbar.set)
text_box.pack(fill="both", expand=True)

scrollbar.config(command=text_box.yview)

copy_button = ttkb.Button(viewer, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=3, column=0, pady=10, sticky="nsew")

viewer.mainloop()


