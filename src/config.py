import os
import json

# Lấy đường dẫn thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Định nghĩa các đường dẫn khác dựa trên BASE_DIR
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Đường dẫn đến file dữ liệu, model và file hiệu chuẩn
DATA_PATH = os.path.join(DATA_DIR, 'device_fingerprints.csv')
MODEL_PATH = os.path.join(MODELS_DIR, 'device_identifier.pkl')
CALIBRATION_PATH = os.path.join(BASE_DIR, 'calibration_data.json')

# Đảm bảo các thư mục tồn tại
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Cấu hình Audio
AUDIO_DURATION = 2
SAMPLE_RATE = 44100

# Hàm tải dữ liệu hiệu chuẩn
def load_calibration_data():
    """Tải dữ liệu hiệu chuẩn từ file JSON."""
    if not os.path.exists(CALIBRATION_PATH):
        # Trả về giá trị mặc định nếu file không tồn tại
        return {'A_at_1m': -45, 'n_path_loss': 3.0}
    with open(CALIBRATION_PATH, 'r') as f:
        return json.load(f)

# Hàm lưu dữ liệu hiệu chuẩn
def save_calibration_data(data):
    """Lưu dữ liệu hiệu chuẩn vào file JSON."""
    with open(CALIBRATION_PATH, 'w') as f:
        json.dump(data, f, indent=4)