import tkinter as tk
from tkinter import END
import numpy as np
import math

# Khởi tạo cửa sổ ứng dụng
root = tk.Tk()
root.title("Calculator")
root.geometry("300x800")
root.resizable(False, False)

# Hiển thị các ô nhập và kết quả
input_display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
input_display.grid(row=0, column=0, columnspan=5, padx=5, pady=(5, 0), ipady=20)  # Tăng chiều cao

result_display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
result_display.grid(row=1, column=0, columnspan=5, padx=5, pady=(0, 5), ipady=20)  # Tăng chiều cao


# Đặt con trỏ nháy ở vị trí đầu tiên
input_display.focus()  # Đưa focus vào ô nhập
input_display.icursor(0)  # Đặt con trỏ nháy ở đầu ô nhập

# Biến lưu chế độ góc (0 cho radian, 1 cho độ)
angle_mode = tk.IntVar(value=0)
calculated = False
last_result = None
ans_used_once = False
operator_pressed_after_calc = False


# # Hàm khi nhấn nút để cập nhật vào ô nhập
# def button_click(value):
#     global calculated, last_result, operator_pressed_after_calc
#     cursor_position = input_display.index(tk.INSERT)  # Get current cursor position
#
#     if calculated:
#         if value in ('+', '-', '*', '/', '**'):
#             input_display.delete(0, END)
#             input_display.insert(END, f"Ans{value}")
#             operator_pressed_after_calc = True
#         elif value == '^':  # Handle exponentiation like other operators after calculation
#             input_display.delete(0, END)
#             input_display.insert(END, "Ans^")
#             operator_pressed_after_calc = True
#         else:
#             # Nếu nhấn nút khác, chỉ cần thêm giá trị
#             input_display.delete(0, END)
#             input_display.insert(END, value)
#         calculated = False
#     else:
#         # Nếu chưa tính toán, chèn giá trị vào tại vị trí con trỏ
#         input_display.insert(cursor_position, value)  # Insert at the current cursor position
#         input_display.icursor(cursor_position + len(value))  # Move cursor to after the inserted text
#         operator_pressed_after_calc = False

def button_click(value):
    global calculated, last_result, operator_pressed_after_calc
    cursor_position = input_display.index(tk.INSERT)  # Get current cursor position

    if value == '*10^':
        if calculated:  # Nếu đã tính toán trước đó
            input_display.delete(0, END)
            input_display.insert(END, 'Ans*(10^')  # Chèn vào cuối ô nhập
            operator_pressed_after_calc = True
        else:  # Nếu chưa tính toán
            input_display.insert(cursor_position, '*10^')  # Chèn vào vị trí con trỏ
            input_display.icursor(cursor_position + 4)  # Di chuyển con trỏ đến sau phần đã chèn
        return  # Thoát hàm sau khi chèn

    if calculated and not operator_pressed_after_calc:
        # Sau khi có kết quả, nếu nhấn toán tử thì sẽ thêm Ans và toán tử vào cuối ô nhập
        if value in ('+', '-', '*', '/', '**', '^', '*10^'):
            input_display.delete(0, END)
            input_display.insert(END, f"Ans{value}")
            operator_pressed_after_calc = True
        else:
            # Nếu nhấn bất kỳ nút nào khác, thêm ký tự vào vị trí con trỏ
            input_display.insert(cursor_position, value)
            input_display.icursor(cursor_position + len(value))  # Di chuyển con trỏ đến sau ký tự vừa chèn
        calculated = False
    else:
        # Nếu chưa tính toán, chèn giá trị vào tại vị trí con trỏ
        input_display.insert(cursor_position, value)  # Chèn vào vị trí con trỏ hiện tại
        input_display.icursor(cursor_position + len(value))  # Di chuyển con trỏ đến sau ký tự vừa chèn
        operator_pressed_after_calc = False
# Hàm tính toán biểu thức
# Hàm tính toán biểu thức
def calculate():
    global calculated, last_result, ans_used_once, operator_pressed_after_calc
    try:
        expression = input_display.get()

        # Thay "Ans" bằng giá trị kết quả cuối
        if "Ans" in expression and last_result is not None:
            expression = expression.replace("Ans", str(last_result))

        # Thay thế các hàm lượng giác và hằng số bằng numpy
        expression = expression.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan").replace("π", "np.pi")
        expression = expression.replace("√", "np.sqrt").replace("e", "np.e").replace("^", "**").replace("%", "*0.01")

        # Thay thế log và ln
        expression = expression.replace("log(", "math.log10(").replace("ln(", "math.log(")

        # Xử lý giai thừa (!)
        expression = handle_factorial(expression)

        # Chuyển sang độ nếu cần
        if angle_mode.get() == 1:
            expression = expression.replace("np.sin", "np.sin(np.radians").replace("np.cos", "np.cos(np.radians").replace("np.tan", "np.tan(np.radians")
            expression += ")" * expression.count("np.radians")

        # Đánh giá biểu thức
        result = eval(expression, {"__builtins__": None}, {"np": np, "math": math})

        # Gần bằng 0 thì hiển thị 0
        if np.isclose(result, 0, atol=1e-9):
            result = 0

        result_display.delete(0, END)
        result_display.insert(END, result)

        last_result = result  # Chỉ lưu kết quả vào Ans nếu không có lỗi
        calculated = True
        ans_used_once = False
        operator_pressed_after_calc = False

        # Đưa con trỏ đến cuối ô nhập
        input_display.icursor(END)
    except ZeroDivisionError:
        result_display.delete(0, END)
        result_display.insert(END, "Math Error")
    except Exception:
        result_display.delete(0, END)
        result_display.insert(END, "Error")
        last_result = None  # Không lưu giá trị lỗi vào Ans
        calculated = True  # Đánh dấu đã tính để vẫn có thể dùng Ans sau đó


