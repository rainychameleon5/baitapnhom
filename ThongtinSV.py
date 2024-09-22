import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog


def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for enc in encodings:
        try:
            data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
            return data
        except Exception as e:
            print(f"Error loading data with encoding {enc}: {e}")

    print("Failed to load data with all attempted encodings.")
    return np.array([])

def save_data(file_path, data):
    """Lưu dữ liệu sinh viên vào file CSV."""
    header = "ID,Tên,Môn học,Điểm"
    try:
        np.savetxt(file_path, data, delimiter=",", fmt="%s", header=header, comments='', encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def add_student_data(file_path, student_id, name, math_grade, physics_grade, chemistry_grade):
    """Thêm thông tin sinh viên"""
    try:
        new_rows = [
            [student_id, name, "Toán", math_grade],
            [student_id, name, "Lý", physics_grade],
            [student_id, name, "Hóa", chemistry_grade]
        ]
        data = np.vstack((load_data(file_path), new_rows))  # Append new rows to the data
        success = save_data(file_path, data)
        if success:
            return f"Thêm dữ liệu cho sinh viên {name} (ID: {student_id}) thành công!"
        else:
            return "Không thể lưu dữ liệu vào file."
    except Exception as e:
        return f"Lỗi khi thêm dữ liệu: {e}"

def search_student(data, student_id):
    """Search for a student's information by ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])


def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])


def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."

def add_student_action():
    """Thêm thông tin"""
    student_id = id_entry.get()
    name = name_entry.get()
    math_grade = math_entry.get()
    physics_grade = physics_entry.get()
    chemistry_grade = chemistry_entry.get()

    if not student_id or not name or not math_grade or not physics_grade or not chemistry_grade:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return
    #Chỉ cho phép nhập giá trị điểm từ 0 đến 10
    try:
        math_grade = float(math_grade)
        physics_grade = float(physics_grade)
        chemistry_grade = float(chemistry_grade)

        if not (0 <= math_grade <= 10) or not (0 <= physics_grade <= 10) or not (0 <= chemistry_grade <= 10):
            raise ValueError

    except ValueError:
        messagebox.showerror("Lỗi", "Điểm phải là số thực trong khoảng từ 0 đến 10.")
        return
    
    result = add_student_data(file_path, student_id, name, math_grade, physics_grade, chemistry_grade)
    messagebox.showinfo("Kết quả", result)

def search_action():
    choice = choice_var.get()
    student_id = id_entry.get()
    subject_name = subject_entry.get()

    if choice == '1':  # Tìm kiếm thông tin sinh viên
        result = search_student(data, student_id)
    elif choice == '2':  # Tìm kiếm điểm môn học
        result = search_subject(data, subject_name)
    elif choice == '3':  # Tính TBC điểm của sinh viên
        result = calculate_average(data, student_id)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)


def main():
    global data
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    # Thêm các widget
    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')

    tk.Label(root, text="ID sinh viên:").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    tk.Label(root, text="Tên sinh viên:").pack(pady=5)
    global name_entry
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Điểm Toán:").pack(pady=5)
    global math_entry
    math_entry = tk.Entry(root)
    math_entry.pack(pady=5)

    tk.Label(root, text="Điểm Lý:").pack(pady=5)
    global physics_entry
    physics_entry = tk.Entry(root)
    physics_entry.pack(pady=5)

    tk.Label(root, text="Điểm Hóa:").pack(pady=5)
    global chemistry_entry
    chemistry_entry = tk.Entry(root)
    chemistry_entry.pack(pady=5)

    
    tk.Button(root, text="Thêm sinh viên", command=add_student_action).pack(pady=10)
    tk.Button(root, text="Tìm kiếm", command=search_action).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
