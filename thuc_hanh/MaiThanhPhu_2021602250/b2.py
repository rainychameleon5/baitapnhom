
import tkinter as tk
from tkinter import messagebox, scrolledtext
from sympy import symbols, simplify, Eq, solve, diff, integrate, limit, sympify, solveset
from sympy.calculus.util import minimum, maximum
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Khai báo biến của sympy
x, y = symbols('x y')


def show_result(result):
    """Hàm hiển thị kết quả lên khu vực hiển thị kết quả."""
    txt_result.config(state='normal')  # Cho phép chỉnh sửa
    txt_result.delete(1.0, tk.END)  # Xóa nội dung cũ
    txt_result.insert(tk.END, str(result))  # Chèn kết quả mới
    txt_result.config(state='disabled')  # Vô hiệu hóa chỉnh sửa


def get_expression():
    """Lấy biểu thức từ ô nhập và chuyển thành biểu thức sympy."""
    expr_text = entry_expr.get()
    try:
        expr = sympify(expr_text)
        return expr
    except Exception as e:
        messagebox.showerror("Lỗi", "Biểu thức không hợp lệ!")
        return None

def delete_last_character():
  """Xóa một ký tự ở vị trí con trỏ trong ô nhập"""
  cursor_position = entry_expr.index(tk.INSERT)
  if cursor_position > 0:
    entry_expr.delete(cursor_position - 1)

def insert_to_entry(value):
  """Chèn ký tự vào vị trí con trỏ trong ô nhập"""
  cursor_position = entry_expr.index(tk.INSERT)
  entry_expr.insert(cursor_position, value)


def clear_entry():
  """Xóa toàn bộ nội dung trong ô nhập"""
  entry_expr.delete(0, tk.END)

def tao_ban_phim_so(parent_frame):
  """Tạo bàn phím số với các phép toán và hàm toán học"""
  keypad_frame = tk.Frame(parent_frame, borderwidth=1, relief='solid')
  keypad_frame.pack(side='right', padx=5)

  # Thêm các phím số và phép toán
  keys = [
    ['(', ')', '^', 'log', 'tan'],
    ['7', '8', '9', 'sin', 'cos'],
    ['4', '5', '6', '*', '/'],
    ['1', '2', '3', '+', '-'],
    ['0', '.', 'x', 'Del', 'C']
  ]

  # Tạo style cho các nút
  button_style = {
      'width': 5,
      'height': 1,
      'font': ('Arial', 10),
      'padx': 2,
      'pady': 2
  }

  for row, key_row in enumerate(keys):
      for col, key in enumerate(key_row):
          if key == 'Del':
              btn = tk.Button(keypad_frame, text=key, command=delete_last_character, **button_style)
              btn.configure(bg='#ff9999')
          elif key == 'C':
              btn = tk.Button(keypad_frame, text=key, command=clear_entry, **button_style)
              btn.configure(bg='#ff6666')
          else:
              # Xử lý các hàm đặc biệt
              if key in ['sin', 'cos', 'tan', 'log', 'exp']:
                  btn = tk.Button(keypad_frame, text=key,
                                  command=lambda k=key: insert_to_entry(f"{k}("),
                                  **button_style)
                  btn.configure(bg='#b3d9ff')
              else:
                  btn = tk.Button(keypad_frame, text=key,
                                  command=lambda k=key: insert_to_entry(k),
                                  **button_style)
                  if key in ['(', ')', '^', '*', '/', 'x', '-', '+']:
                      btn.configure(bg='#e6e6e6')

          btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)

  # Configure grid to expand buttons
  for i in range(5):  # 5 columns
      keypad_frame.grid_columnconfigure(i, weight=1)
  for i in range(5):  # 5 rows
      keypad_frame.grid_rowconfigure(i, weight=1)

def calc_expression():
    expr = get_expression()
    if expr:
        show_result(expr)


def solve_equation():
    expr = get_expression()
    if expr:
        eq = Eq(expr, 0)
        solutions = solve(eq, x)
        try:
            solutions_decimal = [round(sol.evalf(), 3) for sol in solutions]
            show_result(solutions_decimal)
        except Exception as e:
            show_result(solutions)


def derivative_expression():
    expr = get_expression()
    if expr:
        derivative = diff(expr, x)
        show_result(derivative)


def integral_expression():
    expr = get_expression()
    if expr:
        integral = integrate(expr, x)
        show_result(integral)


def limit_expression():
    expr = get_expression()
    if expr:
        lim = limit(expr, x, 0)
        show_result(lim)


def plot_graph():
    expr = get_expression()
    if expr:
        f = lambda val: expr.subs(x, val)
        x_vals = np.linspace(-10, 10, 400)
        y_vals = [f(val) for val in x_vals]

        plt.plot(x_vals, y_vals, label=str(expr))
        plt.title("Đồ thị của biểu thức")
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)
        plt.legend()
        plt.show()


def find_extrema():
    expr = get_expression()
    if expr:
        # Tính đạo hàm bậc nhất
        derivative = diff(expr, x)

        # Giải phương trình đạo hàm bậc nhất = 0 để tìm các điểm cực trị
        critical_points = solve(derivative, x)

        extrema = []
        for point in critical_points:
            second_derivative = diff(derivative, x)
            if second_derivative.subs(x, point) > 0:
                extrema.append((point.evalf(), "Cực tiểu"))
            elif second_derivative.subs(x, point) < 0:
                extrema.append((point.evalf(), "Cực đại"))
            else:
                extrema.append((point.evalf(), "Điểm yên ngựa"))

        show_result(extrema)


# Tạo giao diện chính
root = tk.Tk()
root.title("SymPy với Tkinter")
root.geometry("600x500")  # Kích thước cửa sổ

# Tạo khung cho biểu thức nhập
frame_input = tk.Frame(root)
frame_input.pack(pady=10, padx=10, fill='x')

label_expr = tk.Label(frame_input, text="Nhập biểu thức:")
label_expr.pack(side='left')

entry_expr = tk.Entry(frame_input, width=40)
entry_expr.pack(side='left', padx=10)

tao_ban_phim_so(frame_input)
# Tạo khung cho các nút chức năng
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10, padx=10, fill='x')

buttons = [
    ("Hiển thị biểu thức", calc_expression),
    ("Giải phương trình", solve_equation),
    ("Tính đạo hàm", derivative_expression),
    ("Tính tích phân", integral_expression),
    ("Tính giới hạn (khi x -> 0)", limit_expression),
    ("Vẽ đồ thị", plot_graph),
    ("Tìm cực trị", find_extrema),
]

# Sắp xếp các nút trong grid 2 cột
for i, (text, command) in enumerate(buttons):
    btn = tk.Button(frame_buttons, text=text, command=command, width=25)
    btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky='ew')

# Tạo khung để hiển thị kết quả
frame_result = tk.Frame(root)
frame_result.pack(pady=10, padx=10, fill='both', expand=True)

label_result = tk.Label(frame_result, text="Kết quả:")
label_result.pack(anchor='w')

# Sử dụng scrolledtext để hiển thị kết quả với thanh cuộn
txt_result = scrolledtext.ScrolledText(frame_result, height=15, state='disabled', wrap='word')
txt_result.pack(fill='both', expand=True)

# Chạy ứng dụng
root.mainloop()