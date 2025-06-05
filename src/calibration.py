import time
import numpy as np
import sys

# In ra để xác nhận script được thực thi
print("--- [DEBUG] Bắt đầu thực thi script calibration.py ---")

try:
    from .wifi_scanner import scan_wifi_details
    from .config import save_calibration_data
except ImportError as e:
    print(f"\nLỖI IMPORT: {e}", file=sys.stderr)
    sys.exit(1)

def calibrate():
    """Thực hiện quá trình hiệu chuẩn để xác định hằng số A và n."""
    print("\n--- BẮT ĐẦU QUÁ TRÌNH HIỆU CHUẨN KHOẢNG CÁCH ---")
    
    print("\n[BƯỚC 1]: Đo RSSI tại khoảng cách 1 mét.")
    
    target_bssid = ""
    while not target_bssid:
        prompt = "VUI LÒNG ĐẶT THIẾT BỊ MỤC TIÊU CÁCH 1 MÉT VÀ NHẬP ĐỊA CHỈ BSSID CỦA NÓ: "
        target_bssid = input(prompt).strip().lower()
        if not target_bssid:
            print("Lỗi: BSSID không được để trống. Vui lòng nhập lại.")

    print(f"\nOK. Đang tìm kiếm BSSID: {target_bssid}. Vui lòng giữ yên thiết bị...")
    
    rssi_at_1m_samples = []
    # Vòng lặp for này phải thẳng hàng với dòng print ở trên
    for i in range(10):
        print(f"Lấy mẫu lần {i+1}/10...")
        devices = scan_wifi_details()
        found = False
        
        # Vòng lặp for này phải thụt vào so với vòng lặp cha
        for device in devices:
            # SỬA LỖI: Loại bỏ ký tự thừa ở cuối BSSID
            cleaned_bssid = device['bssid'].lower().strip().rstrip(':')
            
            # Khối if này phải thụt vào so với vòng lặp cha
            if cleaned_bssid == target_bssid:
                rssi_at_1m_samples.append(device['signal'])
                print(f"  => Tìm thấy! RSSI: {device['signal']}")
                found = True
                break # Thoát khỏi vòng lặp device
                
        if not found:
            print(f"  => Không tìm thấy BSSID trong lần quét này.")
        time.sleep(1)

    if not rssi_at_1m_samples:
        print("\n--- THẤT BẠI ---")
        print("Không thể thu thập bất kỳ mẫu RSSI nào cho thiết bị này. Vui lòng kiểm tra lại BSSID và thử lại.")
        return
        
    a_at_1m = np.mean(rssi_at_1m_samples)
    print(f"\n[KẾT QUẢ BƯỚC 1] RSSI trung bình tại 1 mét (A) là: {a_at_1m:.2f}")

    n_path_loss = 0.0
    while n_path_loss <= 0:
        try:
            prompt_n = "\n[BƯỚC 2]: NHẬP HỆ SỐ SUY HAO MÔI TRƯỜNG (n) (ví dụ: 2.0 cho không gian mở, 3.0-4.0 cho trong nhà): "
            n_path_loss = float(input(prompt_n))
            if n_path_loss <= 0:
                print("Lỗi: Hệ số suy hao phải là một số dương.")
        except ValueError:
            print("Lỗi: Vui lòng nhập một con số (ví dụ: 3.0).")

    calibration_data = {
        'target_bssid_for_distance': target_bssid,
        'A_at_1m': a_at_1m,
        'n_path_loss': n_path_loss
    }
    
    save_calibration_data(calibration_data)
    print("\n--- HIỆU CHUẨN HOÀN TẤT! ---")
    print(f"Dữ liệu đã được lưu thành công vào file 'calibration_data.json'.")


# Đảm bảo hàm calibrate() được gọi khi chạy script
if __name__ == "__main__":
    calibrate()