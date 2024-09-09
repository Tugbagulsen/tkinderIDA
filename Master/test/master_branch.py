import tkinter as tk
from tkinter import messagebox
import sys
from gui import *
import sys
sys.path.append('c:/Users/Ahmet/Documents/GitHub/tkinderIDA/Master/test/driving/')

import cv2

from PIL import Image, ImageTk
# import pigpio  # pigpio modülü devre dışı bırakıldı

import threading
import time
from datetime import datetime

import numpy as np

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from dedect_digit import *
from gui import *
from driving.balls_part  import *
from driving.ihas_part import *
from driving.IHA_Muhamemed import *
from driving.IHA_Nesli import *
# Diğer buton fonksiyonları
def btnBatma():
    messagebox.showinfo("Bilgi", "Batma butonuna tikandi")

def btnCikma():
    messagebox.showinfo("Bilgi", "Çıkma butonuna tıklandı")

def btnSag():
    messagebox.showinfo("Bilgi", "Sağ butonuna tıklandı")

def btnSol():
    messagebox.showinfo("Bilgi", "Sol butonuna tıklandı")

def btnIleri():
    messagebox.showinfo("Bilgi", "İleri butonuna tıklandı")

def btnGeri():
    messagebox.showinfo("Bilgi", "Geri butonuna tıklandı")

def btnReset():
    messagebox.showinfo("Bilgi", "Reset butonuna tıklandı")

def btnArm():
    messagebox.showinfo("Bilgi", "Arm butonuna tıkandı")

def btnDisarm():
    messagebox.showinfo("Bilgi", "Disarm butonuna tıklandı")

def btnStabilize():
    messagebox.showinfo("Bilgi", "Stabilize butonuna tıklandı")

def btnAuto():
    messagebox.showinfo("Bilgi", "Auto butonuna tıklandı")
    
def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = tk.LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

def btnCamera():
    start_video_capture()

# Tkinter ana penceresi
master = tk.Tk()
# Başlangıç penceresi boyutları

canvas_genislik = 1000
canvas_yukseklik = 450

# Tkinter ana penceresi
master.title("Kamera ve Veri Okuma Uygulamasi")

# Kanvas oluşturma
canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()


# Veri Paneli (Kamera görüntüsü burada olacak)
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, 0.05, 0.5, 0.65)

# Araç Paneli
label_frame_arac = label_frame_olusturma(master, "Araç", 0.6, 0.04, 0.34, 0.1)
label_arac = tk.Label(label_frame_arac, text="AKRIHA V1.0")
label_arac.pack(padx=15, pady=5, anchor=tk.NW)

# Sonuç Paneli
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.6, 0.2, 0.35, 0.5)

# Fonksiyon Paneli
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.6, 0.35, 0.3)

# Kamera açma butonu


buton_metinleri = ["Batma", "Çıkma", "Sağ", "Sol", "İleri", "Geri", "Kamera", "Reset", "Arm", "Disarm", "Stabilize", "Auto"]
buton_fonksiyonlari = [btnBatma, btnCikma, btnSag, btnSol, btnIleri, btnGeri, btnCamera, btnReset, btnArm, btnDisarm, btnStabilize, btnAuto]

for i, metin in enumerate(buton_metinleri):
    row, column = divmod(i, 2)
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White', command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)

# Sonuç paneline veri yazdırmak için fonksiyon
def update_sonuc_panel(text):
    for widget in label_frame_sonuc.winfo_children():
        widget.destroy()
    label = tk.Label(label_frame_sonuc, text=text)
    label.pack()

# Motorların bağlı olduğu GPIO pinleri
# left_motor_pin = 17   # Sol motor ESC pini  # pigpio ile ilgili kısımlar yorum satırına alındı
# right_motor_pin = 18  # Sağ motor ESC pini  # pigpio ile ilgili kısımlar yorum satırına alındı

# ESC'leri kontrol etmek için pigpio nesnesi oluştur
# pi = pigpio.pi()

# Değişiklik: pigpio bağlantısının kontrol edilmesi
# if not pi.connected:
#     messagebox.showerror("Error", "Pigpio daemon not running!")
#     sys.exit()  # Hata varsa program sonlandırılır

# Global olarak cap_boat ve cap_iha tanımlıyoruz
cap_boat = None  # Değişiklik: Global tanımlama
cap_iha = None   # Değişiklik: Global tanımlama

# Video capture için iki ayrı thread kullanımı
def start_video_capture():
    global cap_boat, cap_iha  # Değişiklik: Global değişkenleri kullan

    boat_camera = 0  # GEMİNİN KAMERASI
    iha_camera = 1   # İHA KAMERASI
    
    cap_boat = cv2.VideoCapture(boat_camera)
    # cap_iha = cv2.VideoCapture(iha_camera)
    
    if not cap_boat.isOpened():
        messagebox.showerror("Error", "BOAT Camera not found or cannot be opened!")
        return

    if not cap_iha.isOpened():
        messagebox.showerror("Error", "IHA Camera not found or cannot be opened!")
        return
    
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
                drive_boat(frame)  # Bu fonksiyonun düzgün tanımlandığından emin olun
                out.write(frame)  # Videoyu kaydet
            time.sleep(0.05)

        cap_boat.release()  # Değişiklik: Kamera kaynağını kapatma
        out.release()  # Değişiklik: Video kaynağını kapatma
    """
    def video_thread_iha():
        PORT = int(port_entry.get())  # Değişiklik: input() yerine GUI giriş kullanıldı
        while cap_iha.isOpened():
            ret, frame = cap_iha.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # IHA_commands_NESLI(frame, PORT)  # Bu fonksiyon aktif olmalı

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                # Değişiklik: Görüntüyü veri panelinde gösterme
                label_image = tk.Label(label_frame_veri, image=imgtk)
                label_image.image = imgtk  # Referansı kaybetmemek için
                label_image.pack()

            time.sleep(0.05)

        cap_iha.release()  # Değişiklik: Kamera kaynağını kapatma
    """
    threading.Thread(target=video_thread_boat).start()
    #threading.Thread(target=video_thread_iha).start()

# Değişiklik: Pencere kapatıldığında kameraların kapatılması
def on_closing():
    global cap_boat, cap_iha  # Değişiklik: Global değişkenler
    if cap_boat is not None and cap_boat.isOpened():
        cap_boat.release()
    if cap_iha is not None and cap_iha.isOpened():
        cap_iha.release()
    master.destroy()

master.protocol("WM_DELETE_WINDOW", on_closing)

# Değişiklik: PORT giriş alanı
port_entry = tk.Entry(master)
port_entry.pack()

master.mainloop()