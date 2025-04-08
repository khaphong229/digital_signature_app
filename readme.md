# Ứng dụng Chữ Ký Số

Ứng dụng này cho phép người dùng tạo và xác thực chữ ký số sử dụng các thuật toán mã hóa hiện đại như RSA và DSA. Ứng dụng cung cấp giao diện đồ họa để quản lý khóa, ký số, và xác thực chữ ký.

## Tính Năng

- **Quản lý Khóa**: Tạo, lưu, và tải khóa riêng và khóa công khai.
- **Ký Số**: Ký tệp bằng khóa riêng và lưu chữ ký.
- **Xác Thực Chữ Ký**: Xác thực chữ ký của tệp bằng khóa công khai.

## Cài Đặt

### Yêu Cầu

- Python 3.x
- Các thư viện Python: `tkinter`, `cryptography`

### Hướng Dẫn Cài Đặt

1. **Clone dự án từ GitHub**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Tạo và kích hoạt môi trường ảo**:

   - **Tạo môi trường ảo**:
     ```bash
     python -m venv venv
     ```
   - **Kích hoạt môi trường ảo**:
     - Trên Windows:
       ```bash
       .\venv\Scripts\activate
       ```
     - Trên macOS và Linux:
       ```bash
       source venv/bin/activate
       ```

3. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install cryptography
   ```

## Sử Dụng

1. **Chạy ứng dụng**:

   ```bash
   python main.py
   ```

2. **Quản lý khóa**:

   - Chọn tab "Quản lý khóa" để tạo cặp khóa mới.
   - Lưu khóa riêng và khóa công khai vào tệp.

3. **Ký số**:

   - Chọn tab "Ký số" để chọn tệp cần ký.
   - Chọn thuật toán hash và nhấn "Ký" để tạo chữ ký.

4. **Xác thực chữ ký**:
   - Chọn tab "Xác thực chữ ký" để chọn tệp và chữ ký cần xác thực.
   - Nhấn "Xác thực" để kiểm tra tính hợp lệ của chữ ký.

## Thông Tin Liên Hệ

- **Tác giả**: [Tên của bạn]
- **Email**: [Email của bạn]
- **GitHub**: [GitHub của bạn]

## Ghi Chú

- Đảm bảo bảo vệ khóa riêng của bạn và không chia sẻ với người khác.
- Khóa công khai có thể được chia sẻ để xác thực chữ ký.
- Chọn kích thước khóa lớn hơn để tăng tính bảo mật.
