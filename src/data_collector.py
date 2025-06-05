import pandas as pd
import os
import time
import numpy as np
from .config import DATA_PATH
from .wifi_scanner import scan_wifi_details
from .audio_processor import get_audio_features

def collect_fingerprint(label):
    """Thu thập một 'vân tay' dữ liệu hoàn chỉnh cho một nhãn cụ thể."""
    print("\nĐang thu thập dữ liệu...")
    
    wifi_devices = scan_wifi_details()
    dominant_freq, max_amplitude = get_audio_features()
    
    if not wifi_devices:
        print("Không thể thu thập dữ liệu Wi-Fi. Bỏ qua điểm dữ liệu này.")
        return None

    # Trích xuất các đặc trưng từ dữ liệu Wi-Fi
    signals = [d['signal'] for d in wifi_devices]
    mean_rssi = np.mean(signals) if signals else -100
    std_rssi = np.std(signals) if signals else 0
    num_aps = len(wifi_devices)
    
    fingerprint = {
        'mean_rssi': mean_rssi,
        'std_rssi': std_rssi,
        'num_access_points': num_aps,
        'dominant_freq': dominant_freq,
        'max_amplitude': max_amplitude,
        'device_label': label
    }
    
    print(f"Đã thu thập: {fingerprint}")
    return fingerprint

def main():
    """Vòng lặp chính để thu thập dữ liệu 'vân tay'."""
    data_records = []
    
    if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
        df_existing = pd.read_csv(DATA_PATH)
        data_records = df_existing.to_dict('records')
        print(f"Đã tải {len(data_records)} bản ghi cũ.")

    while True:
        label = input("\nNhập nhãn cho thiết bị (vd: 'background', 'my_iphone', 'dell_laptop', 'q' để thoát): ").strip()
        if label.lower() == 'q':
            break
        if not label:
            print("Nhãn không được để trống.")
            continue
            
        point = collect_fingerprint(label)
        if point:
            data_records.append(point)
            
        time.sleep(1)

    if data_records:
        df = pd.DataFrame(data_records)
        df.to_csv(DATA_PATH, index=False)
        print(f"\nĐã lưu tổng cộng {len(df)} bản ghi vào '{DATA_PATH}'")

if __name__ == '__main__':
    main()