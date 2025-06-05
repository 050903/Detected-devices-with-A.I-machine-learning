# Advanced Device Detector

## Description
=======
![image](https://github.com/user-attachments/assets/f8843bf7-4cb7-4844-97fc-f7ac81e5fded)# Detected-devices-with-A.I-machine-learning
# Advanced Device Detector folders structure
## Review process 
## Review process 
## Description
![image](https://github.com/user-attachments/assets/3fe6a136-ee37-42b1-ba4e-b8e69c20b30e)
![image](https://github.com/user-attachments/assets/ea313442-626d-46e6-b124-4f5d8e99bed0)
![image](https://github.com/user-attachments/assets/69418db8-4906-4823-8389-41a312ff4494)
![image](https://github.com/user-attachments/assets/192250d9-38c8-4ebe-bde1-f3e3448518c8)
![image](https://github.com/user-attachments/assets/6af5e0f3-6c27-4bbe-8126-6298ebe3d153)
![image](https://github.com/user-attachments/assets/91c34c3d-855e-45b0-8268-57b3bbd38310)
![image](https://github.com/user-attachments/assets/93024ae8-c8d5-42c5-a09d-9a9ac2091830)
![image](https://github.com/user-attachments/assets/cf456ce3-fcea-4a1f-919c-f06cf2f04b3d)
![image](https://github.com/user-attachments/assets/1b21c824-8064-4a08-883d-7de56ad542d2)
![image](https://github.com/user-attachments/assets/07a8ed17-8eb6-49b1-975b-eed7a0d851dc)
![image](https://github.com/user-attachments/assets/eb404b2e-5c34-42e9-8501-34b74822e6e8)
![image](https://github.com/user-attachments/assets/c38e6efb-ab21-4ab8-bdc3-ea2c93986144)
![image](https://github.com/user-attachments/assets/2fe150d2-acb5-4567-ad4a-59844b140ea5)
![image](https://github.com/user-attachments/assets/53e9cb37-86ad-489b-b46d-73b7666665ce)
![image](https://github.com/user-attachments/assets/168f0ce3-9e62-4839-9cb9-495348343467)
![image](https://github.com/user-attachments/assets/55f136bf-950a-4fcd-b3b8-bf60f152f37e)
![image](https://github.com/user-attachments/assets/ad3ad4eb-c0d6-41c9-b92e-ca62316efce4)
![image](https://github.com/user-attachments/assets/552b2f26-7045-4b41-99c6-c73f16ac9847)
![image](https://github.com/user-attachments/assets/ab5d9396-1a97-4eaf-9197-351c11f00d09)
![image](https://github.com/user-attachments/assets/01a65f4c-4ee2-4cbe-865f-ad5e0a7edda9)
![image](https://github.com/user-attachments/assets/b315f542-f1a4-4a45-80a2-e4a1e9c5f35c)
![image](https://github.com/user-attachments/assets/cf859923-877f-4216-9538-8ea3906262fb)
![image](https://github.com/user-attachments/assets/154c5c65-6d86-475a-8e18-1569c70777e7)
![image](https://github.com/user-attachments/assets/d30f5034-a0e3-4dd1-92ee-616f65018b49)
![image](https://github.com/user-attachments/assets/03459ca7-932e-4ba2-81bb-c48d3c36db4b)
![image](https://github.com/user-attachments/assets/10479d60-6892-4170-8798-cc51c63c476a)
![image](https://github.com/user-attachments/assets/6cf88e25-3159-4659-b69d-1dbafcf14dfd)

This is a Python application that combines Wi-Fi scanning data and audio analysis with a Machine Learning model to detect and identify nearby devices. The application provides a graphical user interface (GUI) to display the number of devices, identified devices, prediction confidence, and estimated distance to a target device.

## Technologies and Techniques Used

- **Language:** Python
- **Key Libraries:**
    - `tkinter`: Building the graphical user interface (GUI).
    - `joblib`: Loading and using the trained Machine Learning model.
    - `pandas`, `numpy`: Data processing and preparation.
    - `pywifi`: Scanning Wi-Fi network information.
    - `sounddevice`: Capturing audio data.
    - `scikit-learn`: Using Machine Learning models for device classification.
    - `threading`: Running the device detection in a background thread to not block the GUI.
    - Other libraries for data processing and GUI like `matplotlib`, `seaborn`, `plotly`, etc. (listed in detail in `requirements.txt`).
- **Techniques:**
    - Wi-Fi signal scanning (RSSI, BSSID).
    - Audio feature extraction (dominant frequency, maximum amplitude).
    - Data processing and preparation for the Machine Learning model.
    - Using Machine Learning models (likely classification models).
    - Distance estimation based on the Path Loss model from RSSI (requires calibration).

## How it Works

The application works in the following steps:

1.  **Initialization:** Load the trained Machine Learning model and calibration data (if available).
2.  **Data Collection:** Periodically scan for available Wi-Fi networks and collect audio data from the microphone.
3.  **Feature Extraction:** From Wi-Fi data (e.g., average RSSI, RSSI standard deviation, number of devices) and audio data (dominant frequency, amplitude), create a numerical 'fingerprint'.
4.  **Device Identification:** Use this 'fingerprint' as input for the Machine Learning model to predict the type of device or the current state of the environment.
5.  **Distance Estimation:** If a target BSSID is configured in the calibration data and found during Wi-Fi scanning, the application will estimate the distance based on the signal strength (RSSI) and calibration parameters.
6.  **UI Update:** Display the collected and predicted results on the graphical user interface in real-time.

The data collection and processing happen in a separate thread to ensure the user interface remains responsive.

## How to Run

To run this application, you need to have Python and the necessary libraries installed. Follow these steps:

1.  **Clone repository** (If the project is managed with Git):
    ```bash
    git clone <repo_address>
    cd device-detection
    ```
    (If you already have the files, skip this step and ensure you are in the project's root directory).

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install libraries from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
    Note: `pywifi` might require administrator privileges on some operating systems for Wi-Fi scanning.

5.  **Prepare model and calibration data:**
    - Ensure you have the trained model file (e.g., `model.pkl`) at the path specified in `src/config.py` (`MODEL_PATH`). If not, you need to run the model training process first.
    - Ensure you have the calibration data file (`calibration_data.json`) with the necessary parameters (e.g., `target_bssid_for_distance`, `A_at_1m`, `n_path_loss`) in the project's root directory or specified path.

6.  **Run the application:**
    ```bash
    python main.py
    ```

The GUI application will appear. Press the "Start Detection" button to begin the scanning and identification process.

## Author

Trần Thế Hảo
University Of Transport Ho Chi Minh City (UTH)

## License

This project is licensed under the MIT License. See the [LICENSE](#mit-license) file for details.

---

<a name="mit-license"></a>

## MIT License

Copyright (c) [Current Year] [Your Name or Copyright Holder]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
=======

