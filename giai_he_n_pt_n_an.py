import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class EquationSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Giải hệ phương trình n ẩn")
        self.master.geometry("600x400")

        self.n = tk.StringVar(value="2")  # Changed to StringVar
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

        self.result_frame = ttk.Frame(main_frame, padding="10")
        self.result_frame.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

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
        ttk.Label(self.equation_frame, text="Vector B:").grid(row=0, column=n, sticky=tk.W)

        for i in range(n):
            row = []
            for j in range(n):
                entry = ttk.Entry(self.equation_frame, width=5)
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                row.append(entry)
            self.A.append(row)

            b_entry = ttk.Entry(self.equation_frame, width=5)
            b_entry.grid(row=i+1, column=n, padx=2, pady=2)
            self.B.append(b_entry)

    def solve_equation(self):
        try:
            n = self.n.get()
            A = np.array([[float(entry.get()) for entry in row] for row in self.A])
            B = np.array([float(entry.get()) for entry in self.B])

            X = np.linalg.solve(A, B)

            for widget in self.result_frame.winfo_children():
                widget.destroy()

            ttk.Label(self.result_frame, text="Kết quả:").grid(row=0, column=0, sticky=tk.W)
            for i, x in enumerate(X):
                ttk.Label(self.result_frame, text=f"x{i+1} = {x:.4f}").grid(row=i+1, column=0, sticky=tk.W)

        except np.linalg.LinAlgError:
            messagebox.showerror("Lỗi", "Ma trận A không khả nghịch. Hệ phương trình có thể không có nghiệm hoặc có vô số nghiệm.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ các hệ số và đảm bảo chúng là số.")
    # Rest of the code remains the same...

if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolver(root)
    root.mainloop()
