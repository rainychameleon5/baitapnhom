import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Khởi tạo các biến toàn cục
df = None  # Dữ liệu sẽ được tải lên ở đây
X_train, X_test, y_train, y_test = None, None, None, None
models = {}  # Tạo từ điển để lưu mô hình của từng thuật toán
error_metrics = {}  # Tạo từ điển để lưu thông tin sai số của từng thuật toán


# Hàm để tải lên file dữ liệu
def load_data():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        df = pd.read_csv(filepath)
        messagebox.showinfo("Load Data", "Data loaded successfully!")
    else:
        messagebox.showwarning("Load Data", "No file selected.")


# Hàm huấn luyện mô hình
def train_model():
    global X_train, X_test, y_train, y_test, models

    if df is None:
        messagebox.showerror("Train Error", "Please load the data first.")
        return

    # Lấy tập đặc trưng (X) và nhãn (y)
    X = df.iloc[:, :5]  # Lấy cột từ 0 đến 4 làm đặc trưng
    y = df.iloc[:, 5]  # Cột thứ 6 là nhãn (Performance Index)

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Lựa chọn thuật toán
    algorithm = selected_algorithm.get()

    # Huấn luyện mô hình dựa trên thuật toán đã chọn
    if algorithm == "KNN":
        model = KNeighborsRegressor(n_neighbors=3, p=2)
    elif algorithm == "Linear Regression":
        model = LinearRegression()
    elif algorithm == "Decision Tree":
        model = DecisionTreeRegressor()
    elif algorithm == "SVM":
        model = SVR()

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Tính toán sai số
    y_predict = model.predict(X_test)
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Lưu mô hình và thông số sai số cho thuật toán
    models[algorithm] = model
    error_metrics[algorithm] = {'MSE': mse, 'MAE': mae, 'RMSE': rmse}

    # Hiển thị kết quả sau khi huấn luyện
    result_text.set(f"Model ({algorithm}) trained successfully!\n"
                    f"MSE: {mse:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")


# Hàm kiểm tra và hiển thị sai số, đồ thị
def test_model():
    if X_test is None or y_test is None:
        messagebox.showerror("Test Error", "Please train the model first.")
        return

    # Vẽ biểu đồ so sánh sai số giữa các thuật toán
    algorithms = list(error_metrics.keys())
    mse_values = [error_metrics[alg]['MSE'] for alg in algorithms]
    mae_values = [error_metrics[alg]['MAE'] for alg in algorithms]
    rmse_values = [error_metrics[alg]['RMSE'] for alg in algorithms]

    x = np.arange(len(algorithms))  # vị trí trên trục x

    plt.figure(figsize=(10, 6))
    plt.bar(x - 0.2, mse_values, width=0.2, label='MSE', color='blue')
    plt.bar(x, mae_values, width=0.2, label='MAE', color='orange')
    plt.bar(x + 0.2, rmse_values, width=0.2, label='RMSE', color='green')

    plt.xlabel('Thuật toán')
    plt.ylabel('Giá trị sai số')
    plt.title('So sánh sai số giữa các thuật toán')
    plt.xticks(x, algorithms)
    plt.legend()
    plt.show()


# Hàm dự đoán dữ liệu mới
def predict_new():
    try:
        if not models:
            messagebox.showerror("Prediction Error", "Please train the models first.")
            return

        # Lấy dữ liệu nhập từ giao diện
        hours_studied = float(entry_hours_studied.get())
        previous_scores = float(entry_previous_scores.get())
        extracurricular_activities = float(entry_extracurricular_activities.get())
        sleep_hours = float(entry_sleep_hours.get())
        sample_question_papers_practiced = float(entry_sample_question_papers_practiced.get())

        # Kiểm tra giá trị âm
        if hours_studied < 0 or previous_scores < 0 or extracurricular_activities < 0 or sleep_hours < 0 or sample_question_papers_practiced < 0:
            raise ValueError("Input values cannot be negative.")

        # Chuẩn bị dữ liệu đầu vào
        new_student_data = pd.DataFrame([[hours_studied, previous_scores, extracurricular_activities, sleep_hours,
                                          sample_question_papers_practiced]],
                                        columns=['Hours Studied', 'Previous Scores', 'Extracurricular Activities',
                                                 'Sleep Hours', 'Sample Question Papers Practiced'])

        # Dự đoán kết quả cho từng mô hình
        results = []
        for algorithm, model in models.items():
            predicted_performance = model.predict(new_student_data)
            results.append((algorithm, predicted_performance[0]))

        # Hiển thị kết quả dự đoán
        prediction_result = "\n".join([f"{alg}: Predicted Performance Index = {pred:.2f}" for alg, pred in results])
        messagebox.showinfo("Prediction Results", prediction_result)

    except ValueError as ve:
        messagebox.showerror("Input Error", f"Error: {ve}")


# Tạo giao diện với tkinter
root = tk.Tk()
root.title("Student Performance Predictor")

# Tạo các nút và giao diện cho các phần khác nhau
tk.Button(root, text="Load Data", command=load_data).grid(row=0, column=0)

# Tùy chọn thuật toán
selected_algorithm = tk.StringVar(value="KNN")
tk.Label(root, text="Select Algorithm:").grid(row=1, column=0)
tk.Radiobutton(root, text="KNN", variable=selected_algorithm, value="KNN").grid(row=1, column=1)
tk.Radiobutton(root, text="Linear Regression", variable=selected_algorithm, value="Linear Regression").grid(row=1, column=2)
tk.Radiobutton(root, text="Decision Tree", variable=selected_algorithm, value="Decision Tree").grid(row=1, column=3)
tk.Radiobutton(root, text="SVM", variable=selected_algorithm, value="SVM").grid(row=1, column=4)

# Nút để huấn luyện mô hình
tk.Button(root, text="Train", command=train_model).grid(row=2, column=0)

# Nút kiểm tra và hiển thị sai số, đồ thị
tk.Button(root, text="Compare", command=test_model).grid(row=3, column=0)

# Hiển thị sai số sau khi test
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).grid(row=4, column=0, columnspan=3)

# Nhập liệu mới cho việc dự đoán
tk.Label(root, text="Hours Studied:").grid(row=5, column=0)
entry_hours_studied = tk.Entry(root)
entry_hours_studied.grid(row=5, column=1)

tk.Label(root, text="Previous Scores:").grid(row=6, column=0)
entry_previous_scores = tk.Entry(root)
entry_previous_scores.grid(row=6, column=1)

tk.Label(root, text="Extracurricular Activities:").grid(row=7, column=0)
entry_extracurricular_activities = tk.Entry(root)
entry_extracurricular_activities.grid(row=7, column=1)


tk.Label(root, text="Sleep Hours:").grid(row=8, column=0)
entry_sleep_hours = tk.Entry(root)
entry_sleep_hours.grid(row=8, column=1)


tk.Label(root, text="Sample Question Papers Practiced:").grid(row=9, column=0)
entry_sample_question_papers_practiced = tk.Entry(root)
entry_sample_question_papers_practiced.grid(row=9, column=1)

# Nút để dự đoán dữ liệu mới
tk.Button(root, text="Predict New", command=predict_new).grid(row=10, column=0)

# Bắt đầu giao diện
root.mainloop()
