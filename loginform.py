import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Hàm kết nối cơ sở dữ liệu PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="loginform",  
            user="postgres",         
            password="123456",  
            port="5432"    
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Giá trị tài khoản và mật khẩu cố định
fixed_username = "my_account"
fixed_password = "my_password"

# Tab Đăng Nhập
def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            messagebox.showinfo("Success", "Đăng nhập thành công!")
        else:
            messagebox.showwarning("Login Error", "Sai tên đăng nhập hoặc mật khẩu!")

# Tab Đăng Ký
def register():
    username = entry_register_username.get()  
    password = entry_register_password.get()
    confirm_password = entry_confirm_password.get()  # Lấy giá trị mật khẩu xác nhận
    
    if username and password and confirm_password:
        if password != confirm_password:
            messagebox.showwarning("Register Error", "Mật khẩu và xác nhận mật khẩu không khớp!")
            return
        if username == fixed_username and password == fixed_password:
            messagebox.showwarning("Register Error", "Tên đăng nhập đã tồn tại!")
        else:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    # Chèn tài khoản mới vào bảng users
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "Đăng ký thành công!")
                except psycopg2.IntegrityError:
                    messagebox.showerror("Register Error", "Tên đăng nhập đã tồn tại!")
                    conn.rollback()  # rollback khi có lỗi
                except Exception as e:
                    messagebox.showerror("Register Error", str(e))
                finally:
                    conn.close()
    else:
        messagebox.showwarning("Register Error", "Vui lòng nhập đầy đủ thông tin!")

# Tìm kiếm tài khoản và hiển thị ID và tên đăng nhập
def search_user():
    username = entry_search_username.get()
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        # Truy vấn tìm kiếm người dùng theo tên đăng nhập
        cursor.execute("SELECT id, username FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()  # Lấy bản ghi đầu tiên (nếu có)
        conn.close()
        
        if user:
            # Hiển thị ID và tên đăng nhập nếu tìm thấy
            messagebox.showinfo("User Found", f"ID: {user[0]}\nTên đăng nhập: {user[1]}")
        else:
            messagebox.showwarning("Search Result", "Không tìm thấy người dùng!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Login Form")
root.geometry("400x400")

# Đặt font chữ cho giao diện
font_label = ('Arial', 12)
font_entry = ('Arial', 12)
font_button = ('Arial', 12, 'bold')

# Tạo notebook cho các tab
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tab Đăng Nhập
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Đăng Nhập")

tk.Label(login_tab, text="Tên đăng nhập:", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_login_username = tk.Entry(login_tab, font=font_entry)
entry_login_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_tab, text="Mật khẩu:", font=font_label).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_login_password = tk.Entry(login_tab, show="*", font=font_entry)
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

btn_login = tk.Button(login_tab, text="Đăng Nhập", command=login, font=font_button)
btn_login.grid(row=2, column=0, columnspan=2, pady=20)

# Tab Đăng Ký
register_tab = ttk.Frame(notebook)
notebook.add(register_tab, text="Đăng Ký")

tk.Label(register_tab, text="Tên đăng nhập:", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_register_username = tk.Entry(register_tab, font=font_entry)
entry_register_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(register_tab, text="Mật khẩu:", font=font_label).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_register_password = tk.Entry(register_tab, show="*", font=font_entry)
entry_register_password.grid(row=1, column=1, padx=10, pady=10)

tk.Label(register_tab, text="Xác nhận mật khẩu:", font=font_label).grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_confirm_password = tk.Entry(register_tab, show="*", font=font_entry)
entry_confirm_password.grid(row=2, column=1, padx=10, pady=10)

btn_register = tk.Button(register_tab, text="Đăng Ký", command=register, font=font_button)
btn_register.grid(row=3, column=0, columnspan=2, pady=20)

# Tab Tìm Kiếm
search_tab = ttk.Frame(notebook)
notebook.add(search_tab, text="Tìm Kiếm")

tk.Label(search_tab, text="Tên đăng nhập:", font=font_label).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_search_username = tk.Entry(search_tab, font=font_entry)
entry_search_username.grid(row=0, column=1, padx=10, pady=10)

btn_search = tk.Button(search_tab, text="Tìm Kiếm", command=search_user, font=font_button)
btn_search.grid(row=1, column=0, columnspan=2, pady=20)

root.mainloop()