# Hàm xử lý giai thừa (!)
def handle_factorial(expression):
    while '!' in expression:
        idx = expression.index('!')
        num_start = idx - 1
        # Tìm số đứng trước dấu "!"
        while num_start >= 0 and expression[num_start].isdigit():
            num_start -= 1
        num_start += 1
        number = int(expression[num_start:idx])
        factorial_result = math.factorial(number)
        expression = expression[:num_start] + str(factorial_result) + expression[idx + 1:]
    return expression

# Hàm cho nút Ans
def use_ans():
    global last_result, calculated, ans_used_once, operator_pressed_after_calc
    if calculated and not ans_used_once and not operator_pressed_after_calc:
        input_display.delete(0, END)
        ans_used_once = True
    input_display.insert(END, "Ans")
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

# Hàm xóa ký tự trước con trỏ, với xử lý đặc biệt cho các từ đặc biệt
def delete_last():
    cursor_position = input_display.index(tk.INSERT)  # Get current cursor position
    current_text = input_display.get()

    # Special strings to delete entirely if right before the cursor
    special_terms = ["Ans", "cos(", "sin(", "tan(", "log(", "ln("]

    # Check if the cursor is past the beginning
    if cursor_position > 0:
        # Loop through special terms to check if any are right before the cursor
        for term in special_terms:
            term_length = len(term)
            # If there's a special term right before the cursor, delete it
            if current_text[max(0, cursor_position - term_length):cursor_position] == term:
                input_display.delete(cursor_position - term_length, cursor_position)
                input_display.icursor(cursor_position - term_length)  # Move cursor position back
                return  # Exit after deleting term

        # If no special term, delete the single character before the cursor
        input_display.delete(cursor_position - 1, cursor_position)
        input_display.icursor(cursor_position - 1)  # Move cursor one position back

# Hàm di chuyển con trỏ sang trái
def move_cursor_left():
    current_position = input_display.index(tk.INSERT)
    if current_position > 0:
        input_display.icursor(current_position - 1)

# Hàm di chuyển con trỏ sang phải
def move_cursor_right():
    current_position = input_display.index(tk.INSERT)
    if current_position < len(input_display.get()):
        input_display.icursor(current_position + 1)

# Danh sách các nút máy tính với vị trí và thêm nút Ans, √, ^, !, %, log, ln
buttons = [
    ('C', 3, 0), ('←', 3, 1), ('→', 3, 2),
    ('sin', 4, 0), ('cos', 4, 1), ('tan', 4, 2), ('log', 4, 3),
    ('√', 5, 0), ('^', 5, 1), ('!', 5, 2), ('ln', 5, 3),
    ('*10^', 6, 0), ('%', 6, 1), ('e', 6, 2), ('π', 6, 3),
    ('Ans', 7, 0), ('(', 7, 1), (')', 7, 2), ('Del', 7, 3),
    ('7', 8, 0), ('8', 8, 1), ('9', 8, 2), ('/', 8, 3),
    ('4', 9, 0), ('5', 9, 1), ('6', 9, 2), ('*', 9, 3),
    ('1', 10, 0), ('2', 10, 1), ('3', 10, 2), ('-', 10, 3),
    ('0', 11, 0), ('.', 11, 1), ('=', 11, 2), ('+', 11, 3)
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
    elif text == '←':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=move_cursor_left).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == '→':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=move_cursor_right).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == '√':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda: button_click("√(")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'log':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda: button_click("log(")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'ln':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda: button_click("ln(")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'e':  # Define the 'e' button behavior
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda: button_click("e")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(t)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")



# Di chuyển khung tùy chọn góc lên ngay dưới hàng kết quả
angle_frame = tk.Frame(root)
angle_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
tk.Radiobutton(angle_frame, text="Radian", variable=angle_mode, value=0).pack(side="left")
tk.Radiobutton(angle_frame, text="Degree", variable=angle_mode, value=1).pack(side="left")

# Thêm nút Exit ở hàng cuối, chiếm toàn bộ 5 ô
tk.Button(root, text='Exit', width=5, height=2, font=("Arial", 18), command=root.destroy).grid(row=3, column=3, columnspan=5, padx=5, pady=5, sticky="nsew")


# Configure rows and columns to expand
for i in range(12):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Khởi động ứng dụng
root.mainloop()
