import tkinter as tk
from tkinter import ttk


def decimal_to_base(n, base):
  """Chuyển đổi từ hệ thập phân (decimal) sang hệ cơ số khác."""
  if n == 0:
    return "0"
  digits = []
  while n:
    digits.append(str(n % base))
    n //= base
  return ''.join(digits[::-1])


def base_to_decimal(digits, base):
  """Chuyển đổi từ hệ cơ số bất kỳ sang hệ thập phân (decimal)."""
  n = 0
  for i, digit in enumerate(digits[::-1]):
    n += int(digit) * (base ** i)
  return n


def convert():
  try:
    # Đọc hệ số đầu vào và hệ số đích
    base_from = int(base_from_var.get())
    base_to = int(base_to_var.get())

    # Lấy số từ ô nhập và chuyển về hệ thập phân
    input_number = entry_number.get()
    decimal_number = base_to_decimal([int(digit) for digit in input_number], base_from)

    # Chuyển từ thập phân sang hệ số đích
    result = decimal_to_base(decimal_number, base_to)
    conversion_result.set(result)
  except ValueError:
    conversion_result.set("Lỗi đầu vào")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Chuyển đổi Hệ Cơ Số")
root.geometry("300x300")

# Lựa chọn hệ số đầu vào
ttk.Label(root, text="Chọn hệ số đầu vào:").pack(pady=5)
base_from_var = tk.StringVar(value="10")
base_from_menu = ttk.Combobox(root, textvariable=base_from_var, values=["2", "8", "10", "16"])
base_from_menu.pack()

# Nhập số đầu vào
ttk.Label(root, text="Nhập số:").pack(pady=5)
entry_number = ttk.Entry(root, width=20)
entry_number.pack()

# Lựa chọn hệ số đích
ttk.Label(root, text="Chọn hệ số muốn chuyển:").pack(pady=5)
base_to_var = tk.StringVar(value="2")
base_to_menu = ttk.Combobox(root, textvariable=base_to_var, values=["2", "8", "10", "16"])
base_to_menu.pack()

# Nhãn hiển thị kết quả chuyển đổi
ttk.Label(root, text="Kết quả chuyển đổi:").pack(pady=5)
conversion_result = tk.StringVar()
ttk.Label(root, textvariable=conversion_result).pack()

# Nút chuyển đổi
ttk.Button(root, text="Chuyển đổi", command=convert).pack(pady=10)

# Khởi động vòng lặp Tkinter
root.mainloop()

