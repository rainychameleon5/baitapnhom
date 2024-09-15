import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


def lay_phan_tu_ma_tran(hang, cot):
  """Hàm để nhập các phần tử và kiểm tra định dạng đúng."""
  while True:
    try:
      print(f"Nhập các phần tử cho ma trận dạng mảng 1 chiều (phải có {hang * cot} phần tử):")
      phantu = list(map(float, input().split()))
      if len(phantu) != hang * cot:
        print(f"Số lượng phần tử phải là {hang * cot}, nhưng bạn đã nhập {len(phantu)} phần tử.Mời nhập lại")
        continue  # Lắp lại việc nhập khi sai số lượng
      return np.array(phantu).reshape(hang, cot)
    except ValueError:
      print(f"Lỗi không đúng định dạng. Vui lòng nhập lại.")


def dinh_thuc_ma_tran(matran):
  """Tính định thức"""
  try:
    if matran.shape[0] != matran.shape[1]:
      raise ValueError("Ma trận vuông mới có thể tính định thức")
    dinh_thuc = np.linalg.det(matran)
    return dinh_thuc
  except np.linalg.LinAlgError:
    raise ValueError("Ma trận không thể tính định thức")


def nghich_dao_ma_tran(matran):
  """Tính nghịch đảo"""
  try:
    if matran.shape[0] != matran.shape[1]:
      raise ValueError("Ma trận vuông mới có thể tính nghịch đảo")
    nghich_dao = np.linalg.inv(matran)  # Tính nghịch đảo
    return nghich_dao
  except np.linalg.LinAlgError:  # Khi không có nghịch đảo, numpy sinh lỗi np.linalg.LinAlgError
    raise ValueError("Ma trận không khả nghịch.")


