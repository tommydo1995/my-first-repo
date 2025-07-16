# Xử lý lưu trữ dữ liệu cho ứng dụng Todo List
import json
import os
from datetime import datetime

class Storage:
    def __init__(self, file_path="todo_data.json"):
        """
        Khởi tạo đối tượng Storage để lưu trữ dữ liệu

        Args:
            file_path (str): Đường dẫn đến file lưu trữ (mặc định: todo_data.json)
        """
        self.file_path = file_path
        self.ensure_storage_file()

    def ensure_storage_file(self):
        """Tạo file lưu trữ nếu chưa tồn tại"""
        if not os.path.exists(self.file_path):
            self.save_data([])

    def save_data(self, tasks):
        """
        Lưu danh sách công việc vào file

        Args:
            tasks (list): Danh sách các công việc cần lưu
        """
        try:
            # Thêm thời gian cập nhật cho mỗi task
            for task in tasks:
                if 'cap_nhat' not in task:
                    task['cap_nhat'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
            print("Đã lưu dữ liệu thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {str(e)}")

    def load_data(self):
        """
        Đọc danh sách công việc từ file

        Returns:
            list: Danh sách các công việc đã lưu
        """
        try:
            if not os.path.exists(self.file_path):
                return []

            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            print("Lỗi: File dữ liệu không đúng định dạng JSON")
            return []
        except Exception as e:
            print(f"Lỗi khi đọc dữ liệu: {str(e)}")
            return []

    def backup_data(self):
        """Tạo bản sao lưu của file dữ liệu"""
        try:
            if not os.path.exists(self.file_path):
                print("Không có dữ liệu để sao lưu!")
                return

            # Tạo tên file backup với timestamp
            backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(self.file_path, 'r', encoding='utf-8') as source:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            
            print(f"Đã tạo bản sao lưu tại: {backup_path}")
        except Exception as e:
            print(f"Lỗi khi sao lưu dữ liệu: {str(e)}")

    def get_statistics(self):
        """
        Lấy thống kê về dữ liệu công việc

        Returns:
            dict: Từ điển chứa các thống kê
        """
        tasks = self.load_data()
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get('hoan_thanh', False))
        pending_tasks = total_tasks - completed_tasks

        return {
            'tong_so': total_tasks,
            'da_hoan_thanh': completed_tasks,
            'chua_hoan_thanh': pending_tasks,
            'ty_le_hoan_thanh': f"{(completed_tasks/total_tasks)*100:.1f}%" if total_tasks > 0 else "0%"
        }

# Ví dụ sử dụng:
if __name__ == "__main__":
    # Khởi tạo đối tượng storage
    storage = Storage()

    # Ví dụ về dữ liệu mẫu
    sample_tasks = [
        {
            'id': 1,
            'ten': 'Học Python',
            'mo_ta': 'Học lập trình Python cơ bản',
            'hoan_thanh': False
        },
        {
            'id': 2,
            'ten': 'Làm bài tập',
            'mo_ta': 'Hoàn thành bài tập về nhà',
            'hoan_thanh': True
        }
    ]

    # Lưu dữ liệu mẫu
    storage.save_data(sample_tasks)

    # Đọc và hiển thị dữ liệu
    loaded_tasks = storage.load_data()
    print("\nDữ liệu đã đọc:")
    for task in loaded_tasks:
        print(f"ID: {task['id']}, Tên: {task['ten']}, Hoàn thành: {'✓' if task['hoan_thanh'] else '✗'}")

    # Tạo bản sao lưu
    storage.backup_data()

    # Hiển thị thống kê
    stats = storage.get_statistics()
    print("\nThống kê:")
    print(f"Tổng số công việc: {stats['tong_so']}")
    print(f"Đã hoàn thành: {stats['da_hoan_thanh']}")
    print(f"Chưa hoàn thành: {stats['chua_hoan_thanh']}")
    print(f"Tỷ lệ hoàn thành: {stats['ty_le_hoan_thanh']}")
