import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import numpy as np
import pytesseract
from tkinderIDA.Master.balls_part import *
from tkinderIDA.Master.dedect_digit import *
from tkinderIDA.Master.ihas_part import *
import keyboard

# Tesseract'ın yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Tkinter GUI Kurulumu
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

# Video capture için iki ayrı thread kullanımı
def start_video_capture():
    # Bu kısımda kameranın index numarası belirtilmelidir
    boat_camera = 0  # GEMİNİN KAMERASI
    iha_camera = 1   # İHA KAMERASI
    
    cap_boat = cv2.VideoCapture(boat_camera)
    cap_iha = cv2.VideoCapture(iha_camera)
    
    if not cap_boat.isOpened():
        messagebox.showerror("Error", "BOAT Camera not found or cannot be opened!")
        return

    if not cap_iha.isOpened():
        messagebox.showerror("Error", "IHA Camera not found or cannot be opened!")
        return

    def video_thread_boat():
        while cap_boat.isOpened():
            ret, frame = cap_boat.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                drive_boat(frame)

                # BGR -> RGB conversion for Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                label_veri.imgtk = imgtk
                label_veri.config(image=imgtk)

            time.sleep(0.05)

        cap_boat.release()

    def video_thread_iha():
        PORT = int(input("PORT: "))  # Port sadece bir kez alınır
        while cap_iha.isOpened():
            ret, frame = cap_iha.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                IHA_commands(frame, PORT)

                # BGR -> RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                label_veri.imgtk = imgtk
                label_veri.config(image=imgtk)

            time.sleep(0.05)

        cap_iha.release()

    # Bot ve iha için iki ayrı thread oluşturuldu
    threading.Thread(target=video_thread_boat).start()
    threading.Thread(target=video_thread_iha).start()

# Start buton
start_button = tk.Button(root, text="Start Video Capture", command=start_video_capture)
start_button.pack(pady=20)

# Tkinter main loop
root.mainloop()
