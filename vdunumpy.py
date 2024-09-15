import numpy as np


def lay_phan_tu_ma_tran(hang, cot):
    """Hàm để nhập các phần tử và kiểm tra định dạng đúng."""
    while True:
        try:
            print(f"Nhập các phần tử cho ma trận dạng mảng 1 chiều (phải có {hang * cot} phần tử):")
            phantu = list(map(float, input().split()))
            if len(phantu) != hang * cot:
                print(f"Số lượng phần tử phải là {hang * cot}, nhưng bạn đã nhập {len(phantu)} phần tử.Mời nhập lại")
            return np.array(phantu).reshape(hang, cot)
        except ValueError :
            print(f"Lỗi không đúng định dạng. Vui lòng nhập lại.")

def nghich_dao_ma_tran(matran):
    """Tính nghịch đảo"""
    try:
        if hang != cot:
            raise ValueError("Ma trận vuông mới có thể tính nghịch đảo")
        nghich_dao = np.linalg.inv(matran) #Tính nghịch đảo
        return nghich_dao
    except np.linalg.LinAlgError: #Khi không có nghịch đảo, numpy sinh lỗi np.linalg.LinAlgError
        raise ValueError("Ma trận không khả nghịch.")
    except ValueError as loi:
        raise ValueError(loi)

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

#Chọn các ma trận trong danh sách để cộng
while True:
    try:
        chon = list(map(int, input(f"Nhập các ma trận cần cộng (1 đến {n}): ").split()))
        if any(i < 1 or i > n for i in chon):
            raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")
        break
    except ValueError:
        print(f"Lỗi: Vị trí không phù hợp.Vui lòng nhập lại.")

# Lấy các ma trận được chỉ định từ dsach
dsach_cong = [dsach[i-1] for i in chon]

# Thực hiện phép cộng các ma trận (chỉ cộng khi các ma trận có cùng kích thước)
kich_thuoc_dong_nhat = all(mat.shape == dsach_cong[0].shape for mat in dsach_cong)


if kich_thuoc_dong_nhat:
    tong_matran = np.sum(dsach_cong, axis=0)  # Thực hiện phép cộng từng phần tử của các ma trận
    print("\nTổng của các ma trận:")
    print(tong_matran)
else:
    print("Không thể thực hiện phép cộng vì các ma trận có kích thước khác nhau.")
# Chọn các ma trận trong danh sách để nhân                                                           
while True:                                                                                          
    try:                                                                                             
        chon_nhan = list(map(int, input(f"Nhập các ma trận cần nhân (1 đến {n}): ").split()))        
        if any(i < 1 or i > n for i in chon_nhan):                                                   
            raise ValueError("Vị trí ma trận phải nằm trong khoảng hợp lệ.")                         
        break                                                                                        
    except ValueError:                                                                               
        print(f"Lỗi: Vị trí không phù hợp. Vui lòng nhập lại.")                                      
                                                                                                     
# Lấy các ma trận được chỉ định từ dsach                                                             
dsach_nhan = [dsach[i-1] for i in chon_nhan]                                                         
                                                                                                     
# Thực hiện phép nhân các ma trận (chỉ nhân khi kích thước phù hợp)                                  
def nhan_ma_tran(dsach):                                                                             
    """Nhân các ma trận trong danh sách."""                                                          
    try:                                                                                             
        ket_qua = dsach[0]                                                                           
        for matran in dsach[1:]:                                                                     
            if ket_qua.shape[1] != matran.shape[0]:                                                  
                raise ValueError("Số cột của ma trận trước không bằng số hàng của ma trận sau.")     
            ket_qua = np.dot(ket_qua, matran)  # Nhân ma trận                                        
        return ket_qua                                                                               
    except ValueError as loi:                                                                        
        raise ValueError(loi)  
kqua_nhan = nhan_ma_tran(dsach_nhan)
if kqua_nhan is not None:
    print("\nKết quả của phép nhân các ma trận là:")
    print(kqua_nhan)
    
#In nghịch đảo các ma trận
for i, matr in enumerate(dsach):
    print(f"\r\nNghịch đảo ma trận {i+1}: ")
    try:
        nghichdao = nghich_dao_ma_tran(matr)
        print(nghichdao)
    except ValueError as loi:
        print(f"Không có ma trận nghịch đảo cho ma trận {i+1}")
