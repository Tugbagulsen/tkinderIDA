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

from IHA.find_way import *
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
    konum_kontrol = 0
    
    # GEMİ KAMERASI İNDEXİ
    IHA_kamera = 0  # IHA KAMERASI
    hedef_liman = int(input("Hedef liman sayısı"))
    
    # Kamera başlatma
    cap_IHA = cv2.VideoCapture(IHA_kamera)
    # Kamera kaydı açılamazsa hata mesajı ver
    if not cap_IHA.isOpened():
        messagebox.showerror("Error", "BOAT Camera not found or cannot be opened!")
        return
    
    # Video kaydı için isim ve codec tanımlamaları
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"Akriha_Control_{now}.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_width = int(cap_IHA.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap_IHA.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))

    def video_thread_IHA():
        while cap_IHA.isOpened():
            ret, frame = cap_IHA.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                drive_IHA(ret , frame, hedef_liman, konum_kontrol)  # Bu fonksiyonun düzgün çalıştığından emin olun
                out.write(frame)  # Videoyu kaydet
            time.sleep(0.05)

        cap_IHA.release()  # Değişiklik: Kamera kaynağını kapatma
        out.release()  # Değişiklik: Video kaynağını kapatma
        
    video_thread_IHA()
    
    
if __name__ == '__main__':
    main()