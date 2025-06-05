import pywifi
from pywifi import const
import time
import pandas as pd

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def scan_wifi():
    iface.scan()
    time.sleep(2)
    results = iface.scan_results()
    return [ap.signal for ap in results]  # Lấy giá trị RSSI

# Quét và lưu dữ liệu
rssi_values = scan_wifi()
pd.DataFrame({"rssi": rssi_values}).to_csv("wifi_data.csv", index=False)
print("Đã lưu dữ liệu Wi-Fi vào wifi_data.csv")