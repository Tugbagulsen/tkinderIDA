import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import numpy as np
import pytesseract
from tkinderIDA.Master.balls_controlBoat import drive_boat, turn_left, turn_right, go_straight

# Tesseract'ın yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def rakam_ve_konum_oku(goruntu):
    yukseklik, genislik = goruntu.shape[:2]
    
    # Görüntüyü kırpma işlemi (orijinal koddaki gibi)
    sol_kesim = int(genislik * 0.07)
    sag_kesim = int(genislik * 0.92)
    kirpilmis_goruntu = goruntu[:, sol_kesim:sag_kesim]
    
    gri = cv2.cvtColor(kirpilmis_goruntu, cv2.COLOR_BGR2GRAY)
    gri = cv2.medianBlur(gri, 5)
    
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=123'
    veri = pytesseract.image_to_data(gri, config=custom_config, output_type=pytesseract.Output.DICT)
    
    birler, ikiler, ucler = [], [], []
    tespit_edilen_rakamlar = []
    
    for i in range(len(veri['text'])):
        if veri['text'][i] in ['1', '2', '3']:
            tespit_edilen_rakamlar.append(veri['text'][i])
            x = veri['left'][i] + sol_kesim  # Kırpılmış görüntüye göre ayarlama
            y = veri['top'][i]
            w = veri['width'][i]
            h = veri['height'][i]
            if veri['text'][i] == '1':
                birler.append((x, y, w, h))
            elif veri['text'][i] == '2':
                ikiler.append((x, y, w, h))
            elif veri['text'][i] == '3':
                ucler.append((x, y, w, h))
    
    return birler, ikiler, ucler, tespit_edilen_rakamlar

# Tkinter GUI setup
root = tk.Tk()
root.title("Ball Detection, OCR and Motor Control")
root.geometry("800x600")

label_frame_veri = LabelFrame(root, text="Video Feed", width=640, height=480)
label_frame_veri.pack(padx=10, pady=10)

label_veri = tk.Label(label_frame_veri)
label_veri.pack()

# OCR ile tespit edilen rakamları göstermek için Label
label_rakamlar = tk.Label(root, text="Tespit edilen rakamlar: Yok", font=("Arial", 16))
label_rakamlar.pack(pady=10)

# Function to start video capture
def start_video_capture():
    cap = cv2.VideoCapture(0)  # Capture from default camera
    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not found or cannot be opened!")
        return

    def video_thread():
        orjin = (320, 240)  # Define the center of the screen

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Color detection process (from your previous code)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_red = np.array([0, 120, 70])
                upper_red = np.array([10, 255, 255])
                mask = cv2.inRange(hsv, lower_red, upper_red)
                mask = cv2.GaussianBlur(mask, (5, 5), 2)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contours) >= 2:
                    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
                    centers = []
                    for contour in contours:
                        M = cv2.moments(contour)
                        if M['m00'] != 0:
                            cX = int(M['m10'] / M['m00'])
                            cY = int(M['m01'] / M['m00'])
                            centers.append((cX, cY))
                            cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)
                    
                    if len(centers) == 2:
                        mid_way = ((centers[0][0] + centers[1][0]) // 2,
                                   (centers[0][1] + centers[1][1]) // 2)
                        cv2.circle(frame, mid_way, 5, (255, 0, 0), -1)
                        drive_boat(mid_way, orjin, turn_left, turn_right, go_straight)
                else:
                    # Eğer top algılanmazsa gemiyi düz devam ettir
                    go_straight()

                # OCR process to detect numbers 1, 2, 3
                birler, ikiler, ucler, tespit_edilen_rakamlar = rakam_ve_konum_oku(frame)

                # Tespit edilen rakamları GUI'de göster
                if tespit_edilen_rakamlar:
                    label_rakamlar.config(text=f"Tespit edilen rakamlar: {', '.join(tespit_edilen_rakamlar)}")
                else:
                    label_rakamlar.config(text="Tespit edilen rakamlar: Yok")

                # Convert the frame from BGR to RGB for Tkinter display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                label_veri.imgtk = imgtk
                label_veri.config(image=imgtk)

            time.sleep(0.05)

        cap.release()

    threading.Thread(target=video_thread, daemon=True).start()

# Button to start video capture
start_button = tk.Button(root, text="Start Video Capture", command=start_video_capture)
start_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
