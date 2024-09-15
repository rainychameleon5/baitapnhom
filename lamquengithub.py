import numpy as np
import tkinter as tk
from tkinter import messagebox


class MaTranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tính toán Ma trận")

        # Khung nhập cho ma trận A
        self.label_a = tk.Label(root, text="Nhập Ma trận A:")
        self.label_a.grid(row=0, column=0)

        self.entries_a = self.create_matrix_entries(3, 3, 1, 0)

        # Khung nhập cho ma trận B
        self.label_b = tk.Label(root, text="Nhập Ma trận B:")
        self.label_b.grid(row=5, column=0)

        self.entries_b = self.create_matrix_entries(3, 3, 6, 0)

        # Các nút tính toán
        self.tinh_tong_btn = tk.Button(root, text="Tính Tổng", command=self.tinh_tong)
        self.tinh_tong_btn.grid(row=10, column=0)

        self.tinh_tich_btn = tk.Button(root, text="Tính Tích", command=self.tinh_tich)
        self.tinh_tich_btn.grid(row=10, column=1)

        self.dinh_thuc_btn = tk.Button(root, text="Định Thức A", command=self.tinh_dinh_thuc_a)
        self.dinh_thuc_btn.grid(row=10, column=2)

        self.dinh_thuc_b_btn = tk.Button(root, text="Định Thức B", command=self.tinh_dinh_thuc_b)
        self.dinh_thuc_b_btn.grid(row=10, column=3)

        # Khung hiển thị kết quả
        self.result_label = tk.Label(root, text="Kết quả:")
        self.result_label.grid(row=11, column=0, columnspan=4)
        self.result_text = tk.Text(root, height=5, width=40)
        self.result_text.grid(row=12, column=0, columnspan=4)

    def create_matrix_entries(self, rows, cols, start_row, start_col):
        entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = tk.Entry(self.root, width=5)
                entry.grid(row=start_row + i, column=start_col + j)
                row_entries.append(entry)
            entries.append(row_entries)
        return entries

    def get_matrix_from_entries(self, entries):
        try:
            matrix = []
            for row_entries in entries:
                row = [float(entry.get()) for entry in row_entries]
                matrix.append(row)
            return np.array(matrix)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho ma trận!")
            return None

    def tinh_tong(self):
        ma_tran_a = self.get_matrix_from_entries(self.entries_a)
        ma_tran_b = self.get_matrix_from_entries(self.entries_b)

        if ma_tran_a is None or ma_tran_b is None:
            return

        if ma_tran_a.shape != ma_tran_b.shape:
            messagebox.showerror("Lỗi", "Hai ma trận phải cùng kích thước để tính tổng!")
            return

        tong = np.add(ma_tran_a, ma_tran_b)
        self.show_result(tong)

    def tinh_tich(self):
        ma_tran_a = self.get_matrix_from_entries(self.entries_a)
        ma_tran_b = self.get_matrix_from_entries(self.entries_b)

        if ma_tran_a is None or ma_tran_b is None:
            return

        if ma_tran_a.shape[1] != ma_tran_b.shape[0]:
            messagebox.showerror("Lỗi", "Số cột của A phải bằng số hàng của B để tính tích!")
            return

        tich = np.dot(ma_tran_a, ma_tran_b)
        self.show_result(tich)

    def tinh_dinh_thuc_a(self):
        ma_tran_a = self.get_matrix_from_entries(self.entries_a)

        if ma_tran_a is None:
            return

        if ma_tran_a.shape[0] != ma_tran_a.shape[1]:
            messagebox.showerror("Lỗi", "Ma trận A phải là ma trận vuông để tính định thức!")
            return

        dinh_thuc = np.linalg.det(ma_tran_a)
        self.show_result(dinh_thuc)

    def tinh_dinh_thuc_b(self):
        ma_tran_b = self.get_matrix_from_entries(self.entries_b)

        if ma_tran_b is None:
            return

        if ma_tran_b.shape[0] != ma_tran_b.shape[1]:
            messagebox.showerror("Lỗi", "Ma trận B phải là ma trận vuông để tính định thức!")
            return

        dinh_thuc = np.linalg.det(ma_tran_b)
        self.show_result(dinh_thuc)

    def show_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))
    def show_result(self, result):
    self.result_text.delete(1.0, tk.END)
    
    # Nếu kết quả là một số, kiểm tra xem nó có phải gần bằng 0 hay không
    if isinstance(result, (int, float)) and np.isclose(result, 0):
        messagebox.showwarning("Cảnh báo", "Kết quả gần bằng 0.")
    
    # Nếu kết quả là một ma trận, kiểm tra xem có phần tử nào không xác định không
    if isinstance(result, np.ndarray):
        if np.isnan(result).any():
            messagebox.showerror("Lỗi", "Kết quả chứa giá trị không xác định (NaN).")
        elif np.isclose(result, 0).all():
            messagebox.showwarning("Cảnh báo", "Kết quả là ma trận gần như rỗng.")
    
    self.result_text.insert(tk.END, str(result))



if __name__ == "__main__":
    root = tk.Tk()
    app = MaTranApp(root)
    root.mainloop()
    print("Done")
    print("Done")
