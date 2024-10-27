import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext


def lay_phan_tu_ma_tran(hang, cot):
    """Hàm để nhập các phần tử và kiểm tra định dạng đúng."""
    while True:
        try:
            phantu = list(map(float, entry_matrix.get("1.0", tk.END).split()))
            if len(phantu) != hang * cot:
                raise ValueError(f"Số lượng phần tử phải là {hang * cot}, nhưng bạn đã nhập {len(phantu)} phần tử.")
            return np.array(phantu).reshape(hang, cot)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập lại")
        return None


def dinh_thuc_ma_tran(matran):
    """Tính định thức"""
    try:
        if matran.shape[0] != matran.shape[1]:
            raise ValueError("Ma trận vuông mới có thể tính định thức")
        dinh_thuc = np.linalg.det(matran)
        return dinh_thuc
    except np.linalg.LinAlgError:
        raise ValueError("Ma trận không thể tính định thức")


def nghich_dao_ma_tran(matran):
    """Tính nghịch đảo"""
    try:
        if matran.shape[0] != matran.shape[1]:
            raise ValueError("Ma trận vuông mới có thể tính nghịch đảo")
        nghich_dao = np.linalg.inv(matran)  # Tính nghịch đảo
        return nghich_dao
    except np.linalg.LinAlgError:  # Khi không có nghịch đảo, numpy sinh lỗi np.linalg.LinAlgError
        raise ValueError("Ma trận không khả nghịch.")


def xac_nhan_so_luong_ma_tran():
    # Nhập số lượng ma trận
    global n
    try:
        n = int(entry_so_luong.get())
        if n <= 0:
            raise ValueError("Số lượng ma trận phải là số nguyên dương.")
        messagebox.showinfo("Thông báo", f"Bạn sẽ nhập {n} ma trận.")
        enable_matrix_input()
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập lại")


def enable_matrix_input():
    """Kích hoạt giao diện nhập ma trận"""
    entry_hang.config(state='normal')
    entry_cot.config(state='normal')
    entry_matrix.config(state='normal')
    btn_add.config(state='normal')


def them_ma_tran():
    """Thêm ma trận vào danh sách"""
    global dsach
    try:
        if len(dsach) >= n:
            raise ValueError(f"Đã đủ {n} ma trận. Không thể thêm ma trận mới.")
        hang = int(entry_hang.get())
        cot = int(entry_cot.get())
        if hang <= 0 or cot <= 0:
            raise ValueError("Số hàng và số cột phải là các số nguyên dương.")
        matran = lay_phan_tu_ma_tran(hang, cot)
        if matran is not None:
            dsach.append(matran)
            cap_nhat_danh_sach_ma_tran()
            messagebox.showinfo("Thành công", f"Đã thêm ma trận {len(dsach)}")
            if len(dsach) == n:
                btn_add.config(state='disabled')
                messagebox.showinfo("Thông báo", f"Đã nhập đủ {n} ma trận.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập lại")


def cap_nhat_danh_sach_ma_tran():
    """Cập nhật danh sách ma trận trong giao diện"""
    text_matrices.delete('1.0', tk.END)
    for i, matr in enumerate(dsach):
        text_matrices.insert(tk.END, f"Ma trận {i + 1}:\n{matr}\n\n")


def cong_ma_tran():
    """Thực hiện phép cộng ma trận"""
    try:
        chon = list(map(int, entry_cong.get().split()))
        if any(i < 1 or i > len(dsach) for i in chon):
            raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")
        dsach_cong = [dsach[i - 1] for i in chon]
        if len(dsach_cong) < 2:
            raise ValueError("Cần ít nhất 2 ma trận để thực hiện phép cộng.")
        if not all(mat.shape == dsach_cong[0].shape for mat in dsach_cong):
            raise ValueError("Các ma trận phải có cùng kích thước để cộng.")
        tong_matran = np.sum(dsach_cong, axis=0)
        text_result.delete('1.0', tk.END)
        text_result.insert(tk.END, f"Tổng của các ma trận:\n{tong_matran}")
    except ValueError:
        messagebox.showerror("Lỗi", "Không phù hợp")


