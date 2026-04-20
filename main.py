import cv2
import numpy as np
import qrcode
from pyzbar.pyzbar import decode
import datetime
import os
import winsound
import re
import time



LOG_FILE = "CSV/permissions.csv"
AUTHORIZED_FILE = "CSV/authorized_users.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        myDataList_LOG = f.write("Unit, Name, Date, Time\n")
if not os.path.exists(AUTHORIZED_FILE):
    with open(AUTHORIZED_FILE, "w") as f:
        f.write("Unit, Resident Name\n")

with open(AUTHORIZED_FILE, "r") as f:
    lines = f.read().splitlines()
    myDataList_AUTH = [line.replace(", ", " | ") for line in lines]



# --- INPUT & GENERATE QR ---
def register_resident():
    print("\n>>>> REGISTRATION MODE <<<<")
    unit = input("Enter resident Unit: ").strip().upper()
    name = input("Enter resident name: ").strip()

    if not re.match(r'^[A-Z]-\d{2}-\d{2}', unit):
        print("Invalid format, Use (A-xx-xx)")
        input("\n[Press Enter to return to menu]: ")
        return

    unit_parts = unit[1:].strip("-").split("-")
    floor = int(unit_parts[0])
    room = int(unit_parts[1])
    if floor > 43 or room > 19:
        print(f"Invalid unit number, Max is (A-43-19)")
        input("\n[Press Enter to return to menu]: ")
        return
    
    with open(AUTHORIZED_FILE, "r") as f:
        existing_data = f.read()
        
    if unit in existing_data:
        print(f"FAILED: Unit {unit} is already registered in the system!")
        input("\n[Press Enter to return to menu]: ")
        return
    
    folder = f"storehouse/Block-{unit[0]}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    data = f"{unit} | {name}"
    img = qrcode.make(data)
    save_path = f"{folder}/{unit}_{name}.png"
    img.save(save_path)
    
    with open(AUTHORIZED_FILE, "a") as f:
        f.write(f"{unit}, {name}\n")
    myDataList_AUTH.append(data)


    print("\n" + "=" * 40)
    print("      Success Resident Registered!")
    print("" + "=" * 40)
    print(f"  UNIT NUMBER    :  {unit}")
    print(f"  RESIDENT NAME  :  {name}")
    print("-" * 40)
    input("\n[Press Enter to return to menu]: ")
    return

# --- SCANNER ---
def start_scanner():
    if not os.path.exists("CSV"):
        os.makedirs("CSV")

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    last_scanned = {}
    last_seen_qr = time.time()
    print("\n[INFO] Scanner starting... Press 'q' to stop scanning.")
    print("[INFO] Auto-quit if no QR detected for 5 seconds.\n")

    

    while True:
        success, frame = cap.read()
        if not success: 
            print("[ERROR] Camera not found.")
            break

        codes = decode(frame)
        if codes:
            last_seen_qr = time.time()

        for code in codes:
            raw_data = code.data.decode('utf-8')

            raw_data = code.data.decode('utf-8')
            if raw_data in myDataList_AUTH:
                Output = "Authorized"
                color = (0, 255, 0)
            else:
                Output = "Un-Authorized"
                color = (0, 0, 255)

            pts = np.array([code.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            
            
            if " | " in raw_data:
                parts = raw_data.split(" | ")
                unit, name = parts[0], parts[1]
            else:
                unit, name = "Unknown", raw_data

            now = datetime.datetime.now()

            if name in last_scanned and (now - last_scanned[name]).total_seconds() < 5:
                ...
            else:
                winsound.Beep(1000, 200)
                with open(LOG_FILE, "a") as f:
                    f.write(f"{unit}, {name}, {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                last_scanned[name] = now
                print(f"Logged {Output}: {name}")

            pts = np.array([code.polygon], np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, color, 3)
            cv2.putText(frame, Output, (pts[0][0][0], pts[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        idle_time = time.time() - last_seen_qr
        if idle_time > 40:
            print("\n[SYSTEM] No QR detected for 40 seconds. Auto-quitting...")
            break

        
        cv2.imshow("Check-In System", frame)
        key = cv2.waitKey(50) & 0xFF
        if key in [ord('q'), ord('Q')]:
            break
        

    
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Scanner stopped.")
    input("[Press Enter to return to menu]: ")


# --- Clear Terminal ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# --- MAIN MENU LOOP ---
def Show_Menu():
    while True:
        clear_screen()
        print("=" * 40)
        print("      MSI SMARTGUARD SYSTEM v2.0      ")
        print("=" * 40)
        print(" [1] Register New Resident")
        print(" [2] Start QR Code Scanner")
        print(" [3] Exit Program")
        print("-" * 40)
        print(" [0] Type '0' to clear the screen")
        
        print("\n\n (YOU):\n ", end="")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            register_resident()
        elif choice == "2":
            start_scanner()
        elif choice == "3":
            print("Thanks for your join! Exiting program....")
            break
        elif choice.lower() in ["0", "clear", "cls", "refresh"]:
            clear_screen()
        else:
            print("Please enter between 1 to 3")


Show_Menu()