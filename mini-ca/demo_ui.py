import os
import tkinter as tk
from tkinter import messagebox
from ca_utils import (
    create_root_ca,
    create_intermediate_ca,
    issue_certificate,
    verify_certificate_chain,
    load_cert
)
from revoke_utils import (
    revoke_certificate,
    check_revocation_status
)
from cryptography import x509

class CADemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini CA Demo UI")
        self.geometry("450x350")
        
        # Class variables to hold keys and certs
        self.root_key = None
        self.root_cert = None
        self.inter_key = None
        self.inter_cert = None
        self.user_cert_path = None
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Mini CA Demo", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.log_text = tk.Text(self, height=10, width=55, state='disabled', bg="#f0f0f0")
        self.log_text.pack(pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="1. Tạo Root & Intermediate CA", command=self.setup_ca).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="2. Phát hành User Cert", command=self.issue_cert).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="3. Kiểm tra Chuỗi Cert", command=self.verify_chain).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="4. Thu hồi User Cert", command=self.revoke_cert).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="5. Kiểm tra Trạng thái Thu hồi", command=self.ocsp_check).grid(row=2, column=0, columnspan=2, pady=5)

    def log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def setup_ca(self):
        self.log("Tạo Root CA...")
        self.root_key, self.root_cert = create_root_ca()
        self.log("Root CA tạo xong.")
        
        self.log("Tạo Intermediate CA...")
        self.inter_key, self.inter_cert = create_intermediate_ca(self.root_key, self.root_cert)
        self.log("Intermediate CA tạo xong.")
        messagebox.showinfo("Thông báo", "Đã tạo Root và Intermediate CA thành công!")

    def issue_cert(self):
        if not self.inter_key or not self.inter_cert:
            messagebox.showerror("Lỗi", "Phải tạo CA trước khi phát hành chứng chỉ!")
            return
            
        subject_info = {"common_name": "Phuoc_Nguyen", "org": "PHUOCNTMH Company", "country": "VN"}
        self.log("Phát hành chứng chỉ người dùng cuối...")
        _, _ = issue_certificate(self.inter_key, self.inter_cert, subject_info)
        self.user_cert_path = os.path.join("certs", f"{subject_info['common_name']}_cert.pem")
        self.log(f"Đã phát hành: {self.user_cert_path}")
        messagebox.showinfo("Thông báo", "Phát hành chứng chỉ thành công!")

    def verify_chain(self):
        if not self.user_cert_path or not os.path.exists(self.user_cert_path):
            messagebox.showerror("Lỗi", "Chưa có chứng chỉ user để kiểm tra!")
            return
            
        self.log("Kiểm tra chuỗi chứng chỉ...")
        chain_paths = [os.path.join("certs", "intermediate_cert.pem"), os.path.join("certs", "root_ca_cert.pem")]
        chain_certs = [load_cert(p) for p in chain_paths]
        user_cert = load_cert(self.user_cert_path)
        valid = verify_certificate_chain(user_cert, chain_certs)
        self.log(f"Chuỗi hợp lệ: {valid}")
        messagebox.showinfo("Kết quả", f"Chuỗi chứng chỉ hợp lệ: {valid}")

    def revoke_cert(self):
        cert_file = os.path.join("certs", "Phuoc_Nguyen_cert.pem")
        issuer_cert = os.path.join("certs", "intermediate_cert.pem")
        issuer_key = os.path.join("certs", "intermediate_key.pem")
        
        if not all(os.path.exists(p) for p in [cert_file, issuer_cert, issuer_key]):
            messagebox.showerror("Lỗi", "Thiếu file chứng chỉ hoặc khóa để thu hồi!")
            return
            
        self.log("Thu hồi chứng chỉ user...")
        revoke_certificate(cert_file, issuer_cert, issuer_key, reason=x509.ReasonFlags.key_compromise)
        self.log("Đã thu hồi chứng chỉ")
        messagebox.showinfo("Thông báo", "Chứng chỉ đã được thu hồi!")

    def ocsp_check(self):
        cert_file = os.path.join("certs", "Phuoc_Nguyen_cert.pem")
        if not os.path.exists(cert_file):
            messagebox.showerror("Lỗi", "Chưa có chứng chỉ user để kiểm tra!")
            return
            
        self.log("Kiểm tra trạng thái thu hồi...")
        status = check_revocation_status(cert_file)
        result_text = 'Đã thu hồi' if status else 'Hợp lệ'
        self.log(f"Trạng thái: {result_text}")
        messagebox.showinfo("Kết quả", f"Trạng thái: {result_text}")

if __name__ == "__main__":
    app = CADemoApp()
    app.mainloop()