import tkinter as tk
from tkinter import ttk
from gui.key_tab import KeyTab
from gui.sign_tab import SignTab
from gui.verify_tab import VerifyTab

class DigitalSignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Chữ ký số")
        self.root.geometry("800x600")
        
        # Apply a basic theme
        style = ttk.Style()
        style.theme_use('clam')  # You can try 'alt', 'default', 'classic', 'clam'
        
        # Create notebook (tabs container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create shared state (to share objects between tabs)
        self.shared_state = {
            "private_key": None,
            "public_key": None,
            "current_signature": None
        }
        
        # Initialize tabs
        self.key_tab = KeyTab(self.notebook, self.shared_state)
        self.sign_tab = SignTab(self.notebook, self.shared_state)
        self.verify_tab = VerifyTab(self.notebook, self.shared_state)
        
        # Add tabs to notebook
        self.notebook.add(self.key_tab.frame, text="Quản lý khóa")
        self.notebook.add(self.sign_tab.frame, text="Ký số")
        self.notebook.add(self.verify_tab.frame, text="Xác thực chữ ký")
        
        # Set up menu
        self.create_menu()
        
        # Status bar
        self.status_var = tk.StringVar(value="Sẵn sàng")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Create main menu"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Tạo cặp khóa mới", command=self.key_tab.generate_keys)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="Tệp", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Ký văn bản/tệp", command=lambda: self.notebook.select(1))  # Select sign tab
        tools_menu.add_command(label="Xác thực chữ ký", command=lambda: self.notebook.select(2))  # Select verify tab
        menubar.add_cascade(label="Công cụ", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_help(self):
        """Show help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Hướng dẫn sử dụng")
        help_window.geometry("500x400")
        
        text = tk.Text(help_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add help content
        help_content = """
        HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG CHỮ KÝ SỐ
        
        1. Tab Quản lý khóa
           - Tạo cặp khóa RSA hoặc DSA với kích thước tùy chọn
           - Lưu khóa riêng và khóa công khai vào tệp
           - Có thể bảo vệ khóa riêng bằng mật khẩu
           - Tải khóa từ tệp đã lưu
        
        2. Tab Ký số
           - Ký văn bản hoặc tệp sử dụng khóa riêng
           - Chọn thuật toán hash (SHA256, SHA384, SHA512)
           - Lưu chữ ký vào tệp
        
        3. Tab Xác thực chữ ký
           - Xác thực chữ ký của văn bản hoặc tệp
           - Sử dụng khóa công khai để xác thực
           - Hiển thị kết quả xác thực
        
        Lưu ý quan trọng:
        - Bảo vệ khóa riêng của bạn, không chia sẻ với người khác
        - Khóa công khai có thể chia sẻ cho người cần xác thực chữ ký
        - Chọn kích thước khóa lớn hơn để tăng tính bảo mật
        """
        
        text.insert(tk.END, help_content)
        text.config(state=tk.DISABLED)  # Make read-only
    
    def show_about(self):
        """Show about dialog"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Giới thiệu", 
            "Ứng dụng Chữ ký số\n"
            "Phiên bản 1.0\n\n"
            "Ứng dụng cho phép tạo và xác thực chữ ký số sử dụng các thuật toán mã hóa hiện đại."
        )
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
