import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import joblib
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import MODEL_PATH, load_calibration_data
from src.wifi_scanner import scan_wifi_details
from src.audio_processor import get_audio_features

def estimate_distance(rssi, a_at_1m, n_path_loss):
    """Ước tính khoảng cách dựa trên mô hình Path Loss."""
    if rssi == 0 or n_path_loss == 0:
        return float('inf')
    return 10 ** ((a_at_1m - rssi) / (10 * n_path_loss))

class AdvancedDeviceDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Device Detector")
        self.root.geometry("500x450")

        self.model_bundle = None
        self.is_detecting = False
        self.detection_thread = None
        self.calibration_data = load_calibration_data()

        # --- UI Elements ---
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        self.style.configure("Result.TLabel", font=("Helvetica", 12, "bold"))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        self.toggle_button = ttk.Button(control_frame, text="Bắt đầu phát hiện", command=self.toggle_detection)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Kết quả phát hiện", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Device Count
        ttk.Label(results_frame, text="Số lượng thiết bị Wi-Fi:", style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.device_count_label = ttk.Label(results_frame, text="N/A", style="Result.TLabel", foreground="blue")
        self.device_count_label.grid(row=0, column=1, sticky="w")

        # Identified Device
        ttk.Label(results_frame, text="Thiết bị nhận dạng:", style="Header.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.identified_device_label = ttk.Label(results_frame, text="N/A", style="Result.TLabel", foreground="green")
        self.identified_device_label.grid(row=1, column=1, sticky="w")

        # Confidence
        ttk.Label(results_frame, text="Độ tin cậy:", style="Header.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.confidence_label = ttk.Label(results_frame, text="N/A", style="Result.TLabel", foreground="black")
        self.confidence_label.grid(row=2, column=1, sticky="w")
        
        # Distance
        ttk.Label(results_frame, text="Khoảng cách ước tính:", style="Header.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.distance_label = ttk.Label(results_frame, text="N/A", style="Result.TLabel", foreground="purple")
        self.distance_label.grid(row=3, column=1, sticky="w")

        # Raw data list
        self.raw_list_label = ttk.Label(results_frame, text="Các thiết bị quét được:")
        self.raw_list_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(15, 0))
        self.raw_list = tk.Listbox(results_frame, height=6, font=("Courier New", 9))
        self.raw_list.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.load_model()

    def load_model(self):
        try:
            self.model_bundle = joblib.load(MODEL_PATH)
            messagebox.showinfo("Thông báo", "Mô hình đã được tải thành công.")
        except FileNotFoundError:
            messagebox.showwarning("Cảnh báo", f"Không tìm thấy file model. Vui lòng huấn luyện trước.")

    def toggle_detection(self):
        if self.is_detecting:
            self.is_detecting = False
            self.toggle_button.config(text="Bắt đầu phát hiện")
        else:
            if not self.model_bundle:
                messagebox.showerror("Lỗi", "Không thể bắt đầu vì chưa có mô hình.")
                return
            self.is_detecting = True
            self.toggle_button.config(text="Dừng phát hiện")
            self.detection_thread = threading.Thread(target=self.detect_loop, daemon=True)
            self.detection_thread.start()

    def detect_loop(self):
        model = self.model_bundle['model']
        le = self.model_bundle['label_encoder']
        target_bssid = self.calibration_data.get('target_bssid_for_distance')

        while self.is_detecting:
            # 1. Thu thập dữ liệu
            wifi_devices = scan_wifi_details()
            dominant_freq, max_amplitude = get_audio_features()

            if not wifi_devices:
                time.sleep(2)
                continue

            # 2. Cập nhật số lượng thiết bị
            num_devices = len(wifi_devices)
            self.device_count_label.config(text=f"{num_devices}")
            self.raw_list.delete(0, tk.END)
            for dev in wifi_devices[:10]: # Hiển thị 10 thiết bị đầu
                self.raw_list.insert(tk.END, f"BSSID: {dev['bssid']} | RSSI: {dev['signal']}")
            
            # 3. Chuẩn bị dữ liệu cho mô hình nhận dạng
            signals = [d['signal'] for d in wifi_devices]
            current_fingerprint = pd.DataFrame([[
                np.mean(signals), np.std(signals), len(wifi_devices),
                dominant_freq, max_amplitude
            ]], columns=model.feature_names_in_)

            # 4. Dự đoán và cập nhật UI
            prediction_encoded = model.predict(current_fingerprint)[0]
            prediction_label = le.inverse_transform([prediction_encoded])[0]
            proba = model.predict_proba(current_fingerprint)
            confidence = np.max(proba)

            self.identified_device_label.config(text=prediction_label)
            self.confidence_label.config(text=f"{confidence:.1%}")

            # 5. Ước tính khoảng cách
            distance = "N/A (Chưa hiệu chuẩn)"
            if target_bssid:
                target_device = next((d for d in wifi_devices if d['bssid'] == target_bssid), None)
                if target_device:
                    dist_val = estimate_distance(
                        target_device['signal'], 
                        self.calibration_data['A_at_1m'], 
                        self.calibration_data['n_path_loss']
                    )
                    distance = f"{dist_val:.2f} mét"
                else:
                    distance = "Mục tiêu ngoài tầm quét"
            
            self.distance_label.config(text=distance)
            
            time.sleep(3)
        
        # Reset labels when stopped
        self.device_count_label.config(text="N/A")
        self.identified_device_label.config(text="N/A")
        self.confidence_label.config(text="N/A")
        self.distance_label.config(text="N/A")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedDeviceDetectorApp(root)
    root.mainloop()