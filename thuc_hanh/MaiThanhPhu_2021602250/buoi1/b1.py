import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np

class EquationSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Giải hệ phương trình n ẩn")
        self.master.geometry("600x400")

        self.n = tk.StringVar(value="2")  # Default value
        self.A = []
        self.B = []
        self.result_vars = []

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Số phương trình/ẩn:").grid(column=0, row=0, sticky=tk.W)
        n_entry = ttk.Entry(main_frame, width=5, textvariable=self.n)
        n_entry.grid(column=1, row=0, sticky=tk.W)
        ttk.Button(main_frame, text="Cập nhật", command=self.validate_and_update).grid(column=2, row=0, sticky=tk.W)

        self.equation_frame = ttk.Frame(main_frame, padding="10")
        self.equation_frame.grid(column=0, row=1, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(main_frame, text="Giải hệ phương trình", command=self.solve_equation).grid(column=0, row=2, columnspan=3, pady=10)

        # Frame để chứa kết quả
        self.result_frame = ttk.Frame(main_frame, padding="10")
        self.result_frame.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Tạo một ô ScrolledText để hiển thị kết quả
        self.result_text = scrolledtext.ScrolledText(self.result_frame, width=50, height=5, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.result_text.config(state=tk.DISABLED)  # Không cho phép chỉnh sửa

        # Thêm nút "Thoát" dưới ô kết quả
        self.quit_button = ttk.Button(self.result_frame, text="Thoát", command=self.master.quit)
        self.quit_button.grid(row=1, column=0, pady=10)

        self.update_matrix()

    def validate_and_update(self):
        try:
            n = int(self.n.get())
            if n < 2:
                raise ValueError("Số phương trình/ẩn phải lớn hơn 1")
            self.update_matrix()
        except ValueError:
            messagebox.showerror("Lỗi", "Mời nhập đúng định dạng")

    def update_matrix(self):
        for widget in self.equation_frame.winfo_children():
            widget.destroy()

        n = int(self.n.get())
        self.A = []
        self.B = []

        ttk.Label(self.equation_frame, text="Ma trận A:").grid(row=0, column=0, columnspan=n, sticky=tk.W)
        ttk.Label(self.equation_frame, text="Vector B:").grid(row=0, column=n + 1, sticky=tk.W)

        for i in range(n):
            row = []
            for j in range(n):
                entry = ttk.Entry(self.equation_frame, width=5)
                entry.grid(row=i + 1, column=j, padx=2, pady=2)
                row.append(entry)
            self.A.append(row)

            # Thêm dấu bằng vào trước ô cuối cùng
            ttk.Label(self.equation_frame, text="=").grid(row=i + 1, column=n, padx=2, pady=2)

            # Ô nhập cho vector B
            b_entry = ttk.Entry(self.equation_frame, width=5)
            b_entry.grid(row=i + 1, column=n + 1, padx=2, pady=2)
            self.B.append(b_entry)

    def solve_equation(self):
        try:
            n = int(self.n.get())
            A = np.array([[float(entry.get()) for entry in row] for row in self.A])
            B = np.array([float(entry.get()) for entry in self.B])

            X = np.linalg.solve(A, B)

            # Cập nhật kết quả vào ô ScrolledText
            self.result_text.config(state=tk.NORMAL)  # Cho phép chỉnh sửa tạm thời
            self.result_text.delete(1.0, tk.END)  # Xóa nội dung cũ
            self.result_text.insert(tk.END, "Kết quả:\n")
            for i, x in enumerate(X):
                self.result_text.insert(tk.END, f"x{i + 1} = {x:.4f}\n")
            self.result_text.config(state=tk.DISABLED)  # Quay lại chế độ không chỉnh sửa

        except np.linalg.LinAlgError:
            messagebox.showerror("Lỗi", "Ma trận A không khả nghịch. Hệ phương trình có thể không có nghiệm hoặc có vô số nghiệm.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ các hệ số và đảm bảo chúng là số.")

def tao_ban_phim_so(root):
    """Tạo bàn phím số ở bên phải giao diện với các nút liền kề nhau và nút xóa hoạt động đúng"""
    main_frame = root.winfo_children()[0]  # Lấy main_frame đã tạo trong EquationSolver
    keypad_frame = tk.Frame(main_frame, borderwidth=1, relief='solid')
    keypad_frame.grid(row=1, column=3, rowspan=3, padx=2, sticky='n')

    keys = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['0', '.', '-'],
        ['Xóa']  # Nút Xóa nằm ở hàng thứ 5
    ]

    def backspace():
        """Hàm xóa ký tự cuối cùng trong ô nhập đang được chọn"""
        selected_widget = root.focus_get()
        if isinstance(selected_widget, tk.Entry):
            current_text = selected_widget.get()
            selected_widget.delete(0, tk.END)
            selected_widget.insert(0, current_text[:-1])
        elif isinstance(selected_widget, scrolledtext.ScrolledText):
            current_pos = selected_widget.index(tk.INSERT)
            if current_pos != "1.0":
                prev_pos = selected_widget.index(f"{current_pos}-1c")
                selected_widget.delete(prev_pos, current_pos)

    def insert_to_entry(value):
        """Chèn ký tự vào vị trí con trỏ trong ô nhập hiện đang chọn"""
        selected_widget = root.focus_get()
        if isinstance(selected_widget, tk.Entry) or isinstance(selected_widget, scrolledtext.ScrolledText):
            cursor_position = selected_widget.index(tk.INSERT)
            selected_widget.insert(cursor_position, value)

    # Tạo các nút số và các ký tự
    for row, key_row in enumerate(keys):
        for col, key in enumerate(key_row):
            if key == "Xóa":
                btn = tk.Button(keypad_frame, text=key, command=backspace, width=12, height=2)  # Nút "Xóa" dài 3 ô
                # Đặt nút "Xóa" ở hàng thứ 5 (row=4) và kéo dài qua 3 cột
                btn.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=0, pady=0)
            else:
                btn = tk.Button(keypad_frame, text=key, command=lambda k=key: insert_to_entry(k), width=4, height=2)
                btn.grid(row=row, column=col, sticky='nsew', padx=0, pady=0)

    # Đảm bảo tất cả các cột trong bàn phím đều có chiều rộng tương đương
    for i in range(len(keys[0])):
        keypad_frame.grid_columnconfigure(i, weight=1)
    for i in range(len(keys)):
        keypad_frame.grid_rowconfigure(i, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolver(root)
    tao_ban_phim_so(root)
    root.mainloop()