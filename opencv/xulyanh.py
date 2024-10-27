import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


# Hàm mở ảnh
def open_image():
  file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
  if file_path:
    img = cv2.imread(file_path)
    if img is not None:
      original_image['image'] = img
      processed_image['image'] = img.copy()
      display_images(img, img)
    else:
      messagebox.showerror("Lỗi", "Không thể mở tệp ảnh.")
  else:
    messagebox.showwarning("Cảnh báo", "Không có tệp nào được chọn.")


# Hàm hiển thị ảnh
def display_images(original, processed):
  # Xử lý ảnh gốc
  if len(original.shape) == 2:  # Ảnh grayscale
    original_rgb = cv2.cvtColor(original, cv2.COLOR_GRAY2RGB)
  else:
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
  # Xử lý ảnh đã xử lý
  if len(processed.shape) == 2:  # Ảnh grayscale
    processed_rgb = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
  else:
    processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

  original_pil = Image.fromarray(original_rgb)
  processed_pil = Image.fromarray(processed_rgb)

  original_pil.thumbnail((400, 400))
  processed_pil.thumbnail((400, 400))

  original_tk = ImageTk.PhotoImage(original_pil)
  processed_tk = ImageTk.PhotoImage(processed_pil)

  canvas_original.create_image(200, 200, image=original_tk)
  canvas_original.image = original_tk  # Giữ tham chiếu

  canvas_processed.create_image(200, 200, image=processed_tk)
  canvas_processed.image = processed_tk  # Giữ tham chiếu


# Hàm làm mịn da và loại bỏ mụn
def remove_acne_and_smooth():
  if original_image['image'] is not None:
    img = original_image['image']

    # Bước 1: Làm mịn da bằng Bilateral Filter
    smooth = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)

    # Bước 2: Tìm và xóa mụn
    mask = cv2.inRange(img, (0, 0, 100), (100, 100, 255))  # Tạo mặt nạ cho các điểm sáng (mụn)
    mask_inv = cv2.bitwise_not(mask)  # Mặt nạ ngược

    # Bước 3: Chỉ giữ lại các vùng không phải là mụn
    img_without_acne = cv2.bitwise_and(smooth, smooth, mask=mask_inv)

    # Bước 4: Ghép lại với vùng gốc không có mụn
    img_final = cv2.add(img_without_acne, cv2.bitwise_and(img, img, mask=mask))

    processed_image['image'] = img_final
    display_images(original_image['image'], img_final)
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng mở một ảnh trước.")


# Hàm áp dụng bộ lọc làm mờ
def apply_blur():
  if original_image['image'] is not None:
    img = cv2.GaussianBlur(original_image['image'], (15, 15), 0)
    processed_image['image'] = img
    display_images(original_image['image'], img)


# Hàm áp dụng bộ lọc làm nét
def apply_sharpen():
  if original_image['image'] is not None:
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img = cv2.filter2D(original_image['image'], -1, kernel)
    processed_image['image'] = img
    display_images(original_image['image'], img)


# Hàm áp dụng bộ lọc đen trắng
def apply_black_white():
  if original_image['image'] is not None:
    img = cv2.cvtColor(original_image['image'], cv2.COLOR_BGR2GRAY)
    processed_image['image'] = img
    display_images(original_image['image'], img)
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng mở một ảnh trước.")


# Hàm lưu ảnh đã xử lý
def save_image():
  if processed_image['image'] is not None:
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")])
    if file_path:
      try:
        # Kiểm tra nếu ảnh là grayscale
        if len(processed_image['image'].shape) == 2:
          cv2.imwrite(file_path, processed_image['image'])
        else:
          cv2.imwrite(file_path, processed_image['image'])
        messagebox.showinfo("Lưu ảnh", "Ảnh đã được lưu thành công!")
      except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu ảnh:\n{e}")
  else:
    messagebox.showwarning("Cảnh báo", "Không có ảnh để lưu.")


# Hàm mở cửa sổ chụp ảnh từ camera
def capture_image():
  # Tạo một cửa sổ mới
  capture_window = tk.Toplevel(root)
  capture_window.title("Chụp Ảnh từ Camera")
  capture_window.geometry("600x500")

  # Khung để hiển thị video
  video_label = tk.Label(capture_window)
  video_label.pack()

  # Nút chụp ảnh
  capture_btn = tk.Button(capture_window, text="Chụp Ảnh",
                          command=lambda: take_snapshot(cap, video_label, capture_window))
  capture_btn.pack(pady=10)

  # Mở camera
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
    messagebox.showerror("Lỗi", "Không thể mở camera.")
    capture_window.destroy()
    return

  def show_frame():
    ret, frame = cap.read()
    if ret:
      # Lưu khung hình hiện tại để có thể chụp
      capture_window.current_frame = frame.copy()
      # Chuyển đổi màu cho Tkinter
      cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      pil_image = Image.fromarray(cv2image)
      pil_image = pil_image.resize((600, 400))
      imgtk = ImageTk.PhotoImage(image=pil_image)
      video_label.imgtk = imgtk
      video_label.configure(image=imgtk)
      # Lặp lại sau 10ms
      video_label.after(10, show_frame)
    else:
      messagebox.showerror("Lỗi", "Không thể đọc khung hình từ camera.")
      cap.release()
      capture_window.destroy()

  show_frame()


