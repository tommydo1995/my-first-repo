# Giao diện ứng dụng quản lý công việc
import tkinter as tk
from tkinter import ttk, messagebox
from todo import TodoList
import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Công Việc")
        
        # Cấu hình để cửa sổ có thể thay đổi kích thước
        self.root.resizable(True, True)
        
        # Đặt kích thước tối thiểu cho cửa sổ
        self.root.minsize(600, 400)
        
        # Cấu hình grid weight để các frame có thể mở rộng
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Khởi tạo TodoList
        self.todo = TodoList()
        
        # Tạo giao diện
        self.create_gui()
        
        # Load dữ liệu
        self.load_tasks()

    def create_gui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid weight cho main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)  # Cột trái rộng hơn
        main_frame.grid_columnconfigure(1, weight=1)  # Cột phải hẹp hơn
        
        # Frame bên trái cho danh sách công việc
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid weight cho left_frame
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview để hiển thị danh sách công việc
        columns = ('ID', 'Tên công việc', 'Mô tả', 'Trạng thái', 'Cập nhật')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings')
        
        # Định dạng cột
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tên công việc', text='Tên công việc')
        self.tree.heading('Mô tả', text='Mô tả')
        self.tree.heading('Trạng thái', text='Trạng thái')
        self.tree.heading('Cập nhật', text='Cập nhật')
        
        # Định dạng cột với tỷ lệ phần trăm của cửa sổ
        self.tree.column('ID', width=50, minwidth=50)
        self.tree.column('Tên công việc', width=200, minwidth=150)
        self.tree.column('Mô tả', width=250, minwidth=200)
        self.tree.column('Trạng thái', width=100, minwidth=80)
        self.tree.column('Cập nhật', width=150, minwidth=120)
        
        # Thanh cuộn
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí Treeview và thanh cuộn
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Frame bên phải cho các nút điều khiển
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid cho right_frame
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Các widget nhập liệu
        input_frame = ttk.LabelFrame(right_frame, text="Thêm công việc mới", padding="5")
        input_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        input_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(input_frame, text="Tên công việc:").grid(row=0, column=0, pady=5, sticky=tk.W)
        self.ten_entry = ttk.Entry(input_frame)
        self.ten_entry.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(input_frame, text="Mô tả:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.mo_ta_entry = ttk.Entry(input_frame)
        self.mo_ta_entry.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Các nút chức năng
        ttk.Button(right_frame, text="Thêm công việc", command=self.them_viec).grid(row=4, column=0, pady=5)
        ttk.Button(right_frame, text="Đánh dấu hoàn thành", command=self.danh_dau_hoan_thanh).grid(row=5, column=0, pady=5)
        ttk.Button(right_frame, text="Xóa công việc", command=self.xoa_viec).grid(row=6, column=0, pady=5)
        
        # Frame cho bộ lọc và thống kê
        filter_frame = ttk.LabelFrame(right_frame, text="Bộ lọc", padding="5")
        filter_frame.grid(row=7, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="Tất cả", variable=self.filter_var, 
                       value="all", command=self.load_tasks).grid(row=0, column=0)
        ttk.Radiobutton(filter_frame, text="Hoàn thành", variable=self.filter_var,
                       value="completed", command=self.load_tasks).grid(row=0, column=1)
        ttk.Radiobutton(filter_frame, text="Chưa hoàn thành", variable=self.filter_var,
                       value="pending", command=self.load_tasks).grid(row=0, column=2)
        
        # Frame thống kê
        stats_frame = ttk.LabelFrame(right_frame, text="Thống kê", padding="5")
        stats_frame.grid(row=8, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.stats_label = ttk.Label(stats_frame, text="")
        self.stats_label.grid(row=0, column=0)
        
        # Nút sao lưu
        ttk.Button(right_frame, text="Sao lưu dữ liệu", command=self.sao_luu).grid(row=9, column=0, pady=5)

    def load_tasks(self):
        # Xóa dữ liệu cũ trong tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lọc và hiển thị dữ liệu
        for task in self.todo.tasks:
            if (self.filter_var.get() == "all" or 
                (self.filter_var.get() == "completed" and task['hoan_thanh']) or
                (self.filter_var.get() == "pending" and not task['hoan_thanh'])):
                
                trang_thai = "✓" if task['hoan_thanh'] else "✗"
                cap_nhat = task.get('cap_nhat', '')
                
                self.tree.insert('', 'end', values=(
                    task['id'],
                    task['ten'],
                    task['mo_ta'],
                    trang_thai,
                    cap_nhat
                ))
        
        # Cập nhật thống kê
        self.update_statistics()

    def them_viec(self):
        ten = self.ten_entry.get().strip()
        mo_ta = self.mo_ta_entry.get().strip()
        
        if not ten:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên công việc!")
            return
        
        self.todo.them_viec(ten, mo_ta)
        self.ten_entry.delete(0, tk.END)
        self.mo_ta_entry.delete(0, tk.END)
        self.load_tasks()

    def danh_dau_hoan_thanh(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc!")
            return
        
        task_id = int(self.tree.item(selected_item[0])['values'][0])
        self.todo.danh_dau_hoan_thanh(task_id)
        self.load_tasks()

    def xoa_viec(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một công việc!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa công việc này?"):
            task_id = int(self.tree.item(selected_item[0])['values'][0])
            self.todo.xoa_viec(task_id)
            self.load_tasks()

    def update_statistics(self):
        stats = self.todo.storage.get_statistics()
        stats_text = f"Tổng số: {stats['tong_so']}\n"
        stats_text += f"Hoàn thành: {stats['da_hoan_thanh']}\n"
        stats_text += f"Chưa hoàn thành: {stats['chua_hoan_thanh']}\n"
        stats_text += f"Tỷ lệ: {stats['ty_le_hoan_thanh']}"
        self.stats_label.configure(text=stats_text)

    def sao_luu(self):
        self.todo.sao_luu()
        messagebox.showinfo("Thông báo", "Đã tạo bản sao lưu thành công!")

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
