import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
import datetime

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý mượn sách thư viện")
        self.root.iconbitmap("book.ico")

        # Biến kết nối cơ sở dữ liệu
        self.db_name = tk.StringVar(value='QuanLyThuVien')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='5432')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='tbl_muonsach')

        # Biến quản lý mượn sách
        self.id = tk.StringVar()
        self.mssv = tk.StringVar()
        self.ten_sv = tk.StringVar()
        self.ten_sach = tk.StringVar()
        self.ngay_muon = tk.StringVar()
        self.ngay_tra = tk.StringVar()

        # Tạo giao diện
        self.create_widgets()
        self.create_menubar()

    def create_menubar(self):
        menubar = tk.Menu(self.root)

        # Menu Hệ thống
        system_menu = tk.Menu(menubar, tearoff=0)
        system_menu.add_command(label="Hướng dẫn", command=self.show_help)
        system_menu.add_separator()
        system_menu.add_command(label="Thoát", command=self.root.quit)

        # Thêm menu vào thanh menu chính
        menubar.add_cascade(label="Hệ thống", menu=system_menu)

        # Gắn thanh menu vào cửa sổ chính
        self.root.config(menu=menubar)

    def show_help(self):
        messagebox.showinfo(
            "Hướng dẫn sử dụng", 
            "1. Nhập thông tin sinh viên và sách.\n"
            "2. Chọn các chức năng Thêm, Xóa, Cập nhật hoặc Tìm kiếm.\n"
            "3. LƯU Ý: Kết nối cơ sở dữ liệu trước khi thực hiện các thao tác."
        )

    def create_widgets(self):
        # Frame kết nối database
        db_frame = tk.LabelFrame(self.root, text="Kết nối cơ sở dữ liệu")
        db_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(db_frame, text="Tên cơ sở dữ liệu:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(db_frame, text="Người dùng:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(db_frame, text="Mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(db_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(db_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(db_frame, text="Kết nối", command=self.connect_db).grid(row=5, columnspan=2, pady=10)
        
        tk.Label(db_frame, text="Tên bảng:").grid(row=6, column=0, padx=5, pady=5)
        tk.Entry(db_frame, textvariable=self.table_name).grid(row=6, column=1, padx=5, pady=5)

        tk.Button(db_frame, text="Tải cơ sở dữ liệu", command=self.load_data).grid(row=7, columnspan=2, pady=10)

        # Frame quản lý thư viện
        lib_frame = tk.LabelFrame(self.root, text="Quản lý mượn sách")
        lib_frame.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(lib_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.id).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(lib_frame, text="Mã sinh viên:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.mssv).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(lib_frame, text="Tên sinh viên:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.ten_sv).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(lib_frame, text="Tên sách:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.ten_sach).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(lib_frame, text="Ngày mượn:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.ngay_muon).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(lib_frame, text="Ngày trả:").grid(row=5, column=0, padx=5, pady=5)
        tk.Entry(lib_frame, textvariable=self.ngay_tra).grid(row=5, column=1, padx=5, pady=5)

        tk.Button(lib_frame, text="Thêm", command=self.insert_data).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(lib_frame, text="Xóa", command=self.delete_data).grid(row=6, column=1, padx=5, pady=5)
        tk.Button(lib_frame, text="Cập nhật", command=self.update_data).grid(row=7, column=0, padx=5, pady=5)
        tk.Button(lib_frame, text="Tìm kiếm", command=self.search_data).grid(row=7, column=1, padx=5, pady=5)
        tk.Button(lib_frame, text="Reset", command=self.reset_fields).grid(row=8, columnspan=2, pady=10)
        
        # Vùng hiển thị dữ liệu
        self.data_display_frame = tk.Frame(self.root)
        self.data_display_frame.grid(row=0, column=2, padx=10, pady=10)

        self.data_display = tk.Text(self.data_display_frame, height=20, width=100)
        self.data_display.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.data_display_frame, command=self.data_display.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.data_display.config(yscrollcommand=self.scrollbar.set)

    def reset_fields(self):
        """Xóa dữ liệu trong các ô nhập liệu."""
        self.id.set("")
        self.mssv.set("")
        self.ten_sv.set("")
        self.ten_sach.set("")
        self.ngay_muon.set("")
        self.ngay_tra.set("")
        self.data_display.delete(1.0, tk.END)  # Xóa vùng hiển thị dữ liệu

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành công", "Kết nối cơ sở dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
            self.conn.rollback()

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {table}").format(
                table=sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Xóa nội dung cũ trong Text widget
            self.data_display.delete(1.0, tk.END)

            if rows:
                # Duyệt qua từng hàng và định dạng ngày tháng
                for row in rows:
                    formatted_row = self.format_row(row)
                    self.data_display.insert(tk.END, f"{formatted_row}\n")
            else:
                messagebox.showinfo("Thông báo", "Không có dữ liệu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")
            self.conn.rollback()

    def insert_data(self):
        try:
            # Chuyển chuỗi thành datetime.date
            ngay_muon = datetime.datetime.strptime(self.ngay_muon.get(), '%d/%m/%Y').date()
            ngay_tra = datetime.datetime.strptime(self.ngay_tra.get(), '%d/%m/%Y').date()
            if ngay_tra < ngay_muon:
                messagebox.showerror("Lỗi", "Ngày trả không thể trước ngày mượn. Vui lòng nhập lại!")
                return
            # Thực hiện truy vấn SQL chèn dữ liệu
            query = sql.SQL("INSERT INTO {table} (mssv, ten_sv, ten_sach, ngay_muon, ngay_tra) VALUES (%s, %s, %s, %s, %s)").format(
                table=sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query, (self.mssv.get(), self.ten_sv.get(), self.ten_sach.get(), ngay_muon, ngay_tra))
            self.conn.commit()

            messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {e}")
            self.conn.rollback()

    def delete_data(self):
        try:
            query = sql.SQL("DELETE FROM {table} WHERE id = %s").format(
                table=sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query, (self.id.get(),))
            self.conn.commit()

            messagebox.showinfo("Thành công", "Xóa dữ liệu thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dữ liệu: {e}")
            self.conn.rollback()

    def update_data(self):
        try:
            ngay_muon = datetime.datetime.strptime(self.ngay_muon.get(), '%d/%m/%Y').date()
            ngay_tra = datetime.datetime.strptime(self.ngay_tra.get(), '%d/%m/%Y').date()

            query = sql.SQL("UPDATE {table} SET mssv = %s, ten_sv = %s, ten_sach = %s, ngay_muon = %s, ngay_tra = %s WHERE id = %s").format(
                table=sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query, (self.mssv.get(), self.ten_sv.get(), self.ten_sach.get(), ngay_muon, ngay_tra, self.id.get()))
            self.conn.commit()

            messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật dữ liệu: {e}")
            self.conn.rollback()

    def search_data(self):
        try:
            query = sql.SQL("SELECT * FROM {table} WHERE mssv = %s").format(
                table=sql.Identifier(self.table_name.get())
            )
            self.cur.execute(query, (self.mssv.get(),))
            rows = self.cur.fetchall()

            # Xóa vùng hiển thị và hiển thị kết quả
            self.data_display.delete(1.0, tk.END)
            if rows:
                # Duyệt qua từng hàng và hiển thị
                for row in rows:
                    formatted_row = self.format_row(row)
                    self.data_display.insert(tk.END, f"{formatted_row}\n")
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm dữ liệu: {e}")
            self.conn.rollback()

    def format_row(self, row):
        try:
            id, mssv, ten_sv, ten_sach, ngay_muon, ngay_tra = row
            formatted_ngay_muon = ngay_muon.strftime('%d/%m/%Y') if isinstance(ngay_muon, datetime.date) else ngay_muon
            formatted_ngay_tra = ngay_tra.strftime('%d/%m/%Y') if isinstance(ngay_tra, datetime.date) else ngay_tra
            return (
                f"ID: {id}, Mã SV: {mssv}, Tên SV: {ten_sv}, "
                f"Tên Sách: {ten_sach}\nNgày Mượn: {formatted_ngay_muon}, Ngày Trả: {formatted_ngay_tra}\n"
            )
        except ValueError:
            return "Dữ liệu không hợp lệ.\n"

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
