import tkinter as tk
from tkinter import filedialog, messagebox
from securecrypto import aes_utils


def encrypt():
    global last_key
    file = filedialog.askopenfilename(title="Chọn file để mã hóa")
    if not file:
        return
    pw = password_entry.get()
    key = aes_utils.encrypt_file_aes(file, pw)
    last_key = key
    result_label.config(text=f"🔑 Key: {key}")


def decrypt():
    file = filedialog.askopenfilename(title="Chọn file để giải mã")
    if not file:
        return
    pw = password_entry.get()
    out = aes_utils.decrypt_file_aes(file, pw)
    result_label.config(text=f"📂 Output: {out}")


def copy_key():
    if last_key:
        root.clipboard_clear()
        root.clipboard_append(last_key)
        root.update()
        messagebox.showinfo("Thông báo", "Key đã được copy vào clipboard!")
    else:
        messagebox.showwarning("Cảnh báo", "Chưa có key để copy!")


# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("SecureCrypto GUI")
root.geometry("700x300")  # chỉnh kích thước cửa sổ

last_key = None  # lưu key gần nhất

# Khung nhập mật khẩu
pw_frame = tk.Frame(root, pady=10)
pw_frame.pack()
tk.Label(pw_frame, text="Nhập mật khẩu:", font=("Arial", 12)).pack(side="left", padx=5)
password_entry = tk.Entry(pw_frame, show="*", width=30, font=("Arial", 12))
password_entry.pack(side="left")

# Các nút chức năng
btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()
tk.Button(btn_frame, text="Encrypt", command=encrypt, width=12, font=("Arial", 11)).pack(side="left", padx=10)
tk.Button(btn_frame, text="Decrypt", command=decrypt, width=12, font=("Arial", 11)).pack(side="left", padx=10)
tk.Button(btn_frame, text="Copy Key", command=copy_key, width=12, font=("Arial", 11)).pack(side="left", padx=10)

# Kết quả
result_label = tk.Label(root, text="", font=("Consolas", 11), fg="blue", wraplength=650, justify="center")
result_label.pack(pady=15)

root.mainloop()
