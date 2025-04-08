import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from modules.signature import DigitalSignature  # Import the DigitalSignature class

class SignTab:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        
        # Initialize DigitalSignature
        self.signature_tool = DigitalSignature()
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the sign tab UI"""
        # Frame for signing
        sign_frame = ttk.LabelFrame(self.frame, text="Ký số")
        sign_frame.pack(fill='x', padx=10, pady=10)
        
        # File selection
        file_frame = ttk.Frame(sign_frame)
        file_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(file_frame, text="Chọn tệp:").pack(side='left', padx=5)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(file_frame, text="Chọn", command=self.select_file).pack(side='left', padx=5)
        
        # Hash algorithm selection
        hash_frame = ttk.Frame(sign_frame)
        hash_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(hash_frame, text="Thuật toán hash:").pack(side='left', padx=5)
        self.hash_algo = tk.StringVar(value="SHA256")
        hash_algos = ["SHA256", "SHA384", "SHA512"]
        ttk.Combobox(hash_frame, textvariable=self.hash_algo, values=hash_algos, width=10).pack(side='left', padx=5)
        
        # Sign button
        btn_frame = ttk.Frame(sign_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Ký", command=self.sign_file).pack(side='left', padx=5)
    
    def select_file(self):
        """Select a file to sign"""
        filename = filedialog.askopenfilename(
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
    
    def sign_file(self):
        """Sign the selected file"""
        try:
            file_path = self.file_path.get()
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("Lỗi", "Tệp không tồn tại.")
                return
            
            private_key = self.shared_state.get("private_key")
            if not private_key:
                messagebox.showerror("Lỗi", "Chưa có khóa riêng. Vui lòng tải hoặc tạo khóa trước.")
                return
            
            hash_algo = self.hash_algo.get()
            signature = self.signature_tool.sign_file(file_path, private_key, hash_algo)
            
            # Save signature
            save_path = filedialog.asksaveasfilename(
                defaultextension=".sig",
                filetypes=[("Signature files", "*.sig"), ("All files", "*.*")]
            )
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(signature)
                self.shared_state["current_signature"] = signature
                messagebox.showinfo("Thành công", f"Đã ký tệp và lưu chữ ký vào {save_path}")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể ký tệp: {str(e)}")