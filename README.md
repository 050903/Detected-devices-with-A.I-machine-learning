# Advanced Device Detector

## Description

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