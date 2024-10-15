import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

# Global variables to hold images
original_image = None
processed_image = None

# Function to open an image file
def open_image():
    global original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        original_image = cv2.imread(file_path)
        display_image(original_image, canvas_original)
        show_in_new_window(original_image, title="Original Image")  # Display original image in a separate window

# Function to display image on canvas
def display_image(img, canvas):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR (OpenCV) to RGB (Tkinter)
    img = Image.fromarray(img)
    img.thumbnail((200, 200))  # Resize image for display
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(100, 100, image=img_tk)
    canvas.image = img_tk  # Keep reference to avoid garbage collection

# Apply blur filter
def apply_blur():
    global processed_image
    if original_image is not None:
        processed_image = cv2.GaussianBlur(original_image, (15, 15), 0)  # Apply blur
        display_image(processed_image, canvas_blur)
        show_in_new_window(processed_image, title="Blurred Image")

# Apply sharpen filter
def apply_sharpen():
    global processed_image
    if original_image is not None:
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  # Sharpening kernel
        processed_image = cv2.filter2D(original_image, -1, kernel)
        display_image(processed_image, canvas_sharpen)
        show_in_new_window(processed_image, title="Sharpened Image")

# Apply black and white filter
def apply_black_white():
    global processed_image
    if original_image is not None:
        processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        display_image(processed_image, canvas_bw)
        show_in_new_window(processed_image, title="Black & White Image")

# Display image in a new window using matplotlib
def show_in_new_window(image, title="Image"):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if len(image.shape) == 3 else image
    plt.figure()
    plt.title(title)
    plt.imshow(image_rgb, cmap='gray' if len(image.shape) == 2 else None)
    plt.axis('off')  # Hide axes
    plt.show()

# Save processed image to file
def save_image():
    global processed_image
    if processed_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, processed_image)
            messagebox.showinfo("Image Saved", f"Image saved successfully at {file_path}")

# Set up the GUI
root = tk.Tk()
root.title("Image Filter Application")

# Original image holder
original_image = tk.Label(root)
original_image.image = None

# Create canvas for original and filtered images
canvas_original = tk.Canvas(root, width=200, height=200, bg="gray")
canvas_original.grid(row=0, column=0, padx=10, pady=10)

canvas_blur = tk.Canvas(root, width=200, height=200, bg="gray")
canvas_blur.grid(row=0, column=1, padx=10, pady=10)

canvas_sharpen = tk.Canvas(root, width=200, height=200, bg="gray")
canvas_sharpen.grid(row=0, column=2, padx=10, pady=10)

canvas_bw = tk.Canvas(root, width=200, height=200, bg="gray")
canvas_bw.grid(row=0, column=3, padx=10, pady=10)

# Buttons for selecting image and applying filters
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

open_button = tk.Button(button_frame, text="Chọn ảnh", command=open_image)
open_button.grid(row=0, column=1, padx=10)

blur_button = tk.Button(button_frame, text="Làm mờ", command=apply_blur)
blur_button.grid(row=1, column=0, padx=10)

sharpen_button = tk.Button(button_frame, text="Làm nét", command=apply_sharpen)
sharpen_button.grid(row=1, column=1, padx=10)

bw_button = tk.Button(button_frame, text="Đen trắng", command=apply_black_white)
bw_button.grid(row=1, column=2, padx=10)


# Run the application
root.mainloop()
