import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog


def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for enc in encodings:
        try:
            data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding=enc, skip_header=1)
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
        existing_data = load_data(file_path)

        # Kiểm tra xem ID đã tồn tại chưa
        if student_id in existing_data[:, 0]:
            return "ID sinh viên đã tồn tại. Vui lòng sử dụng ID khác."

        new_rows = [
            [student_id, name, "Toán", math_grade],
            [student_id, name, "Lý", physics_grade],
            [student_id, name, "Hóa", chemistry_grade]
        ]
        data = np.vstack((existing_data, new_rows))  # Append new rows to the data
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


def rank_students_by_total_score(data):
    """Sắp xếp theo tổng điểm"""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_scores = {}

    try:
        for row in data:
            student_id, name, subject, grade = row[0], row[1], row[2], float(row[3])

            if student_id not in student_scores:
                student_scores[student_id] = {"name": name, "total_score": 0}

            student_scores[student_id]["total_score"] += grade

        ranked_students = sorted(student_scores.items(), key=lambda x: x[1]["total_score"], reverse=True)

        result = "Bảng xếp hạng theo tổng điểm:\n"
        for idx, (student_id, info) in enumerate(ranked_students, start=1):
            result += f"{idx}. ID: {student_id}, Tên: {info['name']}, Tổng điểm: {info['total_score']:.2f}\n"

        return result
    except ValueError:
        return "Có lỗi khi tính toán điểm. Vui lòng kiểm tra dữ liệu."


def create_search_window():
    search_window = tk.Toplevel(root)
    search_window.title("Tìm kiếm thông tin sinh viên")

    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(search_window, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(search_window, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(search_window, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')

    tk.Label(search_window, text="ID sinh viên:").pack(pady=5)
    id_entry = tk.Entry(search_window)
    id_entry.pack(pady=5)

    tk.Label(search_window, text="Tên môn học (nếu có):").pack(pady=5)
    subject_entry = tk.Entry(search_window)
    subject_entry.pack(pady=5)

    def search_action():
        choice = choice_var.get()
        student_id = id_entry.get()
        subject_name = subject_entry.get()

        if choice == '1':
            result = search_student(data, student_id)
        elif choice == '2':
            result = search_subject(data, subject_name)
        elif choice == '3':
            result = calculate_average(data, student_id)
        else:
            result = "Lựa chọn không hợp lệ."

        messagebox.showinfo("Kết quả", result)
    
    def go_back():
        search_window.destroy()
        

    tk.Button(search_window, text="Tìm kiếm", command=search_action).pack(pady=10)
    tk.Button(search_window, text="Quay lại", command=go_back).pack(pady=5)


def create_add_student_window():
    add_window = tk.Toplevel(root)
    add_window.title("Thêm sinh viên mới")

    tk.Label(add_window, text="ID sinh viên:").pack(pady=5)
    id_entry = tk.Entry(add_window)
    id_entry.pack(pady=5)

    tk.Label(add_window, text="Tên sinh viên:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Điểm Toán:").pack(pady=5)
    math_entry = tk.Entry(add_window)
    math_entry.pack(pady=5)

    tk.Label(add_window, text="Điểm Lý:").pack(pady=5)
    physics_entry = tk.Entry(add_window)
    physics_entry.pack(pady=5)

    tk.Label(add_window, text="Điểm Hóa:").pack(pady=5)
    chemistry_entry = tk.Entry(add_window)
    chemistry_entry.pack(pady=5)

    def add_student_action():
        student_id = id_entry.get()
        name = name_entry.get()
        math_grade = math_entry.get()
        physics_grade = physics_entry.get()
        chemistry_grade = chemistry_entry.get()

        if not student_id or not name or not math_grade or not physics_grade or not chemistry_grade:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

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
        if result.startswith("ID sinh viên đã tồn tại"):
            messagebox.showerror("Lỗi", result)
        else:
            messagebox.showinfo("Kết quả", result)
            
            # Xóa dữ liệu trong các ô nhập sau khi thêm thành công
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            math_entry.delete(0, tk.END)
            physics_entry.delete(0, tk.END)
            chemistry_entry.delete(0, tk.END)
    
    def go_back():
        add_window.destroy()
           

    tk.Button(add_window, text="Thêm sinh viên", command=add_student_action).pack(pady=10)
    tk.Button(add_window, text="Quay lại", command=go_back).pack(pady=5)


def create_rank_window():
    result = rank_students_by_total_score(data)
    messagebox.showinfo("Bảng xếp hạng", result)

    def view_rank():
        result = rank_students_by_total_score(data)
        messagebox.showinfo("Bảng xếp hạng", result)

    def go_back():
        rank_window.destroy()

    tk.Button(rank_window, text="Xem bảng xếp hạng", command=view_rank).pack(pady=10)
    tk.Button(rank_window, text="Quay lại", command=go_back).pack(pady=5)



def main():
    global root, data, file_path
    file_path = 'data.csv'
    data = load_data(file_path)

    root = tk.Tk()
    root.title("Hệ thống Quản lý Sinh viên")
    root.geometry("300x200")

    tk.Button(root, text="Tìm kiếm sinh viên", command=create_search_window).pack(pady=10)
    tk.Button(root, text="Thêm sinh viên", command=create_add_student_window).pack(pady=10)
    tk.Button(root, text="Xếp hạng sinh viên", command=create_rank_window).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
