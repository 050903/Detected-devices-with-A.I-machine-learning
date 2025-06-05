import sounddevice as sd
import numpy as np
from scipy.fft import fft
import sys

# Sử dụng khối try-except để bắt lỗi import config
try:
    from .config import AUDIO_DURATION, SAMPLE_RATE
except ImportError:
    # Nếu chạy file này độc lập, sử dụng giá trị mặc định
    print("Cảnh báo: Không thể import config. Sử dụng giá trị mặc định cho audio.", file=sys.stderr)
    AUDIO_DURATION = 2
    SAMPLE_RATE = 44100

# Đảm bảo tên hàm được định nghĩa chính xác là "get_audio_features"
def get_audio_features():
    """Ghi âm và trả về tần số và biên độ nổi bật nhất."""
    try:
        # Dòng print này giúp xác nhận hàm được gọi
        print("Đang ghi âm...")
        recording = sd.rec(int(AUDIO_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        audio_data = recording.flatten()

        if audio_data is None or np.sum(np.abs(audio_data)) == 0:
            print("Không có tín hiệu âm thanh được ghi lại.")
            return 0, 0

        # Phân tích FFT
        N = len(audio_data)
        if N == 0:
            return 0, 0
            
        yf = fft(audio_data)
        xf = np.fft.fftfreq(N, 1 / SAMPLE_RATE)
        
        # Chỉ lấy nửa đầu của kết quả (phần dương)
        positive_mask = xf > 0
        xf_pos = xf[positive_mask]
        yf_pos = np.abs(yf[positive_mask])

        if len(yf_pos) == 0:
            return 0, 0

        # Tìm tần số nổi bật (bỏ qua thành phần DC ở gần 0 Hz nếu có)
        # Bắt đầu tìm từ index 1 để tránh nhiễu DC
        if len(yf_pos) > 1:
            dominant_freq_index = np.argmax(yf_pos[1:]) + 1
        else:
            dominant_freq_index = np.argmax(yf_pos)
            
        dominant_freq = xf_pos[dominant_freq_index]
        max_amplitude = yf_pos[dominant_freq_index]

        return dominant_freq, max_amplitude
    except Exception as e:
        print(f"Lỗi khi xử lý âm thanh: {e}", file=sys.stderr)
        return 0, 0

# Phần này để bạn có thể test file này một cách độc lập
if __name__ == '__main__':
    print("\n--- Chạy kiểm tra file audio_processor.py ---")
    freq, amp = get_audio_features()
    if freq is not None:
        print(f"\nKết quả kiểm tra:")
        print(f"  - Tần số nổi bật: {freq:.2f} Hz")
        print(f"  - Biên độ tối đa: {amp:.2f}")
    else:
        print("Kiểm tra thất bại.")