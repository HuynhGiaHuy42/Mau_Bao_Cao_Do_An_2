import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from models.models import SinhVien, ChuyenNganh, User
from sqlalchemy.orm import sessionmaker


class SinhVienApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh Viên")
        self.root.geometry("800x500")
        self.root.configure(bg="#f5f5f5")  # Màu nền sáng cho ứng dụng
        
        self.db_manager = DatabaseManager()
        self.db_session = self.db_manager.get_session()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Khung chứa bảng sinh viên
        self.frame_treeview = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid")
        self.frame_treeview.pack(padx=20, pady=20, fill="both", expand=True)

        # Treeview để hiển thị danh sách sinh viên
        self.tree = ttk.Treeview(self.frame_treeview, columns=("STT", "ID", "Tên", "Tuổi", "Giới tính", "Chuyên ngành"), show="headings", height=15)
        self.tree.heading("STT", text="STT")
        self.tree.heading("ID", text="Mã sinh viên")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tuổi", text="Tuổi")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("Chuyên ngành", text="Chuyên ngành")

        # Cải thiện Treeview bằng Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Các nút chức năng
        self.frame_buttons = tk.Frame(self.root, bg="#f5f5f5")
        self.frame_buttons.pack(padx=20, pady=10)

        self.btn_add = tk.Button(self.frame_buttons, text="Thêm Sinh Viên", command=self.open_add_form, bg="#4CAF50", fg="white", relief="flat", width=15)
        self.btn_add.grid(row=0, column=0, padx=10)

        self.btn_edit = tk.Button(self.frame_buttons, text="Sửa Sinh Viên", command=self.open_edit_form, bg="#FFC107", fg="white", relief="flat", width=15)
        self.btn_edit.grid(row=0, column=1, padx=10)

        self.btn_delete = tk.Button(self.frame_buttons, text="Xóa Sinh Viên", command=self.delete_sinh_vien, bg="#F44336", fg="white", relief="flat", width=15)
        self.btn_delete.grid(row=0, column=2, padx=10)

        # Nút "Quản lý Chuyên Ngành"
        self.btn_manage_cn = tk.Button(self.frame_buttons, text="Quản lý Chuyên Ngành", command=self.open_chuyen_nganh_app, bg="#2196F3", fg="white", relief="flat", width=20)
        self.btn_manage_cn.grid(row=1, column=0, columnspan=3, pady=10)

    def load_data(self):
        # Lấy danh sách sinh viên và hiển thị lên giao diện
        for row in self.tree.get_children():
            self.tree.delete(row)

        sinh_viens = self.db_session.query(SinhVien).all()
        for idx, sv in enumerate(sinh_viens, 1):  # Thêm STT
            self.tree.insert("", "end", values=(idx, sv.ID, sv.Ten, sv.Tuoi, "Nam" if sv.GioiTinh else "Nữ", sv.chuyen_nganh.TenChuyenNganh))

    def open_add_form(self):
        AddSinhVienForm(self.root, self.db_session, self.load_data)

    def open_edit_form(self):
        selected_item = self.tree.selection()
        if selected_item:
            sv_id = self.tree.item(selected_item, "values")[1]
            sv = self.db_session.query(SinhVien).get(sv_id)
            AddSinhVienForm(self.root, self.db_session, self.load_data, sv)

    def delete_sinh_vien(self):
        selected_item = self.tree.selection()
        if selected_item:
            sv_id = self.tree.item(selected_item, "values")[1]
            sv = self.db_session.query(SinhVien).get(sv_id)
            self.db_session.delete(sv)
            self.db_session.commit()
            self.load_data()
            messagebox.showinfo("Thông báo", "Sinh viên đã được xóa.")
        else:
            messagebox.showwarning("Lỗi", "Chọn sinh viên cần xóa.")

    def open_chuyen_nganh_app(self):
        # Ẩn các phần tử của SinhVienApp
        self.frame_treeview.grid_forget()
        self.frame_buttons.grid_forget()

        # Mở cửa sổ quản lý chuyên ngành
        chuyen_nganh_root = tk.Tk()
        app = ChuyenNganhApp(chuyen_nganh_root, self)
        chuyen_nganh_root.mainloop()

    def quit_chuyen_nganh_app(self):
        # Quay lại từ cửa sổ Chuyên Ngành
        self.frame_treeview.grid(padx=20, pady=20, fill="both", expand=True)
        self.frame_buttons.grid(padx=20, pady=10)


