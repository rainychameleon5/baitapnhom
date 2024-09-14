import numpy as np


def lay_phan_tu_ma_tran(hang, cot):
    """Hàm để nhập các phần tử và kiểm tra định dạng đúng."""
    while True:
        print(f"Nhập các phần tử cho ma trận dạng mảng 1 chiều (phải có {hang * cot} phần tử):")
        phantu = list(map(float(input().split())))
        try:
            if len(phantu) != hang * cot:
                print(f"Số lượng phần tử phải là {hang * cot}, nhưng bạn đã nhập {len(phantu)} phần tử.Mời nhập lại")
            return np.array(phantu).reshape(hang, cot)
        except ValueError :
            print(f"Lỗi không đúng định dạng. Vui lòng nhập lại.")


# Nhập số lượng ma trận
while True:
    try:
        n = int(input("Nhập số lượng ma trận (phải là số nguyên): "))
        if n <= 0:
            print("Số lượng ma trận phải là số nguyên dương.")
        else:
            break
    except ValueError:
        print("Lỗi không đúng định dạng. Vui lòng nhập lại.")

# Danh sách để lưu các ma trận
dsach = []

# Nhập kích thước và tạo các ma trận
for i in range(n):
    while True:
        try:
            print(f"Nhập kích thước cho ma trận {i + 1}:")
            hang = int(input(f"Số hàng cho ma trận {i + 1}: "))
            cot = int(input(f"Số cột cho ma trận {i + 1}: "))
            if hang <= 0 or cot <= 0:
                print("Số hàng và số cột phải là các số nguyên dương.")
            else:
                break
        except ValueError :
            print(f"Lỗi không đúng định dạng. Vui lòng nhập lại.")

    # Nhập các phần tử cho ma trận và kiểm tra
    matran = lay_phan_tu_ma_tran(hang, cot)

    # Thêm ma trận vào danh sách
    dsach.append(matran)

# In ra các ma trận đã nhập
for i, matr in enumerate(dsach):
    print(f"\nMa trận {i + 1}:")
    print(matr)
