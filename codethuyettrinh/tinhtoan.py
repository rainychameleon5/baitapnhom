import tkinter as tk
from tkinter import END
import numpy as np

# Initialize the main application window
root = tk.Tk()
root.title("Calculator")
root.geometry("300x550")
root.resizable(False, False)

# Display entry widget
display = tk.Entry(root, font=("Arial", 24), borderwidth=2, relief="ridge", justify="right")
display.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

# Variable to store angle mode (0 for radians, 1 for degrees)
angle_mode = tk.IntVar(value=0)


# Button click function to update the display
def button_click(value):
    display.insert(END, value)


# Function to evaluate the expression based on angle mode
def calculate():
    try:
        expression = display.get()

        # Replace trigonometric functions with numpy functions
        expression = expression.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan").replace("π",
                                                                                                                   "np.pi")

        # If in degree mode, convert degrees to radians in the calculation
        if angle_mode.get() == 1:  # Degrees
            expression = expression.replace("np.sin", "np.sin(np.radians").replace("np.cos",
                                                                                   "np.cos(np.radians").replace(
                "np.tan", "np.tan(np.radians")
            expression += ")" * (expression.count("np.radians"))  # Close the parentheses

        # Evaluate the expression safely using numpy functions
        result = eval(expression, {"__builtins__": None}, {"np": np})
        display.delete(0, END)
        display.insert(END, result)
    except ZeroDivisionError:
        display.delete(0, END)
        display.insert(END, "Math Error")
    except Exception as e:
        display.delete(0, END)
        display.insert(END, "Error")


# Clear display function
def clear():
    display.delete(0, END)


# Delete last character function
def delete_last():
    current_text = display.get()
    display.delete(0, END)
    display.insert(END, current_text[:-1])


# List of calculator buttons with positions
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sin', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('cos', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('tan', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('π', 4, 2), ('+', 4, 3), ('=', 4, 4),
    ('(', 5, 1), (')', 5, 2), ('C', 5, 3), ('Del', 5, 4),
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
angle_frame.grid(row=6, column=0, columnspan=5, pady=10)

# Add radio buttons for angle mode selection
tk.Radiobutton(angle_frame, text="Radians", variable=angle_mode, value=0, font=("Arial", 12)).pack(side="left", padx=10)
tk.Radiobutton(angle_frame, text="Degrees", variable=angle_mode, value=1, font=("Arial", 12)).pack(side="left", padx=10)

# Configure rows and columns to expand
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Run the application
root.mainloop()
