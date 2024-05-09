import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
from datetime import datetime

# Tkinter ana penceresi
master = tk.Tk()

# Başlangıç penceresi boyutları
canvas_genislik = 1000
canvas_yukseklik = 450
panel_genislik = 150
panel_yukseklik = 250
panel_margin = 10
top_margin = 20

# Kanvas oluşturma
canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()

# Panel oluşturma fonksiyonu
def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

# Veri Paneli (Kamera görüntüsü burada olacak)
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, top_margin / canvas_yukseklik, 0.5, 0.65)

# Arac Paneli (başka bir örnek için)
label_frame_arac = label_frame_olusturma(master, "Arac", 0.6, 0.04, 0.34, 0.1)
label_arac = tk.Label(label_frame_arac, text="Jetson Nano    192.168.1.1")
label_arac.pack(padx=15, pady=5, anchor=tk.NW)

# Sonuç Paneli (veriler burada gösterilecek)
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.04, top_margin / 28, 0.9, 0.2)

# Fonksiyon Paneli
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.2, 0.35, 0.5)

# Fonksiyonlar
def btnCamera():
    start_video_capture()

# Diğer buton fonksiyonları
def btnBatma():
    messagebox.showinfo("Bilgi", "Batma butonuna tıklandı")

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
    messagebox.showinfo("Bilgi", "Arm butonuna tıklandı")

def btnDisarm():
    messagebox.showinfo("Bilgi", "Disarm butonuna tıklandı")

def btnStabilize():
    messagebox.showinfo("Bilgi", "Stabilize butonuna tıklandı")

def btnAuto():
    messagebox.showinfo("Bilgi", "Auto butonuna tıklandı")

# Butonları yerleştirme
buton_metinleri = ["Batma", "Çıkma", "Sağ", "Sol", "İleri", "Geri", "Kamera", "Reset", "Arm", "Disarm", "Stabilize", "Auto"]
buton_fonksiyonlari = [btnBatma, btnCikma, btnSag, btnSol, btnIleri, btnGeri, btnCamera, btnReset, btnArm, btnDisarm, btnStabilize, btnAuto]

for i, metin in enumerate(buton_metinleri):
    row = i // 2
    column = i % 2
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White', command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)

# Kamera görüntüsü için fonksiyon
def start_video_capture():
    label_veri = tk.Label(label_frame_veri)  # "Veri" paneli için
    label_veri.pack()

    def video_thread():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera bulunamadı veya açılamadı!")
            return

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)

                # Görüntüyü "Veri" panelindeki etikete yerleştir
                label_veri.config(image=frame)
                label_veri.image = frame

            else:
                break

        # Kaynakları serbest bırak
        cap.release()

    threading.Thread(target=video_thread, daemon=True).start()



# sonuc paneline kameradan veri gelmeli
def update_sonuc_panel(text):
    label_sonuc = tk.Label(label_frame_sonuc, text=text)
    label_sonuc.pack()


update_sonuc_panel("test") # simdilik kalsin

master.mainloop()
