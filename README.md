# MSI SmartGuard Terminal System

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Library-OpenCV%20%7C%20PyZBar-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-Computer%20Vision-blue?style=for-the-badge" />
</p>
<br>

An automated Resident Access Control System built with Python, featuring real-time QR code recognition, data validation, and secure logging.

## ✨ Technical Architecture & Key Features

### 1️⃣ Resident Registration (qrcode)
* **Input Validation:** Uses Regex to ensure unit numbers follow the building format (e.g., A-10-05).
* **Logical Constraints:** Automatically rejects units above Floor 43 or Room 19.
* **Uniqueness Check:** Prevents duplicate registrations by cross-referencing the database.
* **Auto-Categorization:** Saves generated QR images into block-specific folders (e.g., `storehouse/Block-A/`).

### 2️⃣ Intelligent QR Scanner (pyzbar)
* **Real-time Recognition:** Powered by OpenCV and PyZBar for high-speed scanning.
* **Authorization Logic:** Instant visual feedback (Green for Authorized, Red for Un-authorized).
* **Anti-Spam Cooldown:** Prevents multiple logs for the same person within a 5-second window.
* **Smart Auto-Quit:** Automatically closes the scanner after 40 seconds of inactivity to save power.

### 3️⃣ Logging Information
* **CSV Database:** Maintains a permanent record of all entries (Unit, Name, DateTime).
* **Status Monitoring:** Logs both successful entries and unauthorized attempts for security auditing.
<br>

## 🛠️ Technical Stack
| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **Computer Vision** |  OpenCV (`cv2`) |
| **Decoder** | PyZBar |
| **Data Processing** | NumPy, Regex |
| **Storage** | CSV (Flat-file database) |
<br>

## 📂 Project Structure
```text
├── CSV/
│   ├── authorized_users.csv  # Registered resident database
│   └── permissions.csv       # Access history logs
├── storehouse/               # Generated QR ID passes
│   ├── Block-A/
│   └── Block-B/
├── main.py                   # Main application logic
└── requirements.txt          # Project dependencies
```
<br>

## 🚀 Getting Started

To enjoy the full interactive experience of **MSI SmartGuard**, please follow these setup steps:


### <code> Step 1:</code> Prerequisites
Navigate to the Project Directory: Open your terminal and move into the project folder. If you renamed the folder after cloning, use your custom name:

```bash
cd SmartGuard-QR
```


### <code> Step 2:</code> Prerequisites
Ensure you have **Python 3.x** installed. You can install all necessary dependencies at once using the provided requirements file:

```bash
pip install -r requirements.txt
```

### <code>Step 3:</code> Camera Access & Configuration

To ensure the scanner functions correctly, please check the following:

* **Hardware Activation:** Ensure your camera is physically enabled. On many laptops (especially **MSI** or **Lenovo**), you may need to press `FN + F6` or toggle a physical privacy switch.
* **Camera Index Configuration:** If you are using an external webcam or have multiple cameras, you may need to adjust the camera index in the code.
  * In `main.py`, locate: 
    ```python
    cap = cv2.VideoCapture(1)
    ```
  * If the wrong camera opens, change `0` to `1` (or 2,3,4...etc) to select the correct device.
* **Privacy Settings:** Ensure that "Camera Access" is enabled in your Windows/macOS Privacy Settings for desktop applications.

### <code> Step 4:</code> QR Quit Method

Exit Scanner: To close the **QR scanner window**, click on the video feed window and press the 'q' key on your keyboard
<br>
<br><br><br>

## Demo Display
<img width="475" height="594" alt="image" src="https://github.com/user-attachments/assets/cb3b8c52-3695-41ba-aa8e-a340e5a4e87d" />
<br><br>

<img width="1533" height="916" alt="image" src="https://github.com/user-attachments/assets/5786b4a8-725e-4cb0-8469-1c1950d50352" />
<br><br>

<img width="623" height="471" alt="image" src="https://github.com/user-attachments/assets/324b184b-1ef5-4cb9-918a-e71c2936afa5" />
<br><br>

<img width="584" height="272" alt="image" src="https://github.com/user-attachments/assets/0c9d818c-73df-4a06-baa0-97eb892e8b71" />
<br><br><br>


## Contact
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/steven0908)
[![Jobstreet](https://img.shields.io/badge/Jobstreet-003580?style=for-the-badge&logo=target&logoColor=white)](https://my.jobstreet.com/profiles/steven-gohyishen-97x9Q8tbmm)

> **Personal Project** &nbsp; | &nbsp; Completed on Apr 20, 2026 
