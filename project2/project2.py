import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Danh Sách Sinh Viên")

        # Database connection fields
        self.db_name = tk.StringVar(value='Project2')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='pokemon@')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Create the tabs
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        # Tab 1: Connection
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="Kết nối")
        self.create_connection_widgets(tab1)

        # Tab 2: Data Operations
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text="Quản lý danh sách")
        self.create_data_widgets(tab2)

        tab_control.pack(expand=1, fill="both")

    def create_connection_widgets(self, frame):
        connection_frame = ttk.Frame(frame)
        connection_frame.pack(pady=10)

        ttk.Label(connection_frame, text="Tên DB:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

    def create_data_widgets(self, frame):
        query_frame = ttk.Frame(frame)
        query_frame.pack(pady=10)

        ttk.Label(query_frame, text="Tên Bảng:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(query_frame, text="Tải dữ liệu", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        # Treeview for displaying data
        self.tree = ttk.Treeview(frame, columns=("MSSV", "HoTen", "GioiTinh", "Lop"), show="headings", height=10)
        self.tree.heading("MSSV", text="Mã số SV")
        self.tree.heading("HoTen", text="Họ tên SV")
        self.tree.heading("GioiTinh", text="Giới tính")
        self.tree.heading("Lop", text="Lớp")
        self.tree.pack(pady=10)

        # Insert section
        insert_frame = ttk.Frame(frame)
        insert_frame.pack(pady=10)

        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.gender = tk.StringVar()
        self.class_name = tk.StringVar()

        ttk.Label(insert_frame, text="Mã số SV:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.student_id).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(insert_frame, text="Họ tên SV:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.student_name).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(insert_frame, text="Giới tính:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.gender).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(insert_frame, text="Lớp:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.class_name).grid(row=3, column=1, padx=5, pady=5)

        # Buttons for Insert and Delete
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Thêm Sinh Viên", command=self.insert_data).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Xóa Sinh Viên", command=self.delete_data).grid(row=0, column=1, padx=5)

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
            messagebox.showinfo("Success", "Kết nối vào Database thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi kết nối vào Database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            
            # Xóa dữ liệu cũ trong Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Hiển thị dữ liệu mới trong Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi tải dữ liệu: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (masosv, hotensv, gioitinh, lop) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.student_id.get(), self.student_name.get(), self.gender.get(), self.class_name.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Success", "Đã thêm sinh viên thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi thêm dữ liệu: {e}")

    def delete_data(self):
        try:
            # Get the selected item from the Treeview
            selected_item = self.tree.selection()
            
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
                return

            # Get the student ID from the selected row and convert to string
            student_id = str(self.tree.item(selected_item)['values'][0])

            # Confirm deletion
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên có mã số {student_id} không?")
            
            if confirm:
                # Prepare and execute delete query
                delete_query = sql.SQL("DELETE FROM {} WHERE masosv = %s").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(delete_query, (student_id,))
                self.conn.commit()
                
                # Reload data and show success message
                self.load_data()
                messagebox.showinfo("Success", f"Đã xóa sinh viên có mã số {student_id} thành công!")

        except Exception as e:
            messagebox.showerror("Error", f"Lỗi xóa dữ liệu: {e}")
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()