class MatrixOperationsGUI:
  def __init__(self, master):
    self.master = master
    self.master.title("Matrix Operations")
    self.master.geometry("800x600")

    self.matrices = []
    self.create_widgets()

  def create_widgets(self):
    # nhap matran
    input_frame = ttk.LabelFrame(self.master, text="Nhập Ma Trận")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Số hàng:").grid(row=0, column=0, padx=5, pady=5)
    self.rows_entry = ttk.Entry(input_frame, width=5)
    self.rows_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Số cột:").grid(row=0, column=2, padx=5, pady=5)
    self.cols_entry = ttk.Entry(input_frame, width=5)
    self.cols_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Các phần tử (cách nhau bởi dấu cách):").grid(row=1, column=0, columnspan=2, padx=5,
                                                                              pady=5)
    self.elements_entry = ttk.Entry(input_frame, width=50)
    self.elements_entry.grid(row=1, column=2, columnspan=3, padx=5, pady=5)

    ttk.Button(input_frame, text="Thêm Ma Trận", command=self.add_matrix).grid(row=2, column=0, columnspan=5, pady=10)

    # hienthi
    display_frame = ttk.LabelFrame(self.master, text="Các Ma Trận")
    display_frame.pack(padx=10, pady=10, fill="both", expand=True)

    self.matrix_display = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, width=60, height=10)
    self.matrix_display.pack(padx=5, pady=5, fill="both", expand=True)

    # phep toan
    operations_frame = ttk.LabelFrame(self.master, text="Các Phép Toán")
    operations_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(operations_frame, text="Cộng Ma Trận", command=self.add_matrices).pack(side=tk.LEFT, padx=5, pady=5)
    ttk.Button(operations_frame, text="Nhân Ma Trận", command=self.multiply_matrices).pack(side=tk.LEFT, padx=5, pady=5)
    ttk.Button(operations_frame, text="Tính Định Thức", command=self.calculate_determinants).pack(side=tk.LEFT, padx=5,
                                                                                                  pady=5)
    ttk.Button(operations_frame, text="Tính Ma Trận Nghịch Đảo", command=self.calculate_inverses).pack(side=tk.LEFT,
                                                                                                       padx=5, pady=5)

    # ketqua
    results_frame = ttk.LabelFrame(self.master, text="Kết Quả")
    results_frame.pack(padx=10, pady=10, fill="both", expand=True)

    self.results_display = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=60, height=10)
    self.results_display.pack(padx=5, pady=5, fill="both", expand=True)

  def add_matrix(self):
    try:
      hang = int(self.rows_entry.get())
      cot = int(self.cols_entry.get())
      phantu = list(map(float, self.elements_entry.get().split()))

      if len(phantu) != hang * cot:
        raise ValueError(f"Số lượng phần tử phải là {hang * cot}, nhưng bạn đã nhập {len(phantu)} phần tử.")

      matran = np.array(phantu).reshape(hang, cot)
      self.matrices.append(matran)
      self.update_matrix_display()
      self.clear_input_fields()
    except ValueError as e:
      messagebox.showerror("Lỗi Nhập","Cần nhập các phần tử")

  def update_matrix_display(self):
    self.matrix_display.delete(1.0, tk.END)
    for i, matran in enumerate(self.matrices):
      self.matrix_display.insert(tk.END, f"Ma trận {i + 1}:\n{matran}\n\n")

  def clear_input_fields(self):
    self.rows_entry.delete(0, tk.END)
    self.cols_entry.delete(0, tk.END)
    self.elements_entry.delete(0, tk.END)

  # phép nhân
  def multiply_matrices(self):
    if len(self.matrices) < 2:
      messagebox.showwarning("Cảnh báo", "Cần ít nhất hai ma trận để thực hiện phép nhân.")
      return

    try:
      kqua_nhan = self.matrices[0]
      for matran in self.matrices[1:]:
        if kqua_nhan.shape[1] != matran.shape[0]:
          raise ValueError("Số cột của ma trận trước không bằng số hàng của ma trận sau.")
        kqua_nhan = np.dot(kqua_nhan, matran)
      self.display_result("Kết quả của phép nhân các ma trận", kqua_nhan)
    except ValueError as e:
      messagebox.showerror("Lỗi", str(e))

  #phép tổng
  def add_matrices(self):
    if len(self.matrices) < 2:
      messagebox.showwarning("Cảnh báo", "Cần ít nhất hai ma trận để thực hiện phép cộng.")
      return

    try:
      kich_thuoc_dong_nhat = all(mat.shape == self.matrices[0].shape for mat in self.matrices)
      if not kich_thuoc_dong_nhat:
        raise ValueError("Không thể thực hiện phép cộng vì các ma trận có kích thước khác nhau.")

      tong_matran = np.sum(self.matrices, axis=0)
      self.display_result("Tổng của các ma trận", tong_matran)
    except ValueError as e:
      messagebox.showerror("Lỗi", str(e))


  #định thức
  def calculate_determinants(self):
    results = []
    for i, matran in enumerate(self.matrices):
      try:
        dinhthuc = dinh_thuc_ma_tran(matran)
        results.append(f"Định thức ma trận {i + 1}: {dinhthuc}")
      except ValueError as e:
        results.append(f"Không tính được định thức cho ma trận {i + 1}: {str(e)}")
    self.display_result("Định thức của các ma trận", "\n".join(results))

  #nghịch đảo
  def calculate_inverses(self):
    results = []
    for i, matran in enumerate(self.matrices):
      try:
        nghichdao = nghich_dao_ma_tran(matran)
        results.append(f"Nghịch đảo ma trận {i + 1}:\n{nghichdao}\n")
      except ValueError as e:
        results.append(f"Không có ma trận nghịch đảo cho ma trận {i + 1}: {str(e)}")
    self.display_result("Ma trận nghịch đảo", "\n".join(results))

  def display_result(self, title, result):
    self.results_display.delete(1.0, tk.END)
    self.results_display.insert(tk.END, f"{title}:\n{result}")


if __name__ == "__main__":
  root = tk.Tk()
  app = MatrixOperationsGUI(root)
  root.mainloop()
