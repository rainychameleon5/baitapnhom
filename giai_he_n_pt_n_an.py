import numpy as np


def nhap_n():
    while True:
        try:
            n = int(input('Nhập số lượng ẩn: '))
            if n <= 0:
                raise ValueError("Số lượng ẩn phải là số nguyên dương.")
            else:
                return n
        except:
            print("Lỗi! Vui lòng nhập lại đúng định dạng")

def nhap_ptu(ptu):
    while True:
        try:
            gtri = float(input(ptu))
            return gtri
        except ValueError:
            print("Lỗi! Vui lòng nhập lại đúng định dạng")


def tinh_toan():
    # Nhập số ẩn (số phương trình)
    n = nhap_n()

    # Khởi tạo ma trận hệ số A và vector B
    A = np.zeros((n, n))
    B = np.zeros(n)

    # Nhập ma trận hệ số A
    print("Nhập các hệ số của ma trận A:")
    for i in range(n):
        for j in range(n):
            A[i][j] = nhap_ptu(f"A[{i+1}][{j+1}] = ")

    # Nhập vector B
    print("Nhập các giá trị của vector B:")
    for i in range(n):
        B[i] = nhap_ptu(f"B[{i+1}] = ")

    # Giải hệ phương trình
    try:
        X = np.linalg.solve(A, B)
        print(f"Nghiệm của hệ phương trình là: {X}")
    except np.linalg.LinAlgError:
        print("Hệ phương trình không có nghiệm duy nhất (ma trận suy biến).")

# Gọi hàm để giải hệ phương trình
tinh_toan()
