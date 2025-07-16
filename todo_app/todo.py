# Quản lý danh sách việc cần làm (Todo List)
from storage import Storage

class TodoList:
    def __init__(self, storage_file="todo_data.json"):
        """
        Khởi tạo danh sách công việc
        
        Args:
            storage_file (str): Tên file để lưu trữ dữ liệu
        """
        self.storage = Storage(storage_file)
        self.tasks = self.storage.load_data()  # Đọc dữ liệu từ file nếu có

    def them_viec(self, ten_viec, mo_ta="", trang_thai=False):
        """
        Thêm một việc mới vào danh sách
        
        Args:
            ten_viec (str): Tên công việc
            mo_ta (str): Mô tả chi tiết về công việc (mặc định: chuỗi rỗng)
            trang_thai (bool): Trạng thái hoàn thành (mặc định: False - chưa hoàn thành)
        """
        task = {
            'id': len(self.tasks) + 1,
            'ten': ten_viec,
            'mo_ta': mo_ta,
            'hoan_thanh': trang_thai
        }
        self.tasks.append(task)
        self.storage.save_data(self.tasks)
        print(f"Đã thêm công việc: {ten_viec}")

    def xoa_viec(self, id_viec):
        """
        Xóa một việc khỏi danh sách theo ID
        
        Args:
            id_viec (int): ID của công việc cần xóa
        """
        for task in self.tasks:
            if task['id'] == id_viec:
                self.tasks.remove(task)
                self.storage.save_data(self.tasks)
                print(f"Đã xóa công việc có ID: {id_viec}")
                return
        print(f"Không tìm thấy công việc có ID: {id_viec}")

    def danh_dau_hoan_thanh(self, id_viec):
        """
        Đánh dấu một việc là đã hoàn thành
        
        Args:
            id_viec (int): ID của công việc cần đánh dấu
        """
        for task in self.tasks:
            if task['id'] == id_viec:
                task['hoan_thanh'] = True
                self.storage.save_data(self.tasks)
                print(f"Đã đánh dấu hoàn thành công việc: {task['ten']}")
                return
        print(f"Không tìm thấy công việc có ID: {id_viec}")

    def hien_thi_danh_sach(self):
        """Hiển thị toàn bộ danh sách công việc"""
        if not self.tasks:
            print("Danh sách công việc trống!")
            return

        print("\nDANH SÁCH CÔNG VIỆC:")
        print("ID | Tên công việc | Trạng thái | Mô tả")
        print("-" * 50)
        for task in self.tasks:
            trang_thai = "✓" if task['hoan_thanh'] else "✗"
            print(f"{task['id']} | {task['ten']} | {trang_thai} | {task['mo_ta']}")

    def loc_theo_trang_thai(self, hoan_thanh=True):
        """
        Lọc và hiển thị công việc theo trạng thái
        
        Args:
            hoan_thanh (bool): True để lọc việc đã hoàn thành, False để lọc việc chưa hoàn thành
        """
        filtered_tasks = [task for task in self.tasks if task['hoan_thanh'] == hoan_thanh]
        if not filtered_tasks:
            trang_thai = "đã" if hoan_thanh else "chưa"
            print(f"Không có công việc nào {trang_thai} hoàn thành!")
            return

        print(f"\nDANH SÁCH CÔNG VIỆC {'ĐÃ' if hoan_thanh else 'CHƯA'} HOÀN THÀNH:")
        print("ID | Tên công việc | Mô tả")
        print("-" * 40)
        for task in filtered_tasks:
            print(f"{task['id']} | {task['ten']} | {task['mo_ta']}")

# Thêm các phương thức mới
    def sao_luu(self):
        """Tạo bản sao lưu dữ liệu"""
        self.storage.backup_data()

    def xem_thong_ke(self):
        """Hiển thị thống kê về công việc"""
        stats = self.storage.get_statistics()
        print("\nTHỐNG KÊ CÔNG VIỆC:")
        print(f"Tổng số công việc: {stats['tong_so']}")
        print(f"Đã hoàn thành: {stats['da_hoan_thanh']}")
        print(f"Chưa hoàn thành: {stats['chua_hoan_thanh']}")
        print(f"Tỷ lệ hoàn thành: {stats['ty_le_hoan_thanh']}")

# Ví dụ sử dụng:
if __name__ == "__main__":
    todo = TodoList()
    
    while True:
        print("\n=== QUẢN LÝ CÔNG VIỆC ===")
        print("1. Thêm công việc mới")
        print("2. Xem danh sách công việc")
        print("3. Đánh dấu hoàn thành")
        print("4. Xóa công việc")
        print("5. Xem công việc đã hoàn thành")
        print("6. Xem công việc chưa hoàn thành")
        print("7. Xem thống kê")
        print("8. Tạo bản sao lưu")
        print("0. Thoát")
        
        choice = input("\nChọn chức năng (0-8): ")
        
        if choice == "1":
            ten = input("Nhập tên công việc: ")
            mo_ta = input("Nhập mô tả công việc: ")
            todo.them_viec(ten, mo_ta)
        
        elif choice == "2":
            todo.hien_thi_danh_sach()
        
        elif choice == "3":
            todo.hien_thi_danh_sach()
            try:
                id_viec = int(input("Nhập ID công việc cần đánh dấu hoàn thành: "))
                todo.danh_dau_hoan_thanh(id_viec)
            except ValueError:
                print("ID không hợp lệ!")
        
        elif choice == "4":
            todo.hien_thi_danh_sach()
            try:
                id_viec = int(input("Nhập ID công việc cần xóa: "))
                todo.xoa_viec(id_viec)
            except ValueError:
                print("ID không hợp lệ!")
        
        elif choice == "5":
            todo.loc_theo_trang_thai(True)
        
        elif choice == "6":
            todo.loc_theo_trang_thai(False)
        
        elif choice == "7":
            todo.xem_thong_ke()
        
        elif choice == "8":
            todo.sao_luu()
        
        elif choice == "0":
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
        
        else:
            print("Lựa chọn không hợp lệ!")
