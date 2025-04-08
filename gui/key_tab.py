import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from modules.key_generator import KeyGenerator

class KeyTab:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        
        # Initialize key generator
        self.key_gen = KeyGenerator()
        
        # Variables
        self.private_key_path = tk.StringVar()
        self.public_key_path = tk.StringVar()
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the key management tab UI"""
        # Frame for key generation
        gen_frame = ttk.LabelFrame(self.frame, text="Sinh cặp khóa mới")
        gen_frame.pack(fill='x', padx=10, pady=10)
        
        # Algorithm selection
        algo_frame = ttk.Frame(gen_frame)
        algo_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(algo_frame, text="Thuật toán:").pack(side='left', padx=5)
        self.algo_var = tk.StringVar(value="RSA")
        ttk.Radiobutton(algo_frame, text="RSA", variable=self.algo_var, value="RSA").pack(side='left', padx=5)
        ttk.Radiobutton(algo_frame, text="DSA", variable=self.algo_var, value="DSA").pack(side='left', padx=5)
        
        # Key size selection
        size_frame = ttk.Frame(gen_frame)
        size_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(size_frame, text="Kích thước khóa:").pack(side='left', padx=5)
        self.key_size = tk.StringVar(value="2048")
        key_sizes = ["1024", "2048", "3072", "4096"]
        ttk.Combobox(size_frame, textvariable=self.key_size, values=key_sizes, width=10).pack(side='left', padx=5)
        
        # Generate button
        btn_frame = ttk.Frame(gen_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Sinh cặp khóa", command=self.generate_keys).pack(side='left', padx=5)
        
        # Frame for saving keys
        save_frame = ttk.LabelFrame(self.frame, text="Lưu khóa")
        save_frame.pack(fill='x', padx=10, pady=10)
        
        # Private key
        priv_frame = ttk.Frame(save_frame)
        priv_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(priv_frame, text="Khóa riêng:").pack(side='left', padx=5)
        ttk.Entry(priv_frame, textvariable=self.private_key_path, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(priv_frame, text="Lưu", command=self.save_private_key).pack(side='left', padx=5)
        
        # Public key
        pub_frame = ttk.Frame(save_frame)
        pub_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(pub_frame, text="Khóa công khai:").pack(side='left', padx=5)
        ttk.Entry(pub_frame, textvariable=self.public_key_path, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(pub_frame, text="Lưu", command=self.save_public_key).pack(side='left', padx=5)
        
        # Frame for loading keys
        load_frame = ttk.LabelFrame(self.frame, text="Tải khóa")
        load_frame.pack(fill='x', padx=10, pady=10)
        
        # Load private key
        load_priv_frame = ttk.Frame(load_frame)
        load_priv_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(load_priv_frame, text="Khóa riêng:").pack(side='left', padx=5)
        ttk.Button(load_priv_frame, text="Tải khóa riêng", command=self.load_private_key).pack(side='left', padx=5)
        self.priv_key_status = ttk.Label(load_priv_frame, text="Chưa tải")
        self.priv_key_status.pack(side='left', padx=5)
        
        # Load public key
        load_pub_frame = ttk.Frame(load_frame)
        load_pub_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(load_pub_frame, text="Khóa công khai:").pack(side='left', padx=5)
        ttk.Button(load_pub_frame, text="Tải khóa công khai", command=self.load_public_key).pack(side='left', padx=5)
        self.pub_key_status = ttk.Label(load_pub_frame, text="Chưa tải")
        self.pub_key_status.pack(side='left', padx=5)
    
    def generate_keys(self):
        """Generate a new key pair"""
        try:
            algorithm = self.algo_var.get()
            key_size = int(self.key_size.get())
            
            if algorithm == "RSA":
                private_key, public_key = self.key_gen.generate_rsa_keys(key_size=key_size)
                messagebox.showinfo("Thành công", f"Đã sinh cặp khóa RSA {key_size} bits")
            else:  # DSA
                private_key, public_key = self.key_gen.generate_dsa_keys(key_size=key_size)
                messagebox.showinfo("Thành công", f"Đã sinh cặp khóa DSA {key_size} bits")
            
            # Update shared state
            self.shared_state["private_key"] = private_key
            self.shared_state["public_key"] = public_key
            
            # Update status labels
            self.priv_key_status.config(text="Đã tạo")
            self.pub_key_status.config(text="Đã tạo")
            
            # Display key information
            self.private_key_path.set("Khóa riêng đã tạo")
            self.public_key_path.set("Khóa công khai đã tạo")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sinh khóa: {str(e)}")
    
    def save_private_key(self):
        """Save private key to file"""
        try:
            if not self.shared_state["private_key"]:
                messagebox.showerror("Lỗi", "Chưa có khóa riêng. Vui lòng sinh khóa trước.")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pem", 
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Password protection option
            use_password = messagebox.askyesno("Bảo vệ khóa", "Bạn có muốn đặt mật khẩu cho khóa riêng?")
            password = None
            if use_password:
                password = simpledialog.askstring("Mật khẩu", "Nhập mật khẩu:", show='*')
                if not password:  # Cancel or empty password
                    return
            
            self.key_gen.save_private_key(filename, password)
            self.private_key_path.set(filename)
            messagebox.showinfo("Thành công", f"Đã lưu khóa riêng vào {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu khóa riêng: {str(e)}")
    
    def save_public_key(self):
        """Save public key to file"""
        try:
            if not self.shared_state["public_key"]:
                messagebox.showerror("Lỗi", "Chưa có khóa công khai. Vui lòng sinh khóa trước.")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pem", 
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            self.key_gen.save_public_key(filename)
            self.public_key_path.set(filename)
            messagebox.showinfo("Thành công", f"Đã lưu khóa công khai vào {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu khóa công khai: {str(e)}")
    
    def load_private_key(self):
        """Load private key from file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Password prompt
            try:
                # First try without password
                private_key = self.key_gen.load_private_key(filename)
            except Exception:
                # If fails, ask for password
                password = simpledialog.askstring("Mật khẩu", "Nhập mật khẩu cho khóa riêng:", show='*')
                if password is None:  # User cancelled
                    return
                private_key = self.key_gen.load_private_key(filename, password)
            
            # Update shared state
            self.shared_state["private_key"] = private_key
            self.priv_key_status.config(text="Đã tải")
            
            messagebox.showinfo("Thành công", f"Đã tải khóa riêng từ {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải khóa riêng: {str(e)}")
    
    def load_public_key(self):
        """Load public key from file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            public_key = self.key_gen.load_public_key(filename)
            
            # Update shared state
            self.shared_state["public_key"] = public_key
            self.pub_key_status.config(text="Đã tải")
            
            messagebox.showinfo("Thành công", f"Đã tải khóa công khai từ {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải khóa công khai: {str(e)}")
