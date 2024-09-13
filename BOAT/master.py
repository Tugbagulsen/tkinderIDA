import tkinter as tk
from tkinter import messagebox
import sys

import cv2

from PIL import Image, ImageTk
import pigpio

import threading
import time
from datetime import datetime

import numpy as np

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from BOAT.find_way import *

"""

# Motorların bağlı olduğu GPIO pinleri
left_motor_pin = 17   # Sol motor ESC pini
right_motor_pin = 18  # Sağ motor ESC pini

# ESC'leri kontrol etmek için pigpio nesnesi oluştur
pi = pigpio.pi()

# Değişiklik: pigpio bağlantısının kontrol edilmesi
if not pi.connected:
    messagebox.showerror("Error", "Pigpio daemon not running!")
    sys.exit()  # Hata varsa program sonlandırılır

"""

def main():
    start_video_capture()

# Video capture için iki ayrı thread kullanımı
def start_video_capture():
    # GEMİ KAMERASI İNDEXİ
    boat_camera = 0  # GEMİNİN KAMERASI
    
    # Kamera başlatma
    cap_boat = cv2.VideoCapture(boat_camera)
    # Kamera kaydı açılamazsa hata mesajı ver
    if not cap_boat.isOpened():
        messagebox.showerror("Error", "BOAT Camera not found or cannot be opened!")
        return
    
    # Video kaydı için isim ve codec tanımlamaları
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"Akriha_Control_{now}.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_width = int(cap_boat.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap_boat.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))

    def video_thread_boat():
        while cap_boat.isOpened():
            ret, frame = cap_boat.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                #drive_boat(ret , frame)  # Bu fonksiyonun düzgün çalıştığından emin olun
                out.write(frame)  # Videoyu kaydet
            time.sleep(0.05)

        cap_boat.release()  # Değişiklik: Kamera kaynağını kapatma
        out.release()  # Değişiklik: Video kaynağını kapatma

if __name__ == '__main__':
    main()