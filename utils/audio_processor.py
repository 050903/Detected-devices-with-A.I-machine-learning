import sounddevice as sd
import numpy as np
from scipy.fft import fft

def record_audio(duration=5, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    return recording.flatten()

def analyze_audio(audio_data):
    fft_result = np.abs(fft(audio_data)[:len(audio_data)//2])
    dominant_freq = np.argmax(fft_result)
    return dominant_freq, np.max(fft_result)

if __name__ == "__main__":
    audio = record_audio()
    freq, amplitude = analyze_audio(audio)
    print(f"Dominant Frequency: {freq} Hz, Amplitude: {amplitude}")