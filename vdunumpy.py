#ví dụ ứng dụng numpy trong tính toán ma trận ( phép cộng, phép nhân, nghịch đảo, định thức )
import numpy as np

class MaTran():
    def __init__(self, ten_ma_tran):
        self.ten_ma_tran = ten_ma_tran
        self.ma_tran = self.nhap_ma_tran()

    def nhap_ma_tran(self):
        # Nhập số hàng và số cột của ma trận
        hang = int(input(f"Nhập số hàng của ma trận {self.ten_ma_tran}: "))
        cot = int(input(f"Nhập số cột của ma trận {self.ten_ma_tran}: "))

        # Tạo một ma trận rỗng
        ma_tran = []

        # Nhập từng phần tử của ma trận
        print(f"Nhập các phần tử cho ma trận {self.ten_ma_tran} (theo từng hàng):")
        for i in range(hang):
            hang_moi = list(map(float, input(f"Nhập hàng {i+1} (cách nhau bằng dấu cách): ").split()))
            while len(hang_moi) != cot:  # Đảm bảo số phần tử đúng với số cột
                print(f"Sai số cột! Hãy nhập lại hàng {i+1} với đúng {cot} phần tử.")
                hang_moi = list(map(float, input(f"Nhập hàng {i+1} (cách nhau bằng dấu cách): ").split()))
            ma_tran.append(hang_moi)

        return np.array(ma_tran)

    def hien_thi_ma_tran(self):
        print(f"Ma trận {self.ten_ma_tran}:")
        print(self.ma_tran)

def main():
    # Nhập ma trận A và B
    ma_tran_a = MaTran("A")
    ma_tran_b = MaTran("B")

    # Hiển thị ma trận A và B
    ma_tran_a.hien_thi_ma_tran()
    ma_tran_b.hien_thi_ma_tran()

if __name__ == "__main__":
    main()
