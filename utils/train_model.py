import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

import joblib

# Tạo dữ liệu giả lập (thay bằng dữ liệu thực của bạn)
data = {
    "mean_rssi": [-65, -70, -80, -75],
    "rssi_std": [3.2, 2.8, 1.5, 4.0],
    "dominant_freq": [15000, 12000, 500, 18000],
    "label": [1, 1, 0, 1]  # 1: Có thiết bị, 0: Không có
}
df = pd.DataFrame(data)

# Huấn luyện mô hình
model = MLPClassifier(hidden_layer_sizes=(100, 50))  # Dùng neural network
model.fit(df.drop("label", axis=1), df["label"])

# Lưu mô hình
joblib.dump(model, "device_detector.pkl")
print("Đã huấn luyện và lưu mô hình!")