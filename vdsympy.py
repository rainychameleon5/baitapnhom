import tkinter as tk
from tkinter import messagebox
from sympy import symbols, simplify, Eq, solve, diff, integrate, limit, series, Matrix, sympify

# Khai báo biến của sympy
x, y = symbols('x y')

def show_result(result):
    """Hàm hiển thị kết quả lên cửa sổ thông báo."""
    messagebox.showinfo("Kết quả", str(result))

def get_expression():
    """Lấy biểu thức từ ô nhập và chuyển thành biểu thức sympy."""
    expr_text = entry_expr.get()
    try:
        expr = sympify(expr_text)
        return expr
    except Exception as e:
        messagebox.showerror("Lỗi", "Biểu thức không hợp lệ!")
        return None

def calc_expression():
    expr = get_expression()
    if expr:
        show_result(expr)

def simplify_expression():
    expr = get_expression()
    if expr:
        simplified_expr = simplify(expr)
        show_result(simplified_expr)

def solve_equation():
    expr = get_expression()
    if expr:
        eq = Eq(expr, 0)
        solutions = solve(eq, x)
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

def taylor_series():
    expr = get_expression()
    if expr:
        taylor_series = series(expr, x, 0, 5)
        show_result(taylor_series)

def matrix_determinant():
    # Ma trận là cố định, ví dụ đơn giản
    matrix = Matrix([[1, 2], [3, 4]])
    det = matrix.det()
    show_result(det)

# Tạo giao diện chính
root = tk.Tk()
root.title("SymPy với Tkinter")

# Tạo nhãn và ô nhập cho biểu thức tùy chỉnh
label_expr = tk.Label(root, text="Nhập biểu thức:")
label_expr.pack(pady=10)
entry_expr = tk.Entry(root, width=40)
entry_expr.pack(pady=10)

# Tạo các nút cho từng bài toán
tk.Button(root, text="Hiển thị biểu thức", command=calc_expression).pack(pady=10)
tk.Button(root, text="Rút gọn biểu thức", command=simplify_expression).pack(pady=10)
tk.Button(root, text="Giải phương trình", command=solve_equation).pack(pady=10)
tk.Button(root, text="Tính đạo hàm", command=derivative_expression).pack(pady=10)
tk.Button(root, text="Tính tích phân", command=integral_expression).pack(pady=10)
tk.Button(root, text="Tính giới hạn (khi x -> 0)", command=limit_expression).pack(pady=10)
tk.Button(root, text="Chuỗi Taylor", command=taylor_series).pack(pady=10)
tk.Button(root, text="Định thức ma trận cố định", command=matrix_determinant).pack(pady=10)

# Chạy ứng dụng
root.mainloop()
