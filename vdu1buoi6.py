import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

# Function to open an image file
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        img = Image.open(file_path)
        original_image.image = img
        display_image(img)

# Function to display an image on the canvas
def display_image(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(200, 200, image=img_tk)
    canvas.image = img_tk  # Keep a reference to avoid garbage collection

# Apply blur filter
def apply_blur():
    if original_image.image:
        img = original_image.image.filter(ImageFilter.GaussianBlur(5))
        display_image(img)

# Apply sharpen filter
def apply_sharpen():
    if original_image.image:
        enhancer = ImageEnhance.Sharpness(original_image.image)
        img = enhancer.enhance(2.0)  # Increase sharpness
        display_image(img)

# Apply black and white filter
def apply_black_white():
    if original_image.image:
        img = original_image.image.convert('L')  # Convert to grayscale
        display_image(img)

# Set up the GUI
root = tk.Tk()
root.title("Image Filter Application")

# Canvas to display the image
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Original image holder
original_image = tk.Label(root)
original_image.image = None

# Buttons for selecting image and applying filters
button_frame = tk.Frame(root)
button_frame.pack()

open_button = tk.Button(button_frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=10, pady=10)

blur_button = tk.Button(button_frame, text="Blur", command=apply_blur)
blur_button.grid(row=0, column=1, padx=10, pady=10)

sharpen_button = tk.Button(button_frame, text="Sharpen", command=apply_sharpen)
sharpen_button.grid(row=0, column=2, padx=10, pady=10)

bw_button = tk.Button(button_frame, text="Black & White", command=apply_black_white)
bw_button.grid(row=0, column=3, padx=10, pady=10)

# Run the application
root.mainloop()
