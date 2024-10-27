import tkinter as tk
from tkinter import END
import numpy as np

# Khởi tạo cửa sổ ứng dụng
root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")
root.resizable(False, False)

# Khởi tạo màn hình hiển thị
display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Hàm cập nhật màn hình khi nhấn nút
def button_click(value):
    display.insert(END, value)

# Hàm tính toán và hiển thị kết quả
def calculate():
    try:
        expression = display.get()
        result = eval(expression, {"__builtins__": None}, {"np": np})
        display.delete(0, END)
        display.insert(END, result)
    except Exception as e:
        display.delete(0, END)
        display.insert(END, "Error")

# Hàm xóa màn hình
def clear():
    display.delete(0, END)

# Tạo các nút bấm
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('C', 5, 0)
]

# Duyệt qua danh sách nút và tạo từng nút
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=calculate).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    elif text == 'C':
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=clear).grid(row=row, column=col, columnspan=4, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 18),
                  command=lambda t=text: button_click(t)).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# Điều chỉnh các hàng và cột của lưới để co giãn
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i % 4, weight=1)

# Chạy ứng dụng
root.mainloop()

