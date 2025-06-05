import joblib
import numpy as np

# Load mô hình đã huấn luyện
model = joblib.load("device_detector.pkl")

# Dữ liệu mới (thay bằng giá trị thực từ wifi_scan.py và audio_capture.py)
new_data = [[-68, 3.0, 14000]]  # [mean_rssi, rssi_std, dominant_freq]

prediction = model.predict(new_data)
print("⚡ Có thiết bị gần đó!" if prediction[0] == 1 else "🔍 Không phát hiện thiết bị")