def tru_ma_tran():
    """Thực hiện phép trừ ma trận"""
    try:
        chon = list(map(int, entry_tru.get().split()))
        if any(i < 1 or i > len(dsach) for i in chon):
            raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")
        dsach_tru = [dsach[i - 1] for i in chon]
        if len(dsach_tru) < 2:
            raise ValueError("Cần ít nhất 2 ma trận để thực hiện phép trừ.")
        if not all(mat.shape == dsach_tru[0].shape for mat in dsach_tru):
            raise ValueError("Các ma trận phải có cùng kích thước để trừ.")
        hieu_matran = dsach_tru[0]
        for matran in dsach_tru[1:]:
            hieu_matran = np.subtract(hieu_matran, matran)
        text_result.delete('1.0', tk.END)
        text_result.insert(tk.END, f"Hiệu của các ma trận:\n{hieu_matran}")
    except ValueError:
        messagebox.showerror("Lỗi", "Không phù hợp")


def tinh_dinh_thuc():
    """Tính và hiển thị định thức của các ma trận"""
    text_result.delete('1.0', tk.END)
    for i, matr in enumerate(dsach):
        try:
            dinhthuc = dinh_thuc_ma_tran(matr)
            text_result.insert(tk.END, f"Định thức ma trận {i + 1}: {dinhthuc}\n")
        except ValueError:
            text_result.insert(tk.END, f"Không tính được định thức cho ma trận {i + 1}.\n")


def tinh_nghich_dao():
    """Tính và hiển thị nghịch đảo của các ma trận"""
    text_result.delete('1.0', tk.END)
    for i, matr in enumerate(dsach):
        try:
            nghichdao = nghich_dao_ma_tran(matr)
            text_result.insert(tk.END, f"Nghịch đảo ma trận {i + 1}:\n{nghichdao}\n\n")
        except ValueError:
            text_result.insert(tk.END, f"Không có ma trận nghịch đảo cho ma trận {i + 1}.\n")


def tim_hang_ma_tran():
    """Tính và hiển thị hạng của các ma trận"""
    text_result.delete('1.0', tk.END)
    for i, matr in enumerate(dsach):
        hang = np.linalg.matrix_rank(matr)
        text_result.insert(tk.END, f"Hạng của ma trận {i + 1}: {hang}\n")


def nhan_ma_tran():
    """Thực hiện phép nhân ma trận"""
    try:
        chon = list(map(int, entry_nhan.get().split()))
        if len(chon) == 1:
            so = float(entry_hang.get())  # Sử dụng ô nhập hàng để nhập số cần nhân với ma trận
            ketqua = dsach[chon[0] - 1] * so
            text_result.delete('1.0', tk.END)
            text_result.insert(tk.END, f"Nhân ma trận với số {so}:\n{ketqua}")
        else:
            if any(i < 1 or i > len(dsach) for i in chon):
                raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")
            dsach_nhan = [dsach[i - 1] for i in chon]
            if dsach_nhan[0].shape[1] != dsach_nhan[1].shape[0]:
                raise ValueError("Số cột của ma trận thứ nhất phải bằng số hàng của ma trận thứ hai để nhân.")
            ketqua = np.dot(dsach_nhan[0], dsach_nhan[1])
            text_result.delete('1.0', tk.END)
            text_result.insert(tk.END, f"Kết quả phép nhân ma trận:\n{ketqua}")
    except ValueError:
        messagebox.showerror("Lỗi", "Không hợp lệ")


def chia_ma_tran():
    """Thực hiện phép chia ma trận"""
    try:
        chon = list(map(int, entry_chia.get().split()))
        if len(chon) != 2:
            raise ValueError("Cần chọn 2 ma trận để thực hiện phép chia.")
        if any(i < 1 or i > len(dsach) for i in chon):
            raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")
        ma_tran_1, ma_tran_2 = dsach[chon[0] - 1], dsach[chon[1] - 1]
        if ma_tran_2.shape[0] != ma_tran_2.shape[1]:
            raise ValueError("Ma trận thứ hai phải là ma trận vuông để tính nghịch đảo.")
        ma_tran_nghich_dao = nghich_dao_ma_tran(ma_tran_2)
        ketqua = np.dot(ma_tran_1, ma_tran_nghich_dao)
        text_result.delete('1.0', tk.END)
        text_result.insert(tk.END, f"Kết quả phép chia ma trận:\n{ketqua}")
    except ValueError:
        messagebox.showerror("Lỗi", "Không hợp lệ")


# Tạo giao diện người dùng
root = tk.Tk()
root.title("Phép toán ma trận")

tk.Label(root, text="Số lượng ma trận:").grid(row=0, column=0)
entry_so_luong = tk.Entry(root)
entry_so_luong.grid(row=0, column=1)
btn_xac_nhan = tk.Button(root, text="Xác nhận", command=xac_nhan_so_luong_ma_tran)
btn_xac_nhan.grid(row=0, column=2)

tk.Label(root, text="Số hàng:").grid(row=1, column=0)
entry_hang = tk.Entry(root, state='disabled')
entry_hang.grid(row=1, column=1)

tk.Label(root, text="Số cột:").grid(row=2, column=0)
entry_cot = tk.Entry(root, state='disabled')
entry_cot.grid(row=2, column=1)

tk.Label(root, text="Nhập ma trận (cách nhau bởi khoảng trắng):").grid(row=3, column=0, columnspan=2)
entry_matrix = scrolledtext.ScrolledText(root, height=5, width=40, state='disabled')
entry_matrix.grid(row=4, column=0, columnspan=2)

btn_add = tk.Button(root, text="Thêm Ma Trận", command=them_ma_tran, state='disabled')
btn_add.grid(row=5, column=0, columnspan=2)

tk.Label(root, text="Danh sách ma trận:").grid(row=6, column=0, columnspan=2)
text_matrices = scrolledtext.ScrolledText(root, height=10, width=40)
text_matrices.grid(row=7, column=0, columnspan=2)

tk.Label(root, text="Chọn ma trận để cộng:").grid(row=8, column=0)
entry_cong = tk.Entry(root)
entry_cong.grid(row=8, column=1)
btn_cong = tk.Button(root, text="Cộng Ma Trận", command=cong_ma_tran)
btn_cong.grid(row=9, column=0, columnspan=2)

tk.Label(root, text="Chọn ma trận để trừ:").grid(row=10, column=0)
entry_tru = tk.Entry(root)
entry_tru.grid(row=10, column=1)
btn_tru = tk.Button(root, text="Trừ Ma Trận", command=tru_ma_tran)
btn_tru.grid(row=11, column=0, columnspan=2)

tk.Label(root, text="Chọn ma trận để nhân:").grid(row=13, column=0)
entry_nhan = tk.Entry(root)
entry_nhan.grid(row=13, column=1)
btn_nhan = tk.Button(root, text="Nhân Ma Trận", command=nhan_ma_tran)
btn_nhan.grid(row=14, column=0, columnspan=2)

tk.Label(root, text="Chọn ma trận để chia:").grid(row=17, column=0)
entry_chia = tk.Entry(root)
entry_chia.grid(row=17, column=1)
btn_chia = tk.Button(root, text="Chia Ma Trận", command=chia_ma_tran)
btn_chia.grid(row=18, column=0, columnspan=2)

btn_dinh_thuc = tk.Button(root, text="Tính Định Thức", command=tinh_dinh_thuc)
btn_dinh_thuc.grid(row=20, column=0)

btn_nghich_dao = tk.Button(root, text="Tính Nghịch Đảo", command=tinh_nghich_dao)
btn_nghich_dao.grid(row=20, column=1)

btn_hang = tk.Button(root, text="Tìm Hạng Ma Trận", command=tim_hang_ma_tran)
btn_hang.grid(row=21, column=0, columnspan=2)



tk.Label(root, text="Kết quả:").grid(row=22, column=0, columnspan=2)
text_result = scrolledtext.ScrolledText(root, height=10, width=40)
text_result.grid(row=23, column=0, columnspan=2)

n = 0  # Số lượng ma trận
dsach = []  # Danh sách để lưu các ma trận

root.mainloop()