# Hàm chụp ảnh và đóng cửa sổ video
def take_snapshot(cap, video_label, capture_window):
  ret, frame = cap.read()
  if ret:
    cap.release()
    capture_window.destroy()
    original_image['image'] = frame
    processed_image['image'] = frame.copy()
    display_images(frame, frame)
    messagebox.showinfo("Chụp ảnh", "Ảnh đã được chụp thành công!")
  else:
    messagebox.showerror("Lỗi", "Không thể chụp ảnh từ camera.")


# Hàm làm rõ ảnh X-quang
def enhance_xray():
  if original_image['image'] is not None:
    img = original_image['image']

    # Kiểm tra xem ảnh có phải grayscale không
    if len(img.shape) != 2:
      img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
      img_gray = img.copy()

    # Áp dụng CLAHE để tăng cường độ tương phản
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(img_gray)

    # Chuyển đổi ảnh đã xử lý về định dạng BGR để hiển thị đồng nhất
    enhanced_bgr = cv2.cvtColor(enhanced_img, cv2.COLOR_GRAY2BGR)

    processed_image['image'] = enhanced_bgr
    display_images(original_image['image'], enhanced_bgr)
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng mở một ảnh trước.")


# Hàm phát hiện gãy xương và khoanh vùng
def detect_fracture():
  if original_image['image'] is not None:
    img = original_image['image']

    # Chuyển đổi sang grayscale nếu cần
    if len(img.shape) != 2:
      img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
      img_gray = img.copy()

    # Áp dụng CLAHE để tăng cường độ tương phản
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_gray)

    # Phát hiện cạnh sử dụng bộ lọc Canny
    edges = cv2.Canny(img_clahe, threshold1=80, threshold2=250)

    # Tìm các contour
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Tạo ảnh màu để vẽ bounding boxes
    img_with_boxes = img.copy()

    # Lọc các contour dựa trên diện tích và vẽ bounding boxes
    for contour in contours:
      area = cv2.contourArea(contour)
      if area > 120:  # Ngưỡng diện tích, bạn có thể điều chỉnh tùy ý
        x, y, w, h = cv2.boundingRect(contour)
        # Vẽ hộp bao quanh màu xanh lá cây với độ dày 2
        cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

    processed_image['image'] = img_with_boxes
    display_images(original_image['image'], img_with_boxes)
  else:
    messagebox.showwarning("Cảnh báo", "Vui lòng mở một ảnh trước.")


# Thiết lập giao diện người dùng
root = tk.Tk()
root.title("Ứng dụng Xử lý Ảnh với OpenCV")

# Khung chứa hai canvas để hiển thị ảnh gốc và ảnh đã xử lý
display_frame = tk.Frame(root)
display_frame.pack(pady=10)

# Canvas cho ảnh gốc
canvas_original = tk.Canvas(display_frame, width=400, height=400, bg='gray')
canvas_original.pack(side=tk.LEFT, padx=10)

# Canvas cho ảnh đã xử lý
canvas_processed = tk.Canvas(display_frame, width=400, height=400, bg='gray')
canvas_processed.pack(side=tk.RIGHT, padx=10)

# Các nút điều khiển
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

open_button = tk.Button(button_frame, text="Mở Ảnh", command=open_image)
open_button.grid(row=0, column=0, padx=5, pady=5)

capture_button = tk.Button(button_frame, text="Chụp Ảnh", command=capture_image)
capture_button.grid(row=0, column=1, padx=5, pady=5)

smooth_button = tk.Button(button_frame, text="Làm Mịn Da", command=remove_acne_and_smooth)
smooth_button.grid(row=0, column=2, padx=5, pady=5)

blur_button = tk.Button(button_frame, text="Làm Mờ", command=apply_blur)
blur_button.grid(row=0, column=3, padx=5, pady=5)

sharpen_button = tk.Button(button_frame, text="Làm Nét", command=apply_sharpen)
sharpen_button.grid(row=0, column=4, padx=5, pady=5)

bw_button = tk.Button(button_frame, text="Đen & Trắng", command=apply_black_white)
bw_button.grid(row=0, column=5, padx=5, pady=5)

save_button = tk.Button(button_frame, text="Lưu Ảnh", command=save_image)
save_button.grid(row=0, column=6, padx=5, pady=5)

# Thêm nút làm rõ ảnh X-quang
enhance_xray_button = tk.Button(button_frame, text="Làm Rõ X-Quang", command=enhance_xray)
enhance_xray_button.grid(row=0, column=7, padx=5, pady=5)

# Thêm nút phát hiện gãy xương
detect_fracture_button = tk.Button(button_frame, text="Phát Hiện Gãy Xương", command=detect_fracture)
detect_fracture_button.grid(row=0, column=8, padx=5, pady=5)

# Biến chứa ảnh gốc và ảnh đã xử lý
original_image = {'image': None}
processed_image = {'image': None}

# Chạy ứng dụng
root.mainloop()
