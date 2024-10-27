import tkinter as tk
from tkinter import END
import numpy as np

# Khởi tạo cửa sổ ứng dụng
root = tk.Tk()
root.title("Calculator")
root.geometry("300x550")
root.resizable(False, False)

# Hiển thị các ô nhập và kết quả
input_display = tk.Entry(root, font=("Arial", 18), borderwidth=2, relief="ridge", justify="right")
input_display.grid(row=0, column=0, columnspan=5, padx=5, pady=(5, 0))

result_display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
result_display.grid(row=1, column=0, columnspan=5, padx=5, pady=(0, 5))

# Biến lưu chế độ góc (0 cho radian, 1 cho độ)
angle_mode = tk.IntVar(value=0)
calculated = False
last_result = None  # Lưu kết quả phép tính cuối
ans_used_once = False  # Kiểm soát việc sử dụng Ans chỉ xóa thanh nhập một lần sau khi nhấn dấu bằng
operator_pressed_after_calc = False  # Kiểm soát việc có nhấn phép toán sau khi tính hay không


# Hàm khi nhấn nút để cập nhật vào ô nhập
def button_click(value):
    global calculated, last_result, operator_pressed_after_calc
    if calculated:
        if value in ('+', '-', '*', '/'):
            input_display.delete(0, END)
            input_display.insert(END, f"Ans{value}")
            operator_pressed_after_calc = True  # Đánh dấu rằng một phép toán đã được nhấn sau khi tính
        else:
            input_display.delete(0, END)
            input_display.insert(END, value)
        calculated = False
    else:
        input_display.insert(END, value)
        operator_pressed_after_calc = False  # Reset khi nhập các ký tự khác phép toán


# Hàm tính toán biểu thức
def calculate():
    global calculated, last_result, ans_used_once, operator_pressed_after_calc
    try:
        expression = input_display.get()

        # Thay "Ans" bằng giá trị kết quả cuối
        if "Ans" in expression and last_result is not None:
            expression = expression.replace("Ans", str(last_result))

        # Thay thế các hàm lượng giác bằng numpy
        expression = expression.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan").replace("π",
                                                                                                                   "np.pi")

        # Chuyển sang độ nếu cần
        if angle_mode.get() == 1:
            expression = expression.replace("np.sin", "np.sin(np.radians").replace("np.cos",
                                                                                   "np.cos(np.radians").replace(
                "np.tan", "np.tan(np.radians")
            expression += ")" * expression.count("np.radians")

        # Đánh giá biểu thức
        result = eval(expression, {"__builtins__": None}, {"np": np})

        # Gần bằng 0 thì hiển thị 0
        if np.isclose(result, 0, atol=1e-9):
            result = 0

        result_display.delete(0, END)
        result_display.insert(END, result)

        last_result = result
        calculated = True
        ans_used_once = False  # Reset để khi nhấn Ans sẽ xóa thanh nhập ở lần đầu tiên
        operator_pressed_after_calc = False  # Reset khi tính xong
    except ZeroDivisionError:
        result_display.delete(0, END)
        result_display.insert(END, "Math Error")
    except Exception:
        result_display.delete(0, END)
        result_display.insert(END, "Error")


# Hàm cho nút Ans
def use_ans():
    global last_result, calculated, ans_used_once, operator_pressed_after_calc
    if not ans_used_once and not operator_pressed_after_calc:  # Chỉ xóa thanh nhập nếu Ans được dùng ngay sau phép tính và không có phép toán nào
        input_display.delete(0, END)
        ans_used_once = True
    input_display.insert(END, "Ans")  # Hiển thị "Ans" thay vì giá trị của nó
    calculated = False


# Hàm xóa toàn bộ
def clear():
    input_display.delete(0, END)
    result_display.delete(0, END)
    global calculated, last_result, ans_used_once, operator_pressed_after_calc
    calculated = False
    last_result = None
    ans_used_once = False
    operator_pressed_after_calc = False


# Hàm xóa ký tự cuối
def delete_last():
    current_text = input_display.get()
    input_display.delete(0, END)
    input_display.insert(END, current_text[:-1])


# Danh sách các nút máy tính với vị trí và thêm nút Ans
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('sin', 2, 4),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('cos', 3, 4),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('tan', 4, 4),
    ('0', 5, 0), ('.', 5, 1), ('π', 5, 2), ('+', 5, 3), ('=', 5, 4),
    ('(', 6, 1), (')', 6, 2), ('C', 6, 3), ('Del', 6, 4), ('Ans', 6, 0)  # Nút Ans ở vị trí hàng 6, cột 0
]

# Tạo các nút máy tính
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=calculate).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'C':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=clear).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'Del':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=delete_last).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'Ans':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=use_ans).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text in ('sin', 'cos', 'tan'):
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(f"{t}(")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(t)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# Thêm các nút tùy chọn góc
angle_frame = tk.Frame(root)
angle_frame.grid(row=7, column=0, columnspan=5, pady=10)
tk.Radiobutton(angle_frame, text="Radians", variable=angle_mode, value=0, font=("Arial", 12)).pack(side="left", padx=10)
tk.Radiobutton(angle_frame, text="Degrees", variable=angle_mode, value=1, font=("Arial", 12)).pack(side="left", padx=10)

# Cấu hình kích thước hàng và cột
for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Chạy ứng dụng
root.mainloop()
