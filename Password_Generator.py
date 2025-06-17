import tkinter as tk
from tkinter import messagebox
import random, string, os, pyperclip
from cryptography.fernet import Fernet
import pyfiglet
import ttkbootstrap as ttkb

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, "secret.key")
STORAGE_FILE = os.path.join(BASE_DIR, "passwords.enc")

# === Banner ===
print(pyfiglet.figlet_format("PyPassword 🔐"))

# === Load/Create Secret Key ===
def load_or_create_key_if_needed():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()

# === Password Generation ===
def generate_password(nr_letters, nr_symbols, nr_numbers):
    if nr_letters + nr_symbols + nr_numbers < 1:
        raise ValueError("Password must contain at least 1 character.")

    letters = string.ascii_letters
    numbers = string.digits
    symbols = '!#$%&()*+'

    password_chars = (
        (random.sample(letters, 1) if nr_letters else []) +
        (random.sample(symbols, 1) if nr_symbols else []) +
        (random.sample(numbers, 1) if nr_numbers else [])
    )

    password_chars += random.choices(letters, k=nr_letters - bool(nr_letters))
    password_chars += random.choices(symbols, k=nr_symbols - bool(nr_symbols))
    password_chars += random.choices(numbers, k=nr_numbers - bool(nr_numbers))

    random.shuffle(password_chars)
    return ''.join(password_chars)

def get_strength(password):
    score = sum([
        len(password) >= 12,
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(c in '!#$%&()*+' for c in password)
    ])
    return {
        5: "🟢 Strong",
        4: "🟡 Medium",
        3: "🟠 Weak"
    }.get(score, "🔴 Very Weak")

# === Save Password ===
def save_password(password):
    key = load_or_create_key_if_needed()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    with open(STORAGE_FILE, "ab") as f:
        f.write(encrypted + b"\n")

# === GUI Logic ===
def on_generate():
    try:
        letters = int(letters_var.get())
        symbols = int(symbols_var.get())
        numbers = int(numbers_var.get())

        password = generate_password(letters, symbols, numbers)
        pyperclip.copy(password)
        save_password(password)

        result_label.config(text=f"🔑 {password}")
        strength_label.config(text=f"Password Strength: {get_strength(password)}")

        messagebox.showinfo("Success", "Password copied to clipboard and saved securely!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Setup ===
app = ttkb.Window(themename="superhero")  # <-- Change theme here, e.g., "darkly", "cyborg", "solar"
app.title("🔐 PyPassword Generator")
app.geometry("480x460")
app.resizable(False, False)

frame = ttkb.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

ttkb_label = ttkb.Label(frame, text="🔐 PyPassword Generator", font=("Segoe UI", 20, "bold"))
ttkb_label.pack(pady=(0, 25))

letters_var = tk.StringVar(value="8")
symbols_var = tk.StringVar(value="2")
numbers_var = tk.StringVar(value="2")

def add_input(label_text, variable):
    label = ttkb.Label(frame, text=label_text, font=("Segoe UI", 12))
    label.pack(anchor="w", pady=(8, 2))
    entry = ttkb.Entry(frame, textvariable=variable, bootstyle="info")
    entry.pack(fill="x")

add_input("Number of Letters:", letters_var)
add_input("Number of Symbols:", symbols_var)
add_input("Number of Numbers:", numbers_var)

generate_btn = ttkb.Button(frame, text="✨ Generate Password", command=on_generate, bootstyle="success")
generate_btn.pack(pady=25, fill="x")

result_label = ttkb.Label(frame, text="", font=("Courier New", 14), foreground="#333")
result_label.pack(pady=(0, 10))

strength_label = ttkb.Label(frame, text="", font=("Segoe UI", 12, "italic"), foreground="#555")
strength_label.pack()

app.mainloop()