import pywifi
import time

def scan_wifi_details():
    """
    Quét Wi-Fi và trả về một danh sách các thiết bị,
    mỗi thiết bị là một dictionary chứa bssid, signal, và ssid.
    """
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        
        iface.scan()
        time.sleep(2.5) # Tăng thời gian chờ lên một chút
        
        scan_results = iface.scan_results()
        
        devices = []
        # --- PHẦN GỠ LỖI ---
        print("\n[DEBUG] Các BSSID quét được trong lần này:")
        if not scan_results:
            print("  => Không có mạng nào được tìm thấy.")
        else:
            for ap in scan_results:
                # In ra để chúng ta xem
                print(f"  - SSID: {ap.ssid}, BSSID: {ap.bssid.lower()}, Signal: {ap.signal}")
                devices.append({
                    # Luôn chuyển BSSID về chữ thường để so sánh đồng nhất
                    'bssid': ap.bssid.lower(),
                    'signal': ap.signal,
                    'ssid': ap.ssid
                })
        print("--------------------------------------")
        return devices
    except Exception as e:
        print(f"Lỗi khi quét Wi-Fi: {e}")
        return []