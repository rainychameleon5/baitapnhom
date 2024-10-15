import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

# Global variables to hold images for each filter
original_image = None
blurred_image = None
sharpened_image = None
bw_image = None

# Function to open an image file
def open_image():
    global original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        original_image = cv2.imread(file_path)
        display_image(original_image, canvas_original)
        show_in_new_window(original_image, title="Ảnh gốc")  # Display original image in a separate window

# Function to display image on canvas
# Function to display an image on a canvas
def display_image(img, canvas):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR (OpenCV) to RGB (Tkinter)
    img = Image.fromarray(img)
    img.thumbnail((200, 200))  # Resize image for display
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(100, 100, image=img_tk)
    canvas.image = img_tk  # Keep reference to avoid garbage collection


# Open the camera and capture an image using Tkinter
def open_camera():
    global original_image
    cap = cv2.VideoCapture(0)  # Open default camera

    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Không thể truy cập vào camera")
        return

    camera_window = tk.Toplevel()  # Create a new window for the camera feed
    camera_window.title("Chụp ảnh từ camera")

    # Create a canvas for the camera feed
    camera_canvas = tk.Canvas(camera_window, width=640, height=480)
    camera_canvas.pack()

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            camera_canvas.imgtk = imgtk  # Keep reference to avoid garbage collection
            camera_window.after(10, update_frame)  # Refresh the frame every 10 ms

    def capture_image():
        global original_image
        ret, frame = cap.read()
        if ret:
            original_image = frame  # Save the captured frame
            display_image(original_image, canvas_original)  # Display the captured image in the main window
            camera_window.destroy()  # Close the camera window

    # Capture button
    capture_button = tk.Button(camera_window, text="Chụp ảnh", command=capture_image)
    capture_button.pack()

    update_frame()  # Start updating frames in the camera window

    camera_window.mainloop()

    cap.release()

# Apply blur filter
def apply_blur():
    global blurred_image
    if original_image is not None:
        blurred_image = cv2.GaussianBlur(original_image, (15, 15), 0)  # Apply blur
        display_image(blurred_image, canvas_blur)
        show_in_new_window(blurred_image, title="Ảnh làm mờ")

# Apply sharpen filter
def apply_sharpen():
    global sharpened_image
    if original_image is not None:
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  # Sharpening kernel
        sharpened_image = cv2.filter2D(original_image, -1, kernel)
        display_image(sharpened_image, canvas_sharpen)
        show_in_new_window(sharpened_image, title="Ảnh làm nét")

# Apply black and white filter
def apply_black_white():
    global bw_image
    if original_image is not None:
        bw_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        display_image(bw_image, canvas_bw)
        show_in_new_window(bw_image, title="Ảnh đen trắng")

# Function to save specific image to file
def save_image(image, filter_name):
    if image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, image)
            messagebox.showinfo("Lưu ảnh", f"Ảnh {filter_name} đã lưu thành công tại {file_path}")

# Display image in a new window using matplotlib
def show_in_new_window(image, title="Image"):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if len(image.shape) == 3 else image
    plt.figure()
    plt.title(title)
    plt.imshow(image_rgb, cmap='gray' if len(image.shape) == 2 else None)
    plt.axis('off')  # Hide axes
    plt.show()

# Set up the GUI
root = tk.Tk()
root.title("Ứng dụng bộ lọc ảnh")

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

# Buttons for selecting image, capturing from camera, and applying filters
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

open_button = tk.Button(button_frame, text="Mở ảnh", command=open_image)
open_button.grid(row=0, column=0, padx=10)

camera_button = tk.Button(button_frame, text="Chụp ảnh từ camera", command=open_camera)
camera_button.grid(row=0, column=1, padx=10)

blur_button = tk.Button(button_frame, text="Làm mờ", command=apply_blur)
blur_button.grid(row=0, column=2, padx=10)

sharpen_button = tk.Button(button_frame, text="Làm nét", command=apply_sharpen)
sharpen_button.grid(row=0, column=3, padx=10)

bw_button = tk.Button(button_frame, text="Đen trắng", command=apply_black_white)
bw_button.grid(row=0, column=4, padx=10)

# Save buttons under each processed image
save_blur_button = tk.Button(root, text="Lưu ảnh làm mờ", command=lambda: save_image(blurred_image, "làm mờ"))
save_blur_button.grid(row=2, column=1, padx=10, pady=10)

save_sharpen_button = tk.Button(root, text="Lưu ảnh làm nét", command=lambda: save_image(sharpened_image, "làm nét"))
save_sharpen_button.grid(row=2, column=2, padx=10, pady=10)

save_bw_button = tk.Button(root, text="Lưu ảnh đen trắng", command=lambda: save_image(bw_image, "đen trắng"))
save_bw_button.grid(row=2, column=3, padx=10, pady=10)

# Run the application
root.mainloop()
