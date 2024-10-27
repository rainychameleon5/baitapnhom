import tkinter as tk
from tkinter import END
import numpy as np

# Initialize the main application window
root = tk.Tk()
root.title("Calculator")
root.geometry("300x550")
root.resizable(False, False)

# Display entry widgets for input and result
input_display = tk.Entry(root, font=("Arial", 18), borderwidth=2, relief="ridge", justify="right")
input_display.grid(row=0, column=0, columnspan=5, padx=5, pady=(5, 0))

result_display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
result_display.grid(row=1, column=0, columnspan=5, padx=5, pady=(0, 5))

# Variable to store angle mode (0 for radians, 1 for degrees)
angle_mode = tk.IntVar(value=0)
# Thêm biến để theo dõi khi phép tính hoàn thành
calculated = False
last_result = None
# Cập nhật hàm button_click
def button_click(value):
    global calculated, last_result
    if calculated:
        if value in ('+', '-', '*', '/'):
            # Nếu nhấn nút phép toán sau khi tính xong, hiển thị "Ans" và phép toán mới
            input_display.delete(0, END)
            if last_result is not None:
                input_display.insert(END, f"Ans{value}")  # Chỉ hiển thị Ans nếu đã có giá trị trước đó
            else:
                input_display.insert(END, value)  # Nếu không có giá trị, chỉ hiện phép toán
        else:
            # Nếu nhấn số hoặc ký tự khác, xóa toàn bộ và nhập lại từ đầu
            input_display.delete(0, END)
            input_display.insert(END, value)
        calculated = False
    else:
        input_display.insert(END, value)

# Cập nhật hàm calculate
def calculate():
    global calculated, last_result
    try:
        expression = input_display.get()

        # Thay "Ans" bằng kết quả phép tính cuối cùng chỉ khi last_result có giá trị
        if "Ans" in expression:
            if last_result is not None:
                expression = expression.replace("Ans", str(last_result))
            else:
                result_display.delete(0, END)
                result_display.insert(END, "No Ans")  # Thông báo nếu Ans không có giá trị
                return

        expression = expression.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan").replace("π", "np.pi")

        if angle_mode.get() == 1:  # Degrees
            expression = expression.replace("np.sin", "np.sin(np.radians").replace("np.cos", "np.cos(np.radians").replace("np.tan", "np.tan(np.radians")
            expression += ")" * (expression.count("np.radians"))

        result = eval(expression, {"__builtins__": None}, {"np": np})

        if np.isclose(result, 0, atol=1e-9):
            result = 0

        result_display.delete(0, END)
        result_display.insert(END, result)

        # Lưu kết quả cho lần sử dụng tiếp theo
        last_result = result
        calculated = True
    except ZeroDivisionError:
        result_display.delete(0, END)
        result_display.insert(END, "Math Error")
    except Exception as e:
        result_display.delete(0, END)
        result_display.insert(END, "Error")

# Clear display function
def clear():
    input_display.delete(0, END)
    result_display.delete(0, END)
    global calculated, last_result
    calculated = False
    last_result = None

# Delete last character function
def delete_last():
    current_text = input_display.get()
    input_display.delete(0, END)
    input_display.insert(END, current_text[:-1])

# List of calculator buttons with positions
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('sin', 2, 4),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('cos', 3, 4),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('tan', 4, 4),
    ('0', 5, 0), ('.', 5, 1), ('π', 5, 2), ('+', 5, 3), ('=', 5, 4),
    ('(', 6, 1), (')', 6, 2), ('C', 6, 3), ('Del', 6, 4),
]

# Create calculator buttons dynamically
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
    elif text in ('sin', 'cos', 'tan'):
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(f"{t}(")).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(t)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# Add a frame for the radio buttons
angle_frame = tk.Frame(root)
angle_frame.grid(row=7, column=0, columnspan=5, pady=10)

# Add radio buttons for angle mode selection
tk.Radiobutton(angle_frame, text="Radians", variable=angle_mode, value=0, font=("Arial", 12)).pack(side="left", padx=10)
tk.Radiobutton(angle_frame, text="Degrees", variable=angle_mode, value=1, font=("Arial", 12)).pack(side="left", padx=10)

# Configure rows and columns to expand
for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Run the application
root.mainloop()
