
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from modules.signature import DigitalSignature  # Import the DigitalSignature class

class VerifyTab:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        
        # Initialize DigitalSignature
        self.signature_tool = DigitalSignature()
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the verify tab UI"""
        # Frame for verification
        verify_frame = ttk.LabelFrame(self.frame, text="Xác thực chữ ký")
        verify_frame.pack(fill='x', padx=10, pady=10)
        
        # File selection
        file_frame = ttk.Frame(verify_frame)
        file_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(file_frame, text="Chọn tệp:").pack(side='left', padx=5)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(file_frame, text="Chọn", command=self.select_file).pack(side='left', padx=5)
        
        # Signature selection
        sig_frame = ttk.Frame(verify_frame)
        sig_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(sig_frame, text="Chọn chữ ký:").pack(side='left', padx=5)
        self.signature_path = tk.StringVar()
        ttk.Entry(sig_frame, textvariable=self.signature_path, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(sig_frame, text="Chọn", command=self.select_signature).pack(side='left', padx=5)

        # Hash algorithm selection
        hash_frame = ttk.Frame(verify_frame)
        hash_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(hash_frame, text="Thuật toán hash:").pack(side='left', padx=5)
        self.hash_algo = tk.StringVar(value="SHA256")
        hash_algos = ["SHA256", "SHA384", "SHA512"]
        ttk.Combobox(hash_frame, textvariable=self.hash_algo, values=hash_algos, width=10).pack(side='left', padx=5)

        # Verify button
        btn_frame = ttk.Frame(verify_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Xác thực", command=self.verify_signature).pack(side='left', padx=5)
    
    def select_file(self):
        """Select a file to verify"""
        filename = filedialog.askopenfilename(
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
    
    def select_signature(self):
        """Select a signature file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")]
        )
        if filename:
            self.signature_path.set(filename)
    
    def verify_signature(self):
        """Verify the signature of the selected file and display time taken"""
        try:
            file_path = self.file_path.get()
            signature_path = self.signature_path.get()
            
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("Lỗi", "Tệp không tồn tại.")
                return
            
            if not signature_path or not os.path.exists(signature_path):
                messagebox.showerror("Lỗi", "Chữ ký không tồn tại.")
                return
            
            public_key = self.shared_state.get("public_key")
            if not public_key:
                messagebox.showerror("Lỗi", "Chưa có khóa công khai. Vui lòng tải hoặc tạo khóa trước.")
                return
            
            with open(signature_path, "rb") as f:
                signature = f.read()
            
            hash_algo = self.hash_algo.get()  # Get the selected hash algorithm
            is_valid = self.signature_tool.verify_file_signature(file_path, signature, public_key, hash_algorithm=hash_algo)
            if is_valid:
                messagebox.showinfo("Thành công", "Chữ ký hợp lệ.")
            else:
                messagebox.showerror("Lỗi", "Chữ ký không hợp lệ.")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xác thực chữ ký: {str(e)}")