class AddSinhVienForm:
    def __init__(self, parent, db_session, reload_callback, sinh_vien=None):
        self.top = tk.Toplevel(parent)
        self.db_session = db_session
        self.reload_callback = reload_callback
        self.sinh_vien = sinh_vien

        self.top.title("Thêm/Sửa Sinh Viên")
        self.top.geometry("400x300")
        self.top.configure(bg="#f5f5f5")

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho Tên Sinh Viên
        self.ten_label = tk.Label(self.top, text="Tên Sinh Viên:", bg="#f5f5f5")
        self.ten_label.grid(row=0, column=0, pady=10, sticky="e")
        self.ten_entry = tk.Entry(self.top, width=30)
        self.ten_entry.grid(row=0, column=1, pady=10)
        if self.sinh_vien:
            self.ten_entry.insert(0, self.sinh_vien.Ten)

        # Label và Entry cho Tuổi
        self.tuoi_label = tk.Label(self.top, text="Tuổi Sinh Viên:", bg="#f5f5f5")
        self.tuoi_label.grid(row=1, column=0, pady=10, sticky="e")
        self.tuoi_entry = tk.Entry(self.top, width=30)
        self.tuoi_entry.grid(row=1, column=1, pady=10)
        if self.sinh_vien:
            self.tuoi_entry.insert(0, self.sinh_vien.Tuoi)

        # Label và Radiobutton cho Giới Tính
        self.gioi_tinh_label = tk.Label(self.top, text="Giới Tính:", bg="#f5f5f5")
        self.gioi_tinh_label.grid(row=2, column=0, pady=10, sticky="e")
        self.gioi_tinh_var = tk.StringVar(value="Nam")
        self.gioi_tinh_radio1 = tk.Radiobutton(self.top, text="Nam", variable=self.gioi_tinh_var, value="Nam", bg="#f5f5f5")
        self.gioi_tinh_radio2 = tk.Radiobutton(self.top, text="Nữ", variable=self.gioi_tinh_var, value="Nữ", bg="#f5f5f5")
        self.gioi_tinh_radio1.grid(row=2, column=1, sticky="w")
        self.gioi_tinh_radio2.grid(row=2, column=1, sticky="e")
        if self.sinh_vien:
            if self.sinh_vien.GioiTinh:
                self.gioi_tinh_var.set("Nam")
            else:
                self.gioi_tinh_var.set("Nữ")

        # Label và Combobox cho Chuyên Ngành
        self.chuyen_nganh_label = tk.Label(self.top, text="Chuyên Ngành:", bg="#f5f5f5")
        self.chuyen_nganh_label.grid(row=3, column=0, pady=10, sticky="e")
        self.chuyen_nganh_combobox = ttk.Combobox(self.top, width=30, values=[cn.TenChuyenNganh for cn in self.db_session.query(ChuyenNganh).all()])
        self.chuyen_nganh_combobox.grid(row=3, column=1, pady=10)
        if self.sinh_vien:
            self.chuyen_nganh_combobox.set(self.sinh_vien.chuyen_nganh.TenChuyenNganh)

        # Nút Lưu
        self.submit_button = tk.Button(self.top, text="Lưu", command=self.save_sinh_vien, bg="#4CAF50", fg="white", relief="flat", width=15)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_sinh_vien(self):
        ten = self.ten_entry.get()
        tuoi = self.tuoi_entry.get()
        gioi_tinh = True if self.gioi_tinh_var.get() == "Nam" else False
        chuyen_nganh_ten = self.chuyen_nganh_combobox.get()

        # Kiểm tra dữ liệu hợp lệ
        if not ten or not tuoi.isdigit() or not chuyen_nganh_ten:
            messagebox.showwarning("Lỗi", "Vui lòng điền đủ thông tin hợp lệ!")
            return

        chuyen_nganh = self.db_session.query(ChuyenNganh).filter_by(TenChuyenNganh=chuyen_nganh_ten).first()

        if self.sinh_vien:
            # Sửa thông tin sinh viên
            self.sinh_vien.Ten = ten
            self.sinh_vien.Tuoi = int(tuoi)
            self.sinh_vien.GioiTinh = gioi_tinh
            self.sinh_vien.ChuyenNganhID = chuyen_nganh.ChuyenNganhID
        else:
            # Thêm sinh viên mới
            sinh_vien = SinhVien(
                Ten=ten,
                Tuoi=int(tuoi),
                GioiTinh=gioi_tinh,
                ChuyenNganhID=chuyen_nganh.ChuyenNganhID
            )
            self.db_session.add(sinh_vien)

        self.db_session.commit()
        self.reload_callback()
        self.top.destroy()
        messagebox.showinfo("Thông báo", "Sinh viên đã được lưu.")
class LoginRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập / Đăng Ký")
        self.root.geometry("400x300")
        self.db_manager = DatabaseManager()
        self.db_session = self.db_manager.get_session()
        
        self.create_widgets()

    def create_widgets(self):
        # Frame đăng nhập
        self.frame = tk.Frame(self.root, bg="#f5f5f5")
        self.frame.pack(pady=50)

        # Label và Entry cho Tên Đăng Nhập
        self.username_label = tk.Label(self.frame, text="Username:", bg="#f5f5f5")
        self.username_label.grid(row=0, column=0, pady=10, sticky="e")
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Label và Entry cho Mật Khẩu
        self.password_label = tk.Label(self.frame, text="Password:", bg="#f5f5f5")
        self.password_label.grid(row=1, column=0, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        # Nút Đăng Nhập
        self.login_button = tk.Button(self.frame, text="Đăng Nhập", command=self.login, bg="#4CAF50", fg="white", relief="flat", width=15)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Nút Đăng Ký
        self.register_button = tk.Button(self.frame, text="Đăng Ký", command=self.register, bg="#FFC107", fg="white", relief="flat", width=15)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kiểm tra đăng nhập
        user = self.db_session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            self.root.destroy()  # Đóng cửa sổ đăng nhập
            self.open_main_app()  # Mở giao diện chính
        else:
            messagebox.showerror("Lỗi", "Sai username hoặc password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kiểm tra xem user đã tồn tại chưa
        user = self.db_session.query(User).filter_by(username=username).first()
        if user:
            messagebox.showerror("Lỗi", "Username đã tồn tại!")
            return
        
        # Thêm người dùng mới
        try:
            new_user = User(username=username, password=password)
            self.db_session.add(new_user)
            self.db_session.commit()
            messagebox.showinfo("Thông báo", "Đăng ký thành công!")
        except IntegrityError:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra khi đăng ký.")
            self.db_session.rollback()

    def open_main_app(self):
        # Mở cửa sổ chính sau khi đăng nhập thành công
        main_root = tk.Tk()
        app = SinhVienApp(main_root)
        main_root.mainloop()
class ChuyenNganhApp:
    def __init__(self, root, sinh_vien_app):
        self.root = root
        self.root.title("Quản lý Chuyên Ngành")
        self.root.geometry("800x500")
        self.db_manager = DatabaseManager()
        self.db_session = self.db_manager.get_session()
        self.sinh_vien_app = sinh_vien_app  # Giữ tham chiếu đến SinhVienApp
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Frame hiển thị danh sách chuyên ngành
        self.frame_treeview = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid")
        self.frame_treeview.pack(padx=20, pady=20, fill="both", expand=True)

        # Treeview để hiển thị danh sách chuyên ngành
        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Tên Chuyên Ngành"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên Chuyên Ngành", text="Tên Chuyên Ngành")

        # Cải thiện Treeview với Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Các nút chức năng
        self.frame_buttons = tk.Frame(self.root, bg="#f5f5f5")
        self.frame_buttons.pack(padx=20, pady=10)

        self.btn_add = tk.Button(self.frame_buttons, text="Thêm Chuyên Ngành", command=self.open_add_form, bg="#4CAF50", fg="white", relief="flat", width=15)
        self.btn_add.grid(row=0, column=0, padx=10)

    def load_data(self):
        # Lấy danh sách chuyên ngành và hiển thị lên giao diện
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        chuyen_nganhs = self.db_session.query(ChuyenNganh).all()
        for cn in chuyen_nganhs:
            self.tree.insert("", "end", values=(cn.ChuyenNganhID, cn.TenChuyenNganh))

    def open_add_form(self):
        AddChuyenNganhForm(self.root, self.db_session, self.load_data)


class AddChuyenNganhForm:
    def __init__(self, parent, db_session, reload_callback, chuyen_nganh=None):
        self.top = tk.Toplevel(parent)
        self.db_session = db_session
        self.reload_callback = reload_callback
        self.chuyen_nganh = chuyen_nganh

        self.top.title("Thêm/Sửa Chuyên Ngành")
        self.top.geometry("400x250")  # Tăng kích thước cửa sổ để đủ không gian
        self.top.configure(bg="#f5f5f5")

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho ID Chuyên Ngành
        self.id_label = tk.Label(self.top, text="ID Chuyên Ngành:", bg="#f5f5f5")
        self.id_label.grid(row=0, column=0, pady=10, sticky="e")
        self.id_entry = tk.Entry(self.top, width=30)
        self.id_entry.grid(row=0, column=1, pady=10)
        if self.chuyen_nganh:
            self.id_entry.insert(0, self.chuyen_nganh.ChuyenNganhID)

        # Label và Entry cho Tên Chuyên Ngành
        self.ten_label = tk.Label(self.top, text="Tên Chuyên Ngành:", bg="#f5f5f5")
        self.ten_label.grid(row=1, column=0, pady=10, sticky="e")
        self.ten_entry = tk.Entry(self.top, width=30)
        self.ten_entry.grid(row=1, column=1, pady=10)
        if self.chuyen_nganh:
            self.ten_entry.insert(0, self.chuyen_nganh.TenChuyenNganh)

        # Nút Lưu
        self.btn_save = tk.Button(self.top, text="Lưu", command=self.save_chuyen_nganh, bg="#4CAF50", fg="white", relief="flat", width=15)
        self.btn_save.grid(row=2, column=0, columnspan=2, pady=20)

    def save_chuyen_nganh(self):
        id_chuyen_nganh = self.id_entry.get()  # Lấy giá trị ID từ Entry (chỉ đọc)
        ten_chuyen_nganh = self.ten_entry.get()  # Lấy giá trị Tên chuyên ngành từ Entry

        # Kiểm tra dữ liệu nhập
        if not ten_chuyen_nganh:
            messagebox.showerror("Lỗi", "Tên chuyên ngành không được để trống.")
            return

        if self.chuyen_nganh:
            # Cập nhật chuyên ngành (chỉ cập nhật Tên chuyên ngành, không thay đổi ID)
            self.chuyen_nganh.TenChuyenNganh = ten_chuyen_nganh
            self.db_session.commit()
            messagebox.showinfo("Thông báo", "Chuyên ngành đã được cập nhật.")
        else:
            # Thêm mới chuyên ngành (tạo mới với ID và Tên chuyên ngành)
            new_chuyen_nganh = ChuyenNganh(ChuyenNganhID=id_chuyen_nganh, TenChuyenNganh=ten_chuyen_nganh)
            self.db_session.add(new_chuyen_nganh)
            self.db_session.commit()
            messagebox.showinfo("Thông báo", "Chuyên ngành đã được thêm mới.")
        
        # Tải lại dữ liệu danh sách chuyên ngành
        self.reload_callback()
        self.top.destroy()

# Khởi tạo ứng dụng chính
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginRegisterApp(root)
    root.mainloop()
