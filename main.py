import cv2
import numpy as np
import qrcode
from pyzbar.pyzbar import decode
import datetime
import os
import winsound
import re



LOG_FILE = "permissions.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Unit, Name, Date, Time\n")

# --- INPUT & GENERATE QR ---
def register_resident():
    unit = input("\nEnter resident Unit: ").strip().upper()
    name = input("Enter resident name: ").strip()

    if not re.match(r'^[A-Z]-\d+-\d+', unit):
        print("Invalid format, Use (A-xx-xx)")
        return

    folder = f"storehouse/Block-{unit[0]}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    data = f"{unit} | {name}"
    img = qrcode.make(data)
    save_path = f"{folder}/{unit}_{name}.png"
    img.save(save_path)
    
    print(f"Success! ID saved to: {save_path}\n")

# --- SCANNER ---
def start_scanner():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    last_scanned = {}
    print("\n[INFO] Scanner starting... Press 'q' to stop scanning.\n")

    while True:
        success, frame = cap.read()
        if not success: break

        for code in decode(frame):
            raw_data = code.data.decode('utf-8')
            
            if " | " in raw_data:
                parts = raw_data.split(" | ")
                unit, name = parts[0], parts[1]
            else:
                unit, name = "Unknown", raw_data

            now = datetime.datetime.now()
            
            if name in last_scanned and (now - last_scanned[name]).total_seconds() < 5:
                color = (0, 0, 255)
                msg = "On Cooldown"
            else:
                winsound.Beep(1000, 200)
                with open(LOG_FILE, "a") as f:
                    f.write(f"{unit}, {name}, {now.strftime('%Y-%m-%d')}, {now.strftime('%H:%M:%S')}\n")
                
                last_scanned[name] = now
                color = (0, 255, 0)
                msg = f"Welcome {name}"
                print(f"Logged Success: {name}")


        cv2.imshow("Check-In System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# --- MAIN MENU LOOP ---
def main():
    while True:
        print("\n=== MSI RESIDENT SYSTEM ===")
        print("1. Enter Resident Input (Register)")
        print("2. Start QR Code Scanner")
        print("3. Exit Program")
        
        choice = input("\nSelect an option (1-3): ")

        if choice == "1":
            register_resident()
        elif choice == "2":
            start_scanner()
        elif choice == "3":
            print("Thanks for your join! Exiting program....")
            break
        else:
            print("Please enter between 1 to 3")